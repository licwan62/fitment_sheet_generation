# 手动初始 prompt 后，自动循环发送“下一步”，直到检测到完成信号。

param(
    [string]$ChatGptUrl = "https://chatgpt.com/",
    [string]$Browser = "openclaw",
    [string]$OpenClawCommand = "openclaw.cmd",
    [string]$OpenClawConfigPath = "",
    [string]$OpenClawGatewayUrl = "",
    [string]$OpenClawBrowserUrl = "",
    [int]$MaxNextSteps = 100,
    [string]$NextMessage = "下一步",
    [int]$ReplyStabilityDelay = 10,
    [int]$OperationDelay = 2,
    [int]$PostReplyDelay = 2,
    [int]$MaxReplyWaitSeconds = 900,
    [int]$XBrowserRetryCount = 2,
    [int]$XBrowserRecoverDelay = 3,
    [string]$TranscriptPath = (Join-Path (Join-Path $PSScriptRoot "transcripts") ("auto_next_transcript_{0}.md" -f (Get-Date -Format "yyyyMMdd_HHmmss"))),
    [switch]$OpenOnly
)

$ErrorActionPreference = "Stop"

$TranscriptDir = Split-Path -Parent $TranscriptPath
if (-not [string]::IsNullOrWhiteSpace($TranscriptDir) -and -not (Test-Path $TranscriptDir)) {
    New-Item -ItemType Directory -Path $TranscriptDir | Out-Null
}

$oldLibraryOnly = $env:FITMENT_OPENCLAW_LIBRARY_ONLY
try {
    $env:FITMENT_OPENCLAW_LIBRARY_ONLY = "1"
    . (Join-Path $PSScriptRoot "qclaw_fitment_automation.ps1") `
        -ChatGptUrl $ChatGptUrl `
        -Browser $Browser `
        -OpenClawCommand $OpenClawCommand `
        -OpenClawConfigPath $OpenClawConfigPath `
        -OpenClawGatewayUrl $OpenClawGatewayUrl `
        -OpenClawBrowserUrl $OpenClawBrowserUrl `
        -MaxNextSteps $MaxNextSteps `
        -ReplyStabilityDelay $ReplyStabilityDelay `
        -OperationDelay $OperationDelay `
        -PostReplyDelay $PostReplyDelay `
        -MaxReplyWaitSeconds $MaxReplyWaitSeconds `
        -XBrowserRetryCount $XBrowserRetryCount `
        -XBrowserRecoverDelay $XBrowserRecoverDelay `
        -OpenOnly:$OpenOnly
}
finally {
    if ($null -eq $oldLibraryOnly) { Remove-Item Env:FITMENT_OPENCLAW_LIBRARY_ONLY -ErrorAction SilentlyContinue }
    else { $env:FITMENT_OPENCLAW_LIBRARY_ONLY = $oldLibraryOnly }
}

function Get-XBErrorDetail {
    param($Result)

    $parts = @()
    if ($Result -and $Result.error) { $parts += [string]$Result.error }
    if ($Result -and $Result.hint) { $parts += [string]$Result.hint }
    if ($Result -and $Result.data -and $Result.data.raw_error) { $parts += [string]$Result.data.raw_error }
    elseif ($Result -and $Result.data -and $Result.data.result -and $Result.data.result.error) { $parts += [string]$Result.data.result.error }
    if ($parts.Count -eq 0) { return "" }
    return ($parts -join " ")
}

function Test-XBRecoverableError {
    param([string]$Detail)

    if ([string]::IsNullOrWhiteSpace($Detail)) { return $false }

    $recoverablePatterns = @(
        "Unknown error",
        "Session with given id not found",
        "Target closed",
        "No target with given id found",
        "Protocol error",
        "CDP",
        "browser has disconnected",
        "websocket",
        "ECONNRESET",
        "ECONNREFUSED",
        "ERR_ABORTED"
    )

    foreach ($pattern in $recoverablePatterns) {
        if ($Detail -like "*$pattern*") { return $true }
    }

    return $false
}

function Repair-XBrowserSession {
    param([string]$Reason)

    Write-Host "  xbrowser 会话异常，尝试恢复: $Reason" -ForegroundColor Yellow
    try {
        Invoke-XB "cleanup" | Out-Null
    }
    catch {
        Write-Host "  cleanup 失败，继续重新初始化: $($_.Exception.Message)" -ForegroundColor Yellow
    }

    Start-Sleep -Seconds $XBrowserRecoverDelay
    Initialize-XBrowser

    try {
        $reopen = Invoke-XB "run" "--browser" $Browser "open" $ChatGptUrl
        if (-not $reopen.ok) {
            $detail = Get-XBErrorDetail -Result $reopen
            Write-Host "  恢复后重新打开 ChatGPT 未确认成功: $detail" -ForegroundColor Yellow
        }
        else {
            Start-Sleep -Seconds 3
        }
    }
    catch {
        Write-Host "  恢复后重新打开 ChatGPT 失败，稍后由原操作重试: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

function Invoke-XBRun {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$ActionArgs)

    $xbArgs = @("run", "--browser", $Browser) + $ActionArgs
    $maxAttempts = [Math]::Max(1, $XBrowserRetryCount + 1)
    $lastResult = $null

    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {
        try {
            $result = Invoke-XB @xbArgs
        }
        catch {
            $detailText = $_.Exception.Message
            if (($attempt -lt $maxAttempts) -and (Test-XBRecoverableError -Detail $detailText)) {
                Write-Host "  xbrowser 执行异常，准备重试 ($attempt/$($maxAttempts - 1)): $detailText" -ForegroundColor Yellow
                Repair-XBrowserSession -Reason $detailText
                continue
            }
            throw
        }

        $lastResult = $result

        if ($result.ok) {
            if ($result.data -and $result.data.result) { return $result.data.result }
            return $result.data
        }

        $detailText = Get-XBErrorDetail -Result $result
        if (($attempt -lt $maxAttempts) -and (Test-XBRecoverableError -Detail $detailText)) {
            Write-Host "  xbrowser 操作失败，准备重试 ($attempt/$($maxAttempts - 1)): $detailText" -ForegroundColor Yellow
            Repair-XBrowserSession -Reason $detailText
            continue
        }

        break
    }

    $detail = Get-XBErrorDetail -Result $lastResult
    throw "xbrowser 操作失败: $($lastResult.error) $detail"
}

function Get-XBValue {
    param($Result)

    if ($null -eq $Result) { return $null }
    if ($Result.PSObject.Properties.Name -contains "success" -and $Result.PSObject.Properties.Name -contains "data") {
        $data = $Result.data
        if ($null -eq $data) { return $null }
        if ($data.PSObject.Properties.Name -contains "result") { return $data.result }
        return $data
    }
    if ($Result.PSObject.Properties.Name -contains "value") { return $Result.value }
    if ($Result.PSObject.Properties.Name -contains "result") { return $Result.result }
    if ($Result.PSObject.Properties.Name -contains "text") { return $Result.text }
    return $Result
}

function Initialize-XBrowser {
    Write-Host "初始化 OpenClaw browser..." -ForegroundColor Yellow
    $init = Invoke-XB "init"

    if (-not $init.ok) {
        throw "OpenClaw browser 初始化失败: $($init.error) $($init.hint)"
    }

    Write-Host "OpenClaw browser 就绪。" -ForegroundColor Green
}

function Open-ChatGPT {
    Write-Host "打开 ChatGPT: $ChatGptUrl" -ForegroundColor Yellow
    $openArgs = @("run", "--browser", $Browser, "open", $ChatGptUrl)
    $allowCleanupRetry = $true

    while ($true) {
        $openResult = Invoke-XB @openArgs
        if ($openResult.ok) { break }

        $rawError = Get-XBErrorDetail -Result $openResult

        $currentUrl = ""
        try {
            $urlValue = Get-XBValue (Invoke-XBRun "get" "url")
            if ($urlValue -and $urlValue.url) { $currentUrl = [string]$urlValue.url } else { $currentUrl = [string]$urlValue }
        }
        catch { }

        if ($currentUrl -like "https://chatgpt.com*") { break }

        if ($rawError -like "*ERR_ABORTED*") {
            Write-Host "open 返回 ERR_ABORTED，改用新标签页打开 ChatGPT..." -ForegroundColor Yellow
            Invoke-XBRun "tab" "new" $ChatGptUrl | Out-Null
            break
        }

        if ($allowCleanupRetry -and (Test-XBRecoverableError -Detail $rawError)) {
            Write-Host "检测到 xbrowser/CDP 会话异常，执行 cleanup 后重试一次..." -ForegroundColor Yellow
            try {
                Invoke-XB "cleanup" | Out-Null
            }
            catch {
                Write-Host "  cleanup 执行失败，继续尝试重新初始化: $($_.Exception.Message)" -ForegroundColor Yellow
            }
            Start-Sleep -Seconds $XBrowserRecoverDelay
            Initialize-XBrowser
            $allowCleanupRetry = $false
            continue
        }

        throw "打开 ChatGPT 失败: $($openResult.error) $rawError"
    }

    Start-Sleep -Seconds 3
    try { Invoke-XBRun "wait" "--load" "networkidle" | Out-Null } catch { }
}

function Ensure-ChatGPTActive {
    $currentUrl = ""
    try {
        $urlValue = Get-XBValue (Invoke-XBRun "get" "url")
        if ($urlValue -and $urlValue.url) { $currentUrl = [string]$urlValue.url } else { $currentUrl = [string]$urlValue }
    }
    catch { }

    if ($currentUrl -like "https://chatgpt.com*") { return }

    try {
        $tabResult = Get-XBValue (Invoke-XBRun "tab")
        $tabs = @($tabResult.tabs)
        $chatTab = $tabs | Where-Object { $_.url -like "https://chatgpt.com*" } | Select-Object -First 1
        if ($chatTab) {
            Invoke-XBRun "tab" ([string]$chatTab.index) | Out-Null
            Start-Sleep -Seconds 1
            return
        }
    }
    catch { }

    Invoke-XBRun "tab" "new" $ChatGptUrl | Out-Null
    Start-Sleep -Seconds 3
}

function Get-ChatGPTState {
    Ensure-ChatGPTActive
    $script = @'
(() => {
  const textOf = el => (el && (el.innerText || el.textContent || el.value || '') || '').trim();
  const cleanReplyText = text => (text || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(line => line.trimEnd())
    .filter(line => !/^\s*(ChatGPT\s*(说|said)?|You said|你说)\s*[:：]?\s*$/.test(line))
    .join('\n')
    .trim();
  const extractReplyText = node => {
    if (!node) return '';
    const container = node.closest('article') || node.closest('[data-testid*="conversation-turn"]') || node;
    const selectors = [
      '[data-message-content]',
      '[data-testid="markdown"]',
      '[class*="markdown"]',
      '.markdown',
      '[data-message-author-role="assistant"]'
    ];
    const candidates = [];
    for (const selector of selectors) {
      container.querySelectorAll(selector).forEach(el => {
        const text = cleanReplyText(textOf(el));
        if (text) candidates.push(text);
      });
    }
    const clone = container.cloneNode(true);
    clone.querySelectorAll('button, svg, form, textarea, [contenteditable="true"], [role="button"], [aria-hidden="true"]').forEach(el => el.remove());
    const containerText = cleanReplyText(textOf(clone));
    if (containerText) candidates.push(containerText);
    if (!candidates.length) return '';
    return candidates.sort((a, b) => b.length - a.length)[0];
  };
  const isVisible = el => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  let assistantNodes = Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'));
  if (assistantNodes.length === 0) {
    assistantNodes = Array.from(document.querySelectorAll('article')).filter(el => {
      const role = el.getAttribute('data-message-author-role') || '';
      return role !== 'user';
    });
  }
  if (assistantNodes.length === 0) {
    assistantNodes = Array.from(document.querySelectorAll('main [class*="markdown"]'));
  }
  const assistantTexts = assistantNodes.map(extractReplyText).filter(t => t.length > 0);
  const reply = assistantTexts.length ? assistantTexts[assistantTexts.length - 1] : '';
  const editor = Array.from(document.querySelectorAll('#prompt-textarea, textarea, [contenteditable="true"], [role="textbox"]'))
    .find(el => isVisible(el) && !el.disabled && el.getAttribute('aria-disabled') !== 'true');
  const buttons = Array.from(document.querySelectorAll('button'));
  const buttonText = b => ((b.getAttribute('aria-label') || '') + ' ' + (b.innerText || '')).toLowerCase();
  const isGenerating = buttons.some(b => /stop|停止/.test(buttonText(b)) && !b.disabled && isVisible(b));
  const pageText = document.body.innerText || '';
  return {
    reply,
    inputReady: !!editor && !editor.disabled && editor.getAttribute('aria-disabled') !== 'true',
    isGenerating,
    loggedOut: /log in|sign up|登录|注册/.test(pageText) && !editor,
    pageError: /something went wrong|network error|页面错误|网络错误|出错了/.test(pageText)
  };
})()
'@
    return (Get-XBValue (Invoke-XBRun "eval" $script))
}

function Set-ChatGPTEditorText {
    param([string]$Text)

    Ensure-ChatGPTActive
    $encodedText = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($Text))
    $script = @"
(() => {
  const encoded = '$encodedText';
  const nextValue = new TextDecoder().decode(Uint8Array.from(atob(encoded), c => c.charCodeAt(0)));
  const isVisible = el => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const editor = Array.from(document.querySelectorAll('#prompt-textarea, textarea, [contenteditable="true"], [role="textbox"]'))
    .find(el => isVisible(el) && !el.disabled && el.getAttribute('aria-disabled') !== 'true');
  if (!editor) return { ok: false, reason: 'no-editor' };

  editor.focus();
  if (editor.scrollIntoView) editor.scrollIntoView({ block: 'center' });

  if ('value' in editor) {
    const proto = Object.getPrototypeOf(editor);
    const descriptor = proto ? Object.getOwnPropertyDescriptor(proto, 'value') : null;
    if (descriptor && descriptor.set) descriptor.set.call(editor, nextValue);
    else editor.value = nextValue;
    editor.dispatchEvent(new InputEvent('input', { bubbles: true, data: nextValue, inputType: 'insertText' }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
    return { ok: true };
  }

  if (editor.isContentEditable) {
    editor.innerHTML = '';
    nextValue.split(/\r?\n/).forEach((line, index) => {
      if (index > 0) editor.appendChild(document.createElement('br'));
      editor.appendChild(document.createTextNode(line));
    });
    editor.dispatchEvent(new InputEvent('input', { bubbles: true, data: nextValue, inputType: 'insertText' }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
    return { ok: true };
  }

  return { ok: false, reason: 'unsupported-editor' };
})()
"@
    $result = Get-XBValue (Invoke-XBRun "eval" $script)
    if (-not $result -or -not $result.ok) {
        $reason = if ($result -and $result.reason) { [string]$result.reason } else { "unknown" }
        throw "写入 ChatGPT 输入框失败: $reason"
    }
}

function Click-ChatGPTSendButton {
    $script = @'
(() => {
  const direct = document.querySelector('[data-testid="send-button"], [data-testid="composer-send-button"], button[aria-label*="Send"], button[aria-label*="发送"]');
  const buttons = Array.from(document.querySelectorAll('button'));
  const match = direct || buttons.find(b => {
    const t = ((b.getAttribute('aria-label') || '') + ' ' + (b.innerText || '') + ' ' + (b.getAttribute('data-testid') || '')).toLowerCase();
    return !b.disabled && /(send|发送|submit)/.test(t);
  });
  if (!match || match.disabled || match.getAttribute('aria-disabled') === 'true') return false;
  match.click();
  return true;
})()
'@
    $clicked = Get-XBValue (Invoke-XBRun "eval" $script)
    if (-not $clicked) {
        Invoke-XBRun "press" "Enter" | Out-Null
    }
}

function Send-ChatGPTMessage {
    param([string]$Message)

    Set-ChatGPTEditorText -Text $Message
    Start-Sleep -Seconds $OperationDelay
    Click-ChatGPTSendButton
    Start-Sleep -Seconds $OperationDelay
}

function Copy-LastChatGPTReplyText {
    param([string]$FallbackReply = "")

    Ensure-ChatGPTActive
    $script = @'
(() => {
  const textOf = el => (el && (el.innerText || el.textContent || '') || '').trim();
  const cleanReplyText = text => (text || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(line => line.trimEnd())
    .filter(line => !/^\s*(ChatGPT\s*(说|said)?|You said|你说)\s*[:：]?\s*$/.test(line))
    .join('\n')
    .trim();
  const extractReplyText = node => {
    const container = node.closest('article') || node.closest('[data-testid*="conversation-turn"]') || node;
    const selectors = [
      '[data-message-content]',
      '[data-testid="markdown"]',
      '[class*="markdown"]',
      '.markdown',
      '[data-message-author-role="assistant"]'
    ];
    const candidates = [];
    for (const selector of selectors) {
      container.querySelectorAll(selector).forEach(el => {
        const text = cleanReplyText(textOf(el));
        if (text) candidates.push(text);
      });
    }
    const clone = container.cloneNode(true);
    clone.querySelectorAll('button, svg, form, textarea, [contenteditable="true"], [role="button"], [aria-hidden="true"]').forEach(el => el.remove());
    const containerText = cleanReplyText(textOf(clone));
    if (containerText) candidates.push(containerText);
    if (!candidates.length) return '';
    return candidates.sort((a, b) => b.length - a.length)[0];
  };
  let assistantNodes = Array.from(document.querySelectorAll('[data-message-author-role="assistant"]'));
  if (assistantNodes.length === 0) {
    assistantNodes = Array.from(document.querySelectorAll('article')).filter(el => {
      const role = el.getAttribute('data-message-author-role') || '';
      return role !== 'user';
    });
  }
  if (assistantNodes.length === 0) return { ok: false, reason: 'no-assistant-node' };
  const last = assistantNodes[assistantNodes.length - 1];
  last.scrollIntoView({ block: 'center' });
  const text = extractReplyText(last);
  if (!text) return { ok: false, reason: 'empty-reply' };
  if (/^(ChatGPT\s*(说|said)?|更新点|当前批次进度|下一步方向)\s*[:：]?\s*$/i.test(text)) {
    return { ok: false, reason: 'reply-shell-only' };
  }
  return { ok: true, text };
})()
'@
    $replyResult = Get-XBValue (Invoke-XBRun "eval" $script)
    if (-not $replyResult -or -not $replyResult.ok) {
        if ([string]::IsNullOrWhiteSpace($FallbackReply)) {
            $reason = if ($replyResult -and $replyResult.reason) { [string]$replyResult.reason } else { "unknown" }
            throw "读取最后一条回复失败: $reason"
        }
        $fallbackTrimmed = $FallbackReply.Trim()
        if ($fallbackTrimmed -match "^(ChatGPT\s*(说|said)?|更新点|当前批次进度|下一步方向)\s*[:：]?\s*$") {
            $reason = if ($replyResult -and $replyResult.reason) { [string]$replyResult.reason } else { "unknown" }
            throw "读取最后一条回复失败: $reason；状态文本也只是回复外壳"
        }
        return $FallbackReply.TrimEnd()
    }
    return ([string]$replyResult.text).TrimEnd()
}

function Wait-ChatGPTReplyComplete {
    $deadline = (Get-Date).AddSeconds($MaxReplyWaitSeconds)
    $lastReply = ""
    $stableSince = $null

    while ((Get-Date) -lt $deadline) {
        $state = Get-ChatGPTState
        if ($state.loggedOut) { return @{ Ok = $false; Status = "登录失效"; Remark = "ChatGPT 页面显示未登录"; Reply = "" } }
        if ($state.pageError) { return @{ Ok = $false; Status = "页面错误"; Remark = "页面出现错误提示"; Reply = [string]$state.reply } }

        $reply = [string]$state.reply
        if ($reply -ne $lastReply) {
            $lastReply = $reply
            $stableSince = Get-Date
        }
        elseif ($reply.Length -gt 0 -and -not $state.isGenerating -and $stableSince -and ((Get-Date) - $stableSince).TotalSeconds -ge $ReplyStabilityDelay) {
            Start-Sleep -Seconds $PostReplyDelay
            try {
                $reply = Copy-LastChatGPTReplyText -FallbackReply $reply
            }
            catch {
                Write-Host "  回复捕捉未取到正文，继续等待: $($_.Exception.Message)" -ForegroundColor Yellow
                $lastReply = ""
                $stableSince = $null
                Start-Sleep -Seconds 2
                continue
            }
            return @{ Ok = $true; Status = ""; Remark = ""; Reply = $reply }
        }

        Start-Sleep -Seconds 2
    }

    return @{ Ok = $false; Status = "超时"; Remark = "等待回复超过 $MaxReplyWaitSeconds 秒"; Reply = $lastReply }
}

function Test-CompletionSignal {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) { return $false }

    $patterns = @(
        "(^|[\r\n。！？.!?；;：:])\s*(本批次|当前批次|该批次)\s*(已)?完成\s*([。！？.!?；;]|$)",
        "(^|[\r\n。！？.!?；;：:])\s*批次(已)?(完成|结束)\s*([。！？.!?；;]|$)",
        "(^|[\r\n。！？.!?；;：:])\s*全部(已)?完成\s*([。！？.!?；;]|$)",
        "(^|[\r\n。！？.!?；;：:])\s*可[入出]库全量表\s*([。！？.!?；;]|$)"
    )

    foreach ($pattern in $patterns) {
        if ($Text -match $pattern) { return $true }
    }

    return $false
}

function Add-RoundTranscript {
    param(
        [int]$Round,
        [string]$Title,
        [string]$Reply
    )

    Add-Content -Path $TranscriptPath -Value "`r`n--- Round $Round / $Title ---`r`n$Reply`r`n" -Encoding UTF8
}

Initialize-XBrowser
Open-ChatGPT

if ($OpenOnly) {
    $checkUrl = [string](Invoke-OpenClawEvaluate -Expression "(() => location.href)()")
    Write-Host "OpenClaw 页面控制验证成功: $checkUrl" -ForegroundColor Green
    exit 0
}

"# Auto next transcript`r`n开始时间：$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")`r`n发送内容：$NextMessage`r`n" | Set-Content -Path $TranscriptPath -Encoding UTF8

Write-Host ""
Write-Host "请在 ChatGPT 页面手动写完并发送初始 prompt。" -ForegroundColor Cyan
Write-Host "确认初始 prompt 已经发出后，回到这个窗口按 Enter；脚本会等待首轮回复完成，然后一直发送下一步直到完成信号。" -ForegroundColor Cyan
[void](Read-Host "准备好后按 Enter 开始接管")

$round = 1
$nextCount = 0

while ($true) {
    Write-Host "等待第 $round 轮回复完成..." -ForegroundColor Gray
    $wait = Wait-ChatGPTReplyComplete
    $reply = [string]$wait.Reply
    $title = if ($round -eq 1) { "手动初始 prompt 回复" } else { "下一步回复" }
    Add-RoundTranscript -Round $round -Title $title -Reply $reply

    if (-not $wait.Ok) {
        Write-Host "停止: $($wait.Status) - $($wait.Remark)" -ForegroundColor Yellow
        Write-Host "记录文件: $TranscriptPath" -ForegroundColor Yellow
        exit 1
    }

    if (Test-CompletionSignal -Text $reply) {
        Add-Content -Path $TranscriptPath -Value "`r`n完成时间：$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")`r`n状态：检测到完成信号`r`n" -Encoding UTF8
        Write-Host "检测到完成信号，已停止。" -ForegroundColor Green
        Write-Host "记录文件: $TranscriptPath" -ForegroundColor Green
        exit 0
    }

    if ($nextCount -ge $MaxNextSteps) {
        Add-Content -Path $TranscriptPath -Value "`r`n停止时间：$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")`r`n状态：达到最大下一步次数 $MaxNextSteps`r`n" -Encoding UTF8
        Write-Host "达到最大下一步次数 $MaxNextSteps，已停止。" -ForegroundColor Yellow
        Write-Host "记录文件: $TranscriptPath" -ForegroundColor Yellow
        exit 2
    }

    $nextCount++
    $round++
    Write-Host "发送下一步 ($nextCount/$MaxNextSteps)..." -ForegroundColor Yellow
    Send-ChatGPTMessage -Message $NextMessage
}
