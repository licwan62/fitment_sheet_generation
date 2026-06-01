# qclaw 全量表补强自动化脚本
# 通过 QClaw xbrowser 控制 ChatGPT 网页版，遍历 TSV，多轮发送“下一步”，保存结果。

param(
    [string]$InputDir = (Join-Path $PSScriptRoot "input_sheets"),
    [string]$OutputDir = (Join-Path $PSScriptRoot "output_sheets"),
    [string]$LogPath = (Join-Path $PSScriptRoot "log.csv"),
    [string]$SummaryPath = (Join-Path $PSScriptRoot "summary.txt"),
    [string]$RequirementPath = (Join-Path $PSScriptRoot "requirement.md"),
    [string]$ChatGptUrl = "https://chatgpt.com/",
    [string]$Browser = "edge",
    [int]$MaxNextSteps = 30,
    [int]$ReplyStabilityDelay = 10,
    [int]$OperationDelay = 2,
    [int]$LargePayloadDelay = 8,
    [int]$PostReplyDelay = 2,
    [int]$MaxReplyWaitSeconds = 900,
    [double]$SimilarityThreshold = 0.95,
    [int]$MinNewChars = 100,
    [string[]]$OnlyFiles = @(),
    [switch]$ConfigureXBrowserQuick,
    [switch]$OpenOnly
)

$ErrorActionPreference = "Stop"

$XBrowserScript = "C:\Program Files\QClaw\v0.2.23.532\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs"
$BundledNode = "C:\Program Files\QClaw\v0.2.23.532\resources\node\node.exe"
$NodeBinary = if ($env:QCLAW_CLI_NODE_BINARY) {
    $env:QCLAW_CLI_NODE_BINARY
}
elseif (Test-Path $BundledNode) {
    $BundledNode
}
else {
    "node"
}
$SkipStatuses = @("成功")
$ProgressKeywords = @("更新点", "当前批次进度", "下一步优先核对", "待终核", "可入库", "数据抓取过程", "全量表", "TSV", "新增/拆出记录", "主要数值修改", "🟢", "🟡", "🔴")

function Invoke-XB {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)

    if (-not (Test-Path $XBrowserScript)) {
        throw "找不到 xbrowser 脚本: $XBrowserScript"
    }

    $raw = & $NodeBinary $XBrowserScript @Args
    if ($LASTEXITCODE -ne 0 -and [string]::IsNullOrWhiteSpace($raw)) {
        throw "xbrowser 执行失败: xb $($Args -join ' ')"
    }

    try {
        return ($raw | ConvertFrom-Json)
    }
    catch {
        throw "xbrowser 返回内容不是 JSON: $raw"
    }
}

function Invoke-XBRun {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$ActionArgs)

    $xbArgs = @("run", "--browser", $Browser) + $ActionArgs
    $result = Invoke-XB @xbArgs
    if (-not $result.ok) {
        $hint = if ($result.hint) { " 提示: $($result.hint)" } else { "" }
        $detail = ""
        if ($result.data -and $result.data.raw_error) {
            $detail = " 原始错误: $($result.data.raw_error)"
        }
        elseif ($result.data -and $result.data.result -and $result.data.result.error) {
            $detail = " 原始错误: $($result.data.result.error)"
        }
        elseif ($result.data -and $result.data.browser_running) {
            $detail = " 请先手动关闭 $Browser 浏览器窗口，然后重新运行。"
        }
        throw "xbrowser 操作失败: $($result.error)$hint$detail"
    }
    return $result.data.result
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
    Write-Host "初始化 xbrowser..." -ForegroundColor Yellow
    $init = Invoke-XB "init"

    if (-not $init.ok) {
        if ($init.error -like "*未安装*") {
            Write-Host "xbrowser 未安装，正在安装..." -ForegroundColor Yellow
            $setup = Invoke-XB "setup"
            if (-not $setup.ok) { throw "xbrowser 安装失败: $($setup.error)" }
            $init = Invoke-XB "init"
        }
    }

    if (-not $init.ok) {
        if ($init.error -like "*需要配置*" -or $init.hint -like "*guide config*") {
            if ($ConfigureXBrowserQuick) {
                Write-Host "按参数 -ConfigureXBrowserQuick 执行 xbrowser 快速配置..." -ForegroundColor Yellow
                $config = Invoke-XB "config" "reset"
                if (-not $config.ok) {
                    throw "xbrowser 快速配置失败: $($config.error) $($config.hint)"
                }
                $init = Invoke-XB "init"
            }
            else {
                throw @"
xbrowser 首次使用需要配置。

可选方式：
1. 快速开始：使用 QClaw 内置浏览器，干净环境，立即可用。
   运行：
   powershell -NoProfile -ExecutionPolicy Bypass -File "$PSCommandPath" -ConfigureXBrowserQuick -OpenOnly

2. 自定义设置：选择 Chrome / Edge / QQ 浏览器及显示模式。
   请在 QClaw 内部完成 xbrowser 配置引导后，再重新运行本脚本。
"@
            }
        }
    }

    if (-not $init.ok) {
        throw "xbrowser 初始化失败: $($init.error) $($init.hint)"
    }

    Write-Host "xbrowser 就绪。" -ForegroundColor Green
}

function Test-Prerequisites {
    Write-Host "检查目录和文件..." -ForegroundColor Yellow

    if (-not (Test-Path $InputDir)) { throw "输入目录不存在: $InputDir" }
    if (-not (Test-Path $RequirementPath)) { throw "requirement.md 不存在: $RequirementPath" }
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    }
    if ((-not (Test-Path $LogPath)) -or [string]::IsNullOrWhiteSpace((Get-Content -Path $LogPath -Raw -ErrorAction SilentlyContinue))) {
        "文件名,开始时间,结束时间,状态,发送次数,输出文件名,备注" | Set-Content -Path $LogPath -Encoding UTF8
    }
}

function Get-ProcessedFileSet {
    $set = New-Object "System.Collections.Generic.HashSet[string]"
    if (-not (Test-Path $LogPath)) { return ,$set }

    try {
        $rows = Import-Csv -Path $LogPath -Encoding UTF8
        foreach ($row in $rows) {
            $name = $row."文件名"
            if (-not $name) { $name = $row.FileName }
            $status = $row."状态"
            if (-not $status) { $status = $row.Status }
            if ($name -and ($status -in $SkipStatuses)) { [void]$set.Add($name) }
        }
    }
    catch {
        Write-Host "警告: log.csv 解析失败，将不跳过历史文件。$_" -ForegroundColor Yellow
    }

    return ,$set
}

function Get-OutputFilePath {
    param([string]$BaseName)

    $path = Join-Path $OutputDir "$BaseName`_result.md"
    $counter = 2
    while (Test-Path $path) {
        $path = Join-Path $OutputDir "$BaseName`_result_$counter.md"
        $counter++
    }
    return $path
}

function Add-LogEntry {
    param(
        [string]$FileName,
        [string]$StartTime,
        [string]$EndTime,
        [string]$Status,
        [int]$SendCount,
        [string]$OutputFile,
        [string]$Remarks
    )

    $line = '"{0}","{1}","{2}","{3}",{4},"{5}","{6}"' -f `
        ($FileName -replace '"', '""'),
        ($StartTime -replace '"', '""'),
        ($EndTime -replace '"', '""'),
        ($Status -replace '"', '""'),
        $SendCount,
        ((Split-Path $OutputFile -Leaf) -replace '"', '""'),
        ($Remarks -replace '"', '""')

    Add-Content -Path $LogPath -Value $line -Encoding UTF8
}

function Test-ContainsAny {
    param([string]$Text, [string[]]$Keywords)
    foreach ($keyword in $Keywords) {
        if ($Text -match [regex]::Escape($keyword)) { return $true }
    }
    return $false
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

function Test-FullTableRequestSignal {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) { return $false }

    $patterns = @(
        "(^|[\r\n。！？.!?；;：:])\s*(全部|所有|均|都)\s*可[入出]库\s*([。！？.!?；;]|$)",
        "(^|[\r\n。！？.!?；;：:])\s*全(?:部|量)?\s*记录\s*(均|都)?\s*可[入出]库\s*([。！？.!?；;]|$)",
        "(^|[\r\n。！？.!?；;：:])\s*无待核.*可[入出]库\s*([。！？.!?；;]|$)"
    )

    foreach ($pattern in $patterns) {
        if ($Text -match $pattern) { return $true }
    }

    return $false
}

function Get-TSVDataRowCountFromText {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) { return 0 }

    $lines = $Text -split "`r?`n"
    $headerPattern = "^主车型`t品牌`t分类`t结构`t版本`t代际`t年份`tmax_length_in`tmax_width_in \(w/o\)`tmax_height_in`t参考车型`t备注`t迭代状态\s*$"
    $inTable = $false
    $count = 0

    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ($trimmed -match $headerPattern) {
            $inTable = $true
            continue
        }
        if (-not $inTable) { continue }
        if ([string]::IsNullOrWhiteSpace($trimmed)) {
            if ($count -gt 0) { break }
            continue
        }
        if ($trimmed -like "---*") { break }
        if (($trimmed -split "`t").Count -ge 13) { $count++ }
    }

    return $count
}

function Get-TSVDataRowsFromText {
    param([string]$Text)

    $rows = @()
    if ([string]::IsNullOrWhiteSpace($Text)) { return $rows }

    $lines = $Text -split "`r?`n"
    $headerPattern = "^主车型`t品牌`t分类`t结构`t版本`t代际`t年份`tmax_length_in`tmax_width_in \(w/o\)`tmax_height_in`t参考车型`t备注`t迭代状态\s*$"
    $inTable = $false

    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ($trimmed -match $headerPattern) {
            $inTable = $true
            continue
        }
        if (-not $inTable) { continue }
        if ([string]::IsNullOrWhiteSpace($trimmed)) {
            if ($rows.Count -gt 0) { break }
            continue
        }
        if ($trimmed -like "---*") { break }

        $columns = $trimmed -split "`t"
        if ($columns.Count -ge 13) {
            $rows += [PSCustomObject]@{
                Year = [string]$columns[6]
                Reference = [string]$columns[10]
                Remarks = [string]$columns[11]
                Status = [string]$columns[12]
            }
        }
    }

    return $rows
}

function Test-YearRangeReferencesCovered {
    param([string]$Reply)

    $rows = @(Get-TSVDataRowsFromText -Text $Reply)
    foreach ($row in $rows) {
        $year = ([string]$row.Year).Trim()
        $reference = [string]$row.Reference
        if ($year -match "^\s*(\d{4})\s*-\s*(\d{4})\s*$") {
            $startYear = $Matches[1]
            $endYear = $Matches[2]
            $escapedStart = [regex]::Escape($startYear)
            $escapedEnd = [regex]::Escape($endYear)
            $hasExplicitRange = $reference -match "\b$escapedStart\s*-\s*$escapedEnd\b"
            $hasBothEndpoints = ($reference -match "\b$escapedStart\b") -and ($reference -match "\b$escapedEnd\b")
            if (-not ($hasExplicitRange -or $hasBothEndpoints)) { return $false }
        }
    }

    return $true
}

function Test-ReplyHasPendingRows {
    param([string]$Reply)

    $rows = @(Get-TSVDataRowsFromText -Text $Reply)
    foreach ($row in $rows) {
        $text = "$($row.Remarks) $($row.Status)"
        if ($text -match "待终核|待补强|待核|需继续|继续确认") { return $true }
    }

    return $false
}

function Test-ReplyContainsFullTable {
    param(
        [string]$Reply,
        [int]$MinimumRows
    )

    if ($MinimumRows -le 0) { return $true }
    return ((Get-TSVDataRowCountFromText -Text $Reply) -ge $MinimumRows)
}

function Test-ForceNextSignal {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) { return $false }

    $patterns = @(
        "回复\s*[：:]\s*下一步",
        '请(回复|发送)\s*[“"]?下一步[”"]?',
        "(^|[\r\n])\s*下一步[。.!！]?\s*$",
        "适合直接开始做完整全量表修复",
        "开始重构输出",
        "将按最新全量表格式开始",
        "我将按最新全量表格式开始重构输出"
    )

    foreach ($pattern in $patterns) {
        if ($Text -match $pattern) { return $true }
    }

    return $false
}

function Get-LevenshteinDistance {
    param([string]$Text1, [string]$Text2)

    $len1 = $Text1.Length
    $len2 = $Text2.Length
    $d = New-Object 'int[,]' ($len1 + 1), ($len2 + 1)

    for ($i = 0; $i -le $len1; $i++) { $d[$i, 0] = $i }
    for ($j = 0; $j -le $len2; $j++) { $d[0, $j] = $j }

    for ($i = 1; $i -le $len1; $i++) {
        for ($j = 1; $j -le $len2; $j++) {
            $cost = if ($Text1[$i - 1] -eq $Text2[$j - 1]) { 0 } else { 1 }
            $deleteCost = $d[($i - 1), $j] + 1
            $insertCost = $d[$i, ($j - 1)] + 1
            $replaceCost = $d[($i - 1), ($j - 1)] + $cost
            $d[$i, $j] = [Math]::Min([Math]::Min($deleteCost, $insertCost), $replaceCost)
        }
    }

    return $d[$len1, $len2]
}

function Get-TextSimilarity {
    param([string]$Text1, [string]$Text2)

    if ([string]::IsNullOrEmpty($Text1) -or [string]::IsNullOrEmpty($Text2)) { return 0.0 }
    $maxCompareLength = 6000
    if ($Text1.Length -gt $maxCompareLength) { $Text1 = $Text1.Substring($Text1.Length - $maxCompareLength) }
    if ($Text2.Length -gt $maxCompareLength) { $Text2 = $Text2.Substring($Text2.Length - $maxCompareLength) }
    $maxLen = [Math]::Max($Text1.Length, $Text2.Length)
    if ($maxLen -eq 0) { return 1.0 }
    return [Math]::Max(0.0, 1.0 - ((Get-LevenshteinDistance -Text1 $Text1 -Text2 $Text2) / $maxLen))
}

function Open-ChatGPT {
    Write-Host "打开 ChatGPT: $ChatGptUrl" -ForegroundColor Yellow
    $openArgs = @("run", "--browser", $Browser, "open", $ChatGptUrl)
    $openResult = Invoke-XB @openArgs

    if (-not $openResult.ok) {
        $rawError = ""
        if ($openResult.data -and $openResult.data.raw_error) {
            $rawError = [string]$openResult.data.raw_error
        }
        elseif ($openResult.data -and $openResult.data.result -and $openResult.data.result.error) {
            $rawError = [string]$openResult.data.result.error
        }

        $currentUrl = ""
        try {
            $urlResult = Invoke-XBRun "get" "url"
            $urlValue = Get-XBValue $urlResult
            if ($urlValue -and $urlValue.url) { $currentUrl = [string]$urlValue.url }
            else { $currentUrl = [string]$urlValue }
        }
        catch { }

        if ($currentUrl -notlike "https://chatgpt.com*") {
            if ($rawError -like "*ERR_ABORTED*") {
                Write-Host "open 返回 ERR_ABORTED，改用新标签页打开 ChatGPT..." -ForegroundColor Yellow
                Invoke-XBRun "tab" "new" $ChatGptUrl | Out-Null
            }
            else {
                $hint = if ($openResult.hint) { " 提示: $($openResult.hint)" } else { "" }
                throw "xbrowser 打开 ChatGPT 失败: $($openResult.error)$hint 原始错误: $rawError"
            }
        }
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
            Write-Host "  切回 ChatGPT 标签页..." -ForegroundColor Gray
            Invoke-XBRun "tab" ([string]$chatTab.index) | Out-Null
            Start-Sleep -Seconds 1
            return
        }
    }
    catch { }

    Write-Host "  当前没有 ChatGPT 标签页，重新打开..." -ForegroundColor Yellow
    Invoke-XBRun "tab" "new" $ChatGptUrl | Out-Null
    Start-Sleep -Seconds 3
    try { Invoke-XBRun "wait" "--load" "networkidle" | Out-Null } catch { }
}

function Get-ChatGPTState {
    Ensure-ChatGPTActive
    $script = @'
(() => {
  const textOf = el => (el && (el.innerText || el.textContent || el.value || '') || '').trim();
  const isVisible = el => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const findEditor = () => Array.from(document.querySelectorAll('#prompt-textarea, textarea, [contenteditable="true"], [role="textbox"]'))
    .find(el => isVisible(el) && !el.disabled && el.getAttribute('aria-disabled') !== 'true');
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
  const assistantTexts = assistantNodes.map(textOf).filter(t => t.length > 0);
  const reply = assistantTexts.length ? assistantTexts[assistantTexts.length - 1] : '';
  const editor = findEditor();
  const buttons = Array.from(document.querySelectorAll('button'));
  const buttonText = b => ((b.getAttribute('aria-label') || '') + ' ' + (b.innerText || '')).toLowerCase();
  const isGenerating = buttons.some(b => /stop|停止/.test(buttonText(b)) && !b.disabled && isVisible(b));
  const pageText = document.body.innerText || '';
  return {
    reply,
    inputReady: !!editor && !editor.disabled && editor.getAttribute('aria-disabled') !== 'true',
    isGenerating,
    hasStopButton: isGenerating,
    loggedOut: /log in|sign up|登录|注册/.test(pageText) && !editor,
    pageError: /something went wrong|network error|页面错误|网络错误|出错了/.test(pageText)
  };
})()
'@
    $result = Invoke-XBRun "eval" $script
    return (Get-XBValue $result)
}

function Focus-ChatGPTEditor {
    Ensure-ChatGPTActive
    $script = @'
(() => {
  const isVisible = el => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const editor = Array.from(document.querySelectorAll('#prompt-textarea, textarea, [contenteditable="true"], [role="textbox"]'))
    .find(el => isVisible(el) && !el.disabled && el.getAttribute('aria-disabled') !== 'true');
  if (!editor) return false;
  editor.focus();
  if (editor.scrollIntoView) editor.scrollIntoView({block: 'center'});
  return true;
})()
'@
    $focused = Get-XBValue (Invoke-XBRun "eval" $script)
    if (-not $focused) { throw "没有找到 ChatGPT 输入框，请确认已经登录并进入聊天页面。" }
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

function Get-ChatGPTEditorText {
    Ensure-ChatGPTActive
    $script = @'
(() => {
  const isVisible = el => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const editor = Array.from(document.querySelectorAll('#prompt-textarea, textarea, [contenteditable="true"], [role="textbox"]'))
    .find(el => isVisible(el) && !el.disabled && el.getAttribute('aria-disabled') !== 'true');
  if (!editor) return '';
  return (editor.value || editor.innerText || editor.textContent || '').trim();
})()
'@
    $text = Get-XBValue (Invoke-XBRun "eval" $script)
    return [string]$text
}

function Get-ChatGPTComposerState {
    Ensure-ChatGPTActive
    $script = @'
(() => {
  const isVisible = el => {
    if (!el) return false;
    const style = window.getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  };
  const textOf = el => (el && (el.innerText || el.textContent || el.value || '') || '').trim();
  const editor = Array.from(document.querySelectorAll('#prompt-textarea, textarea, [contenteditable="true"], [role="textbox"]'))
    .find(el => isVisible(el) && !el.disabled && el.getAttribute('aria-disabled') !== 'true');
  const editorText = textOf(editor);
  const buttons = Array.from(document.querySelectorAll('button'));
  const sendButton = buttons.find(b => {
    const t = ((b.getAttribute('aria-label') || '') + ' ' + (b.innerText || '') + ' ' + (b.getAttribute('data-testid') || '')).toLowerCase();
    return /(send|发送|submit)/.test(t);
  });
  const composer = editor ? (editor.closest('form') || editor.closest('[data-testid*="composer"]') || editor.closest('main') || document.body) : document.body;
  const composerText = textOf(composer);
  const attachmentLike = Array.from(document.querySelectorAll('[data-testid*="attachment"], [data-testid*="file"], [aria-label*="附件"], [aria-label*="文件"], [aria-label*="Remove"], [aria-label*="移除"], [class*="attachment"], [class*="file"]'));
  const hasAttachment = attachmentLike.length > 0 || /附件|已上传|上传完成|移除文件|remove file|\.txt|\.tsv|文本/.test(composerText);
  return {
    editorText,
    editorLength: editorText.length,
    composerText,
    composerLength: composerText.length,
    hasAttachment,
    sendEnabled: !!sendButton && !sendButton.disabled && sendButton.getAttribute('aria-disabled') !== 'true'
  };
})()
'@
    $state = Get-XBValue (Invoke-XBRun "eval" $script)
    return $state
}

function Set-ClipboardReliable {
    param([string]$Text)

    $lastError = $null
    for ($attempt = 1; $attempt -le 8; $attempt++) {
        try {
            Set-Clipboard -Value $Text
            return
        }
        catch {
            $lastError = $_.Exception.Message
            Start-Sleep -Milliseconds (250 * $attempt)
        }
    }

    try {
        Add-Type -AssemblyName System.Windows.Forms -ErrorAction SilentlyContinue
        [System.Windows.Forms.Clipboard]::SetText($Text)
        return
    }
    catch {
        throw "剪贴板写入失败: $lastError; fallback: $($_.Exception.Message)"
    }
}

function Wait-MessageAccepted {
    param(
        [string]$Message,
        [int]$TimeoutSeconds = 12
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        $state = Get-ChatGPTState
        $composerState = Get-ChatGPTComposerState
        $editorText = [string]$composerState.editorText

        if ($state.isGenerating) { return $true }
        if ([string]::IsNullOrWhiteSpace($editorText) -and -not $composerState.sendEnabled -and -not $composerState.hasAttachment) { return $true }
        if ($editorText.Trim() -ne $Message.Trim()) { return $true }

        Start-Sleep -Seconds 1
    }

    return $false
}

function Wait-EditorTextReady {
    param(
        [string]$ExpectedText,
        [switch]$LargePayload,
        [int]$TimeoutSeconds = 15
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $expectedTrimmed = $ExpectedText.Trim()
    $minimumLength = if ($LargePayload) { [Math]::Min(1000, [Math]::Max(100, [int]($expectedTrimmed.Length * 0.5))) } else { $expectedTrimmed.Length }

    while ((Get-Date) -lt $deadline) {
        $composerState = Get-ChatGPTComposerState
        $editorTrimmed = ([string]$composerState.editorText).Trim()

        if ($LargePayload) {
            if ($composerState.hasAttachment -or ($composerState.sendEnabled -and $editorTrimmed.Length -eq 0)) {
                return $true
            }
            if ($editorTrimmed.Length -ge $minimumLength -and $editorTrimmed.Contains("【任务要求】") -and $editorTrimmed.Contains("【TSV 数据】")) {
                return $true
            }
        }
        else {
            $composerTrimmed = ([string]$composerState.composerText).Trim()
            if ($editorTrimmed -eq $expectedTrimmed) {
                return $true
            }
            if ($editorTrimmed.Contains($expectedTrimmed) -or $composerTrimmed.Contains($expectedTrimmed)) {
                return $true
            }
            if ($composerState.sendEnabled) {
                return $true
            }
        }

        Start-Sleep -Seconds 1
    }

    return $false
}

function Start-ChatGPTNewConversation {
    Ensure-ChatGPTActive
    Write-Host "  新建 ChatGPT 对话..." -ForegroundColor Gray
    $script = @'
(() => {
  const textOf = el => (el && (el.innerText || el.textContent || el.getAttribute('aria-label') || '') || '').trim();
  const candidates = Array.from(document.querySelectorAll('a, button'));
  let match = candidates.find(el => {
    const text = textOf(el);
    return text === '新聊天' || text === 'New chat';
  });
  if (!match) {
    match = candidates.find(el => {
      const href = el.getAttribute && el.getAttribute('href');
      return href === '/' || href === '/?temporary-chat=false';
    });
  }
  if (!match) return false;
  match.click();
  return true;
})()
'@
    $clicked = Get-XBValue (Invoke-XBRun "eval" $script)
    if (-not $clicked) {
        Invoke-XBRun "tab" "new" $ChatGptUrl | Out-Null
    }
    Start-Sleep -Seconds 3
    try { Invoke-XBRun "wait" "--load" "networkidle" | Out-Null } catch { }
}

function Send-ChatGPTMessage {
    param(
        [string]$Message,
        [switch]$LargePayload
    )

    Focus-ChatGPTEditor
    $pasteAttempts = if ($LargePayload) { 4 } else { 3 }
    $pasted = $false

    for ($pasteAttempt = 1; $pasteAttempt -le $pasteAttempts; $pasteAttempt++) {
        Set-ClipboardReliable -Text $Message
        Start-Sleep -Seconds 1
        Focus-ChatGPTEditor
        Invoke-XBRun "press" "Control+A" | Out-Null
        Invoke-XBRun "press" "Control+V" | Out-Null

        $pasteWaitSeconds = if ($LargePayload) { [Math]::Max($LargePayloadDelay, 12) } else { 5 }
        if (Wait-EditorTextReady -ExpectedText $Message -LargePayload:$LargePayload -TimeoutSeconds $pasteWaitSeconds) {
            $pasted = $true
            break
        }

        Write-Host "  粘贴内容未确认，重试粘贴 ($pasteAttempt/$pasteAttempts)..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }

    if (-not $pasted) {
        $composerState = Get-ChatGPTComposerState
        throw "粘贴未确认，输入框长度: $($composerState.editorLength)，composer长度: $($composerState.composerLength)，附件状态: $($composerState.hasAttachment)，发送按钮可用: $($composerState.sendEnabled)，预期长度: $($Message.Length)"
    }

    if ($LargePayload) {
        Write-Host "  大文本已确认粘贴，等待 $LargePayloadDelay 秒后发送..." -ForegroundColor Gray
        Start-Sleep -Seconds $LargePayloadDelay
    }
    else {
        Start-Sleep -Seconds $OperationDelay
    }

    $maxSendAttempts = if ($LargePayload) { 4 } else { 3 }
    for ($attempt = 1; $attempt -le $maxSendAttempts; $attempt++) {
        Click-ChatGPTSendButton
        Start-Sleep -Seconds $OperationDelay

        $accepted = Wait-MessageAccepted -Message $Message -TimeoutSeconds 12
        if ($accepted) { return }

        Write-Host "  消息似乎未发出，重试发送 ($attempt/$maxSendAttempts)..." -ForegroundColor Yellow
        Focus-ChatGPTEditor
        Invoke-XBRun "press" "Enter" | Out-Null
        Start-Sleep -Seconds $OperationDelay

        $accepted = Wait-MessageAccepted -Message $Message -TimeoutSeconds 8
        if ($accepted) { return }
    }

    throw "消息未发出，输入框仍保留待发送内容: $($Message.Substring(0, [Math]::Min(40, $Message.Length)))"
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
        elseif ($reply.Length -gt 0 -and -not $state.isGenerating -and $state.inputReady -and $stableSince -and ((Get-Date) - $stableSince).TotalSeconds -ge $ReplyStabilityDelay) {
            Start-Sleep -Seconds $PostReplyDelay
            return @{ Ok = $true; Status = ""; Remark = ""; Reply = $reply }
        }
        elseif ($reply.Length -gt 0 -and -not $state.isGenerating -and $stableSince -and ((Get-Date) - $stableSince).TotalSeconds -ge ($ReplyStabilityDelay + 8)) {
            Start-Sleep -Seconds $PostReplyDelay
            return @{ Ok = $true; Status = ""; Remark = ""; Reply = $reply }
        }

        Start-Sleep -Seconds 2
    }

    return @{ Ok = $false; Status = "页面错误"; Remark = "等待回复超过 $MaxReplyWaitSeconds 秒"; Reply = $lastReply }
}

function Test-RepeatedReply {
    param([string]$Previous, [string]$Current)

    if ([string]::IsNullOrEmpty($Previous) -or [string]::IsNullOrEmpty($Current)) { return $false }
    $similarity = Get-TextSimilarity -Text1 $Previous -Text2 $Current
    $newChars = $Current.Length - $Previous.Length
    $hasNewProgress = (Test-ContainsAny -Text $Current -Keywords @("更新点", "新增/拆出记录", "主要数值修改")) -and (-not (Test-ContainsAny -Text $Previous -Keywords @("更新点", "新增/拆出记录", "主要数值修改")))
    return ($similarity -gt $SimilarityThreshold -and $newChars -lt $MinNewChars -and -not $hasNewProgress)
}

function Test-DeviatedReply {
    param([string]$Reply, [int]$Round)

    if (Test-ContainsAny -Text $Reply -Keywords $ProgressKeywords) { return $false }
    if (Test-CompletionSignal -Text $Reply) { return $false }
    if ($Round -le 2) { return $false }
    if ($Reply.Length -lt 50) { return $false }
    return $true
}

function Process-TSVFile {
    param([System.IO.FileInfo]$TSVFile)

    $fileName = $TSVFile.Name
    $startTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $sendCount = 0
    $nextCount = 0
    $round = 1
    $previousReply = ""
    $requestedFullTable = $false
    $minimumFullTableRows = 0
    $status = ""
    $remarks = ""
    $outputFile = Get-OutputFilePath -BaseName $TSVFile.BaseName

    Write-Host "`n处理文件: $fileName" -ForegroundColor Cyan
    "# 文件名：$fileName`r`n" | Set-Content -Path $outputFile -Encoding UTF8

    try {
        Start-ChatGPTNewConversation

        $requirementContent = Get-Content $RequirementPath -Raw -Encoding UTF8
        $tsvContent = Get-Content $TSVFile.FullName -Raw -Encoding UTF8
        $minimumFullTableRows = [Math]::Max(0, (@($tsvContent -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count - 1))
        $message = @"
【任务要求】
$requirementContent

【当前文件名】
$fileName

【TSV 数据】
$tsvContent
"@

        Send-ChatGPTMessage -Message $message -LargePayload
        $sendCount++

        while ($true) {
            Write-Host "  等待第 $round 轮回复完成..." -ForegroundColor Gray
            $wait = Wait-ChatGPTReplyComplete
            $reply = [string]$wait.Reply

            $roundTitle = if ($round -eq 1) { "--- Round 1 / 首次发送 ---" } else { "--- Round $round / 下一步 ---" }
            Add-Content -Path $outputFile -Value "`r`n$roundTitle`r`n$reply`r`n" -Encoding UTF8

            if (-not $wait.Ok) {
                $status = $wait.Status
                $remarks = $wait.Remark
                break
            }

            if (Test-ForceNextSignal -Text $reply) {
                Write-Host "  检测到继续信号，发送 下一步..." -ForegroundColor Yellow
                if ($nextCount -ge $MaxNextSteps) {
                    $status = "次数上限终止"
                    $remarks = "达到最大下一步次数: $MaxNextSteps"
                    break
                }
                $previousReply = $reply
                $nextCount++
                $round++
                Send-ChatGPTMessage -Message "下一步"
                $sendCount++
                continue
            }

            $hasFullTable = Test-ReplyContainsFullTable -Reply $reply -MinimumRows $minimumFullTableRows
            $hasCoveredYearRefs = Test-YearRangeReferencesCovered -Reply $reply
            $hasPendingRows = Test-ReplyHasPendingRows -Reply $reply

            if ((Test-FullTableRequestSignal -Text $reply) -and ((-not $hasFullTable) -or (-not $hasCoveredYearRefs) -or $hasPendingRows)) {
                Write-Host "  检测到全部/所有可入库，但完整表或年份参考覆盖不足，发送完整全量表请求..." -ForegroundColor Yellow
                if ($nextCount -ge $MaxNextSteps) {
                    $status = "次数上限终止"
                    $remarks = "达到最大下一步次数: $MaxNextSteps"
                    break
                }
                $requestedFullTable = $true
                $previousReply = $reply
                $nextCount++
                $round++
                Send-ChatGPTMessage -Message "给我当前批次更新后的完整可替换 TSV。必须包含未变更、已修改、新增/拆分后的全部记录；不要只给变化部分或摘要。年份是范围时，参考车型必须覆盖起止年份，例如 2002-2004 Audi A6 Avant，不能只写 2002 Audi A6 Avant。仍有待终核/待补强行时不要说完成，请继续补强。表格后单独输出：本批次完成。"
                $sendCount++
                continue
            }

            if (Test-CompletionSignal -Text $reply) {
                if ($hasFullTable -and $hasCoveredYearRefs -and (-not $hasPendingRows)) {
                    $status = "成功"
                    $remarks = "检测到明确批次完成信号且包含完整表"
                    break
                }

                Write-Host "  检测到完成信号，但表格不完整、年份参考覆盖不足或仍有待补强行，继续请求完整全量表..." -ForegroundColor Yellow
                if ($nextCount -ge $MaxNextSteps) {
                    $status = "次数上限终止"
                    $remarks = "完成信号未附完整表、年份参考覆盖不足或仍有待补强行，且达到最大下一步次数: $MaxNextSteps"
                    break
                }
                $requestedFullTable = $true
                $previousReply = $reply
                $nextCount++
                $round++
                Send-ChatGPTMessage -Message "你刚才给了完成信号，但当前批次完整可替换 TSV 不完整、年份范围行的参考车型没有覆盖起止年份，或仍有待终核/待补强行。请继续补强；只有全部行都可入库时，才输出当前批次更新后的完整可替换 TSV。年份是 2002-2004 这类范围时，参考车型必须类似 2002-2004 Audi A6 Avant 或同时包含 2002 和 2004，不能只写 2002。最终表格后单独输出：本批次完成。"
                $sendCount++
                continue
            }

            if (Test-RepeatedReply -Previous $previousReply -Current $reply) {
                $status = "重复终止"
                $remarks = "连续两轮回复高度相似，疑似未继续推进"
                break
            }

            if ($nextCount -ge $MaxNextSteps) {
                $status = "次数上限终止"
                $remarks = "达到最大下一步次数: $MaxNextSteps"
                break
            }

            if (Test-DeviatedReply -Reply $reply -Round $round) {
                $status = "偏离终止"
                $remarks = "回复缺少 TSV / 更新点 / 当前进度 / 下一步方向等正常推进信号"
                break
            }

            $previousReply = $reply
            $nextCount++
            $round++

            Write-Host "  继续发送 下一步 ($nextCount/$MaxNextSteps)..." -ForegroundColor Yellow
            Send-ChatGPTMessage -Message "下一步"
            $sendCount++
        }
    }
    catch {
        $status = "页面错误"
        $remarks = "异常: $($_.Exception.Message)"
        Add-Content -Path $outputFile -Value "`r`n--- 脚本异常 ---`r`n$remarks`r`n" -Encoding UTF8
    }

    $endTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-LogEntry -FileName $fileName -StartTime $startTime -EndTime $endTime -Status $status -SendCount $sendCount -OutputFile $outputFile -Remarks $remarks
    Write-Host "完成: $fileName -> $status ($remarks)" -ForegroundColor $(if ($status -eq "成功") { "Green" } else { "Yellow" })
}

function Generate-Summary {
    $rows = @()
    try { $rows = @(Import-Csv -Path $LogPath -Encoding UTF8) } catch { }

    $count = @{
        "成功" = 0
        "重复终止" = 0
        "次数上限终止" = 0
        "页面错误" = 0
        "登录失效" = 0
        "偏离终止" = 0
    }

    foreach ($row in $rows) {
        $status = $row."状态"
        if (-not $status) { $status = $row.Status }
        if ($count.ContainsKey($status)) { $count[$status]++ }
    }

    $failed = $count["重复终止"] + $count["次数上限终止"] + $count["页面错误"] + $count["登录失效"] + $count["偏离终止"]
    $summary = @"
总文件数：$($rows.Count)
成功数：$($count["成功"])
重复终止数：$($count["重复终止"])
次数上限终止数：$($count["次数上限终止"])
页面错误数：$($count["页面错误"])
登录失效数：$($count["登录失效"])
偏离终止数：$($count["偏离终止"])
失败数：$failed
输出目录：$OutputDir
完成时间：$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

    Set-Content -Path $SummaryPath -Value $summary -Encoding UTF8
}

function Main {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "qclaw 全量表补强自动化" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan

    Test-Prerequisites
    Initialize-XBrowser
    Open-ChatGPT

    if ($OpenOnly) {
        Write-Host "已打开 ChatGPT。请登录完成后重新运行脚本开始处理。" -ForegroundColor Yellow
        return
    }

    $state = Get-ChatGPTState
    if ($state.loggedOut -or -not $state.inputReady) {
        Write-Host "ChatGPT 当前不可输入。请在打开的浏览器里登录，并进入可发送消息的页面后再运行脚本。" -ForegroundColor Red
        exit 1
    }

    $tsvFiles = @(Get-ChildItem -Path $InputDir -Filter "*.tsv" | Sort-Object Name)
    if ($OnlyFiles.Count -gt 0) {
        $onlySet = New-Object "System.Collections.Generic.HashSet[string]" ([StringComparer]::OrdinalIgnoreCase)
        foreach ($onlyFile in $OnlyFiles) {
            foreach ($onlyFilePart in ($onlyFile -split ",")) {
                $trimmed = $onlyFilePart.Trim()
                if (-not $trimmed) { continue }
                $name = if ($trimmed.EndsWith(".tsv", [StringComparison]::OrdinalIgnoreCase)) { $trimmed } else { "$trimmed.tsv" }
                [void]$onlySet.Add($name)
            }
        }
        $tsvFiles = @($tsvFiles | Where-Object { $onlySet.Contains($_.Name) })
    }
    $processedSet = New-Object "System.Collections.Generic.HashSet[string]"
    if ($OnlyFiles.Count -eq 0) {
        $processedSet = Get-ProcessedFileSet
    }
    Write-Host "找到 $($tsvFiles.Count) 个 TSV 文件。" -ForegroundColor Green

    foreach ($tsvFile in $tsvFiles) {
        if ($processedSet.Contains($tsvFile.Name)) {
            Write-Host "跳过已处理文件: $($tsvFile.Name)" -ForegroundColor Gray
            continue
        }

        Process-TSVFile -TSVFile $tsvFile
        Start-Sleep -Seconds 5
    }

    Generate-Summary
    Write-Host "`n全部处理完成。汇总文件: $SummaryPath" -ForegroundColor Green
}

Main
