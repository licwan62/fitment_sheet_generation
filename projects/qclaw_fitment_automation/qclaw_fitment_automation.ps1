# qclaw 全量表补强自动化脚本
# 通过 QClaw xbrowser 控制 ChatGPT 网页版，遍历 TSV，多轮发送“下一步”，保存结果。

[CmdletBinding(PositionalBinding = $false)]
param(
    [Alias("project_dir", "project-dir")]
    [string]$Project = "",
    [Alias("input_dir", "input-dir")]
    [string]$InputDir = "",
    [Alias("output_dir", "output-dir")]
    [string]$OutputDir = "",
    [Alias("log_path", "log-path")]
    [string]$LogPath = "",
    [Alias("summary_path", "summary-path")]
    [string]$SummaryPath = "",
    [Alias("requirement_path", "requirement-path")]
    [string]$RequirementPath = "",
    [string]$ChatGptUrl = "https://chatgpt.com/",
    [string]$Browser = "openclaw",
    [string]$OpenClawCommand = "openclaw.cmd",
    [string]$OpenClawConfigPath = "",
    [string]$OpenClawGatewayUrl = "",
    [string]$OpenClawBrowserUrl = "",
    [Alias("MaxRounds", "max-rounds", "max_rounds")]
    [int]$MaxNextSteps = 30,
    [int]$ReplyStabilityDelay = 10,
    [int]$OperationDelay = 2,
    [int]$LargePayloadDelay = 8,
    [int]$PostReplyDelay = 2,
    [int]$MaxReplyWaitSeconds = 900,
    [int]$StuckGeneratingGraceSeconds = 35,
    [int]$XBrowserRetryCount = 2,
    [int]$XBrowserRecoverDelay = 3,
    [double]$SimilarityThreshold = 0.95,
    [int]$MinNewChars = 100,
    [string[]]$OnlyFiles = @(),
    [switch]$ConfigureXBrowserQuick,
    [switch]$OpenOnly,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs = @()
)

$ErrorActionPreference = "Stop"

$ExplicitParameters = New-Object "System.Collections.Generic.HashSet[string]" ([StringComparer]::OrdinalIgnoreCase)
foreach ($key in $PSBoundParameters.Keys) {
    if ($key -ne "ExtraArgs") { [void]$ExplicitParameters.Add($key) }
}

$ScriptRoot = if (-not [string]::IsNullOrWhiteSpace($PSScriptRoot)) {
    $PSScriptRoot
}
elseif (-not [string]::IsNullOrWhiteSpace($PSCommandPath)) {
    Split-Path -Parent $PSCommandPath
}
else {
    (Get-Location).Path
}

function Set-ArgumentValue {
    param(
        [string]$Name,
        [string]$Value
    )

    $normalized = ($Name.TrimStart("-") -replace "-", "_").ToLowerInvariant()
    switch ($normalized) {
        "project" { $script:Project = $Value; [void]$script:ExplicitParameters.Add("Project") }
        "project_dir" { $script:Project = $Value; [void]$script:ExplicitParameters.Add("Project") }
        "input_dir" { $script:InputDir = $Value; [void]$script:ExplicitParameters.Add("InputDir") }
        "inputdir" { $script:InputDir = $Value; [void]$script:ExplicitParameters.Add("InputDir") }
        "output_dir" { $script:OutputDir = $Value; [void]$script:ExplicitParameters.Add("OutputDir") }
        "outputdir" { $script:OutputDir = $Value; [void]$script:ExplicitParameters.Add("OutputDir") }
        "log_path" { $script:LogPath = $Value; [void]$script:ExplicitParameters.Add("LogPath") }
        "logpath" { $script:LogPath = $Value; [void]$script:ExplicitParameters.Add("LogPath") }
        "summary_path" { $script:SummaryPath = $Value; [void]$script:ExplicitParameters.Add("SummaryPath") }
        "summarypath" { $script:SummaryPath = $Value; [void]$script:ExplicitParameters.Add("SummaryPath") }
        "requirement_path" { $script:RequirementPath = $Value; [void]$script:ExplicitParameters.Add("RequirementPath") }
        "requirementpath" { $script:RequirementPath = $Value; [void]$script:ExplicitParameters.Add("RequirementPath") }
        "max_rounds" { $script:MaxNextSteps = [int]$Value; [void]$script:ExplicitParameters.Add("MaxNextSteps") }
        "maxrounds" { $script:MaxNextSteps = [int]$Value; [void]$script:ExplicitParameters.Add("MaxNextSteps") }
        "max_next_steps" { $script:MaxNextSteps = [int]$Value; [void]$script:ExplicitParameters.Add("MaxNextSteps") }
        "only_files" { $script:OnlyFiles = @($Value -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ }); [void]$script:ExplicitParameters.Add("OnlyFiles") }
        "onlyfiles" { $script:OnlyFiles = @($Value -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ }); [void]$script:ExplicitParameters.Add("OnlyFiles") }
        "open_only" { $script:OpenOnly = [switch]::Present; [void]$script:ExplicitParameters.Add("OpenOnly") }
        "openonly" { $script:OpenOnly = [switch]::Present; [void]$script:ExplicitParameters.Add("OpenOnly") }
        default { throw "未知参数: $Name" }
    }
}

function Read-GnuStyleArguments {
    if (-not $ExtraArgs -or $ExtraArgs.Count -eq 0) { return }

    for ($i = 0; $i -lt $ExtraArgs.Count; $i++) {
        $name = $ExtraArgs[$i]
        if (-not $name.StartsWith("-")) {
            throw "无法识别的位置参数: $name"
        }

        $normalized = ($name.TrimStart("-") -replace "-", "_").ToLowerInvariant()
        $isSwitch = $normalized -in @("open_only", "openonly")
        if ($isSwitch) {
            Set-ArgumentValue -Name $name -Value "true"
            continue
        }

        if ($i + 1 -ge $ExtraArgs.Count -or $ExtraArgs[$i + 1].StartsWith("-")) {
            throw "参数 $name 缺少值"
        }

        Set-ArgumentValue -Name $name -Value $ExtraArgs[$i + 1]
        $i++
    }
}

function Set-DefaultPaths {
    if ([string]::IsNullOrWhiteSpace($InputDir)) { $script:InputDir = Join-Path $ScriptRoot "input_sheets" }
    if ([string]::IsNullOrWhiteSpace($OutputDir)) { $script:OutputDir = Join-Path $ScriptRoot "output_sheets" }
    if ([string]::IsNullOrWhiteSpace($LogPath)) { $script:LogPath = Join-Path $ScriptRoot "log.csv" }
    if ([string]::IsNullOrWhiteSpace($SummaryPath)) { $script:SummaryPath = Join-Path $ScriptRoot "summary.txt" }
    if ([string]::IsNullOrWhiteSpace($RequirementPath)) { $script:RequirementPath = Join-Path $ScriptRoot "requirements\eu_autodata.md" }
}

function Resolve-ProjectPaths {
    if ([string]::IsNullOrWhiteSpace($Project)) { return }

    $projectRoot = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Project)
    if (-not $ExplicitParameters.Contains("InputDir")) { $script:InputDir = Join-Path $projectRoot "input" }
    if (-not $ExplicitParameters.Contains("OutputDir")) { $script:OutputDir = Join-Path $projectRoot "output" }
    if (-not $ExplicitParameters.Contains("LogPath")) { $script:LogPath = Join-Path $projectRoot "log.csv" }
    if (-not $ExplicitParameters.Contains("SummaryPath")) { $script:SummaryPath = Join-Path $projectRoot "summary.txt" }
}

Read-GnuStyleArguments
Set-DefaultPaths
Resolve-ProjectPaths

$OpenClawConfig = $null
$OpenClawAuthToken = ""
$OpenClawTargetId = ""
$OpenClawResolvedCommand = ""
$SkipStatuses = @("成功")
$InputFilePattern = if ($env:FITMENT_INPUT_PATTERN) { $env:FITMENT_INPUT_PATTERN } else { "*.tsv" }
$InputFileOrder = if ($env:FITMENT_INPUT_ORDER) { $env:FITMENT_INPUT_ORDER } else { "name_asc" }
$SkipProcessedFiles = ($env:FITMENT_SKIP_PROCESSED -ne "false")
$ProgressKeywords = @("更新点", "当前批次进度", "下一步优先处理", "下一步优先补缺失", "下一步优先核对", "待终核", "可入库", "数据抓取过程", "全量表", "TSV", "新增/拆出记录", "主要数值修改", "🟢", "🟡", "🔴")
$RequiredTsvHeader = if ($env:FITMENT_TSV_HEADER) { $env:FITMENT_TSV_HEADER } else { "主车型`t年份区间`t结构`t对应尺码`t品牌`t前台车型`t排序依据车型`t子车系`t分类`t版本`t门数`t代际`t区间最小年份`t区间最大年份`tmax_length_in`tmax_width_in`tmax_height_in`tmax_length_cm`tmax_width_cm`tmax_height_cm`t驾驶室类型`t货斗长度_ft`t长度余量`t无尺码原因`t参考车型`t备注`t迭代状态" }
$SubseriesEnabled = ($env:FITMENT_SUBSERIES_ENABLED -ne "false")
$RequiredSubseriesMatchHeader = if ($env:FITMENT_SUBSERIES_HEADER) { $env:FITMENT_SUBSERIES_HEADER } else { "Year`t主车型`t结构`t版本`t候选车型`t匹配数量" }
$AutoEmptyColumns = if ($env:FITMENT_AUTO_EMPTY_COLUMNS_DEFINED -eq "true") { [string]$env:FITMENT_AUTO_EMPTY_COLUMNS } elseif ($env:FITMENT_AUTO_EMPTY_COLUMNS) { $env:FITMENT_AUTO_EMPTY_COLUMNS } else { "对应尺码、排序依据车型、子车系、区间最小年份、区间最大年份、max_length_cm、max_width_cm、max_height_cm、长度余量、无尺码原因" }
$SubseriesAutoEmptyColumns = if ($env:FITMENT_SUBSERIES_AUTO_EMPTY_COLUMNS_DEFINED -eq "true") { [string]$env:FITMENT_SUBSERIES_AUTO_EMPTY_COLUMNS } elseif ($env:FITMENT_SUBSERIES_AUTO_EMPTY_COLUMNS) { $env:FITMENT_SUBSERIES_AUTO_EMPTY_COLUMNS } else { "匹配数量" }
$ExtraDataInstructions = if ($env:FITMENT_DATA_INSTRUCTIONS) { $env:FITMENT_DATA_INSTRUCTIONS } else { "" }
$AutoEmptyReminder = if ($AutoEmptyColumns) { "以下自动字段必须保留列但值留空：$AutoEmptyColumns。" } else { "" }
$SubseriesReminder = if ($SubseriesEnabled) { "另需维护子车系匹配表，表头固定为：$RequiredSubseriesMatchHeader；以下自动字段必须保留列但值留空：$SubseriesAutoEmptyColumns。" } else { "不要输出子车系匹配表。" }
$HeaderReminder = "全量 TSV 表头必须严格使用 requirement 指定的字段顺序：$RequiredTsvHeader。$AutoEmptyReminder$SubseriesReminder$ExtraDataInstructions"
$PhaseOrderReminder = '执行顺序必须固定为：第一阶段先解决数据缺失，优先补齐缺失年份、缺失结构/版本/门数/驾驶室/货斗、缺失尺寸、缺失参考车型等会阻塞成表的数据；第二阶段才解决核对问题，逐年核对参考车型覆盖、尺寸口径和迭代状态。只要仍存在任何数据缺失，不要把主要精力转到核对问题，也不要写全部可入库或本批次完成。回复中的下一步方向请按阶段写：有缺失时写“下一步优先补缺失”，缺失已补齐后再写“下一步优先核对”。'
$SubseriesOutputItem = if ($SubseriesEnabled) { "；4) 本轮更新后的子车系匹配表" } else { "" }
$ContinueMessage = '继续补强当前批次，并严格按以下格式回复：1) 更新点；2) 当前批次进度；3) 本轮更新后的全量 TSV（必须是真正更新过的 TSV，不能只写计划或说明，' + $HeaderReminder + '）' + $SubseriesOutputItem + '；5) 下一步优先处理（有数据缺失时必须写下一步优先补缺失，缺失补齐后再写下一步优先核对）；6) 若仍未完成，在末尾单独输出：下一步。' + $PhaseOrderReminder + '不要新增当前 TSV 范围外的年代、代际或车型行；拆分后的年份合集不得超出原记录年份范围；最终 TSV 顺序必须保持当前 split 第一条到最后一条的边界。不要只描述这一轮将要做什么而不给 TSV，不要连续重复上一轮内容。'
$MissingSignalsMessage = '你的上一轮回复缺少正常推进信号。请立刻继续当前批次，并严格补齐以下内容：更新点、当前批次进度、本轮更新后的全量 TSV' + $(if ($SubseriesEnabled) { "、本轮更新后的子车系匹配表" } else { "" }) + '、下一步优先处理；如果还没完成，末尾单独输出：下一步。不得只给说明、计划、摘要或重复上一轮文本，必须给一个更新过的全量 TSV。' + $PhaseOrderReminder + $HeaderReminder
$FullTableRequestMessage = '给我当前批次更新后的完整可替换全量 TSV' + $(if ($SubseriesEnabled) { "，并给出子车系匹配表" } else { "" }) + '。全量 TSV 必须包含未变更、已修改、在当前记录年份范围内拆分后的全部记录；不要只给变化部分、摘要或说明。若仍有数据缺失，先继续补缺失，不要提前转为最终核对或完成。不要新增当前 TSV 范围外的年代、代际或车型行，输出顺序必须保持当前 split 第一条到最后一条的边界。' + $PhaseOrderReminder + $HeaderReminder
$CompletionFixMessage = '你刚才给了完成信号，但当前回复没有可直接入库的完整全量 TSV' + $(if ($SubseriesEnabled) { "、缺少子车系匹配表" } else { "" }) + '，或仍可能存在未先解决的数据缺失。若本批次其实还没完成，请先补齐数据缺失，再做核对，并带上：更新点、当前批次进度、本轮更新后的全量 TSV' + $(if ($SubseriesEnabled) { "、本轮更新后的子车系匹配表" } else { "" }) + '、下一步优先处理，并在末尾单独输出：下一步。' + $PhaseOrderReminder + $HeaderReminder

function Invoke-XB {
    param([Parameter(ValueFromRemainingArguments = $true)][string[]]$Args)

    if (-not $Args -or $Args.Count -eq 0) { throw "OpenClaw 浏览器命令为空" }

    $command = $Args[0]
    if ($command -eq "init") {
        Initialize-OpenClawRuntime
        $status = Invoke-OpenClawBrowserHttp -Method "GET" -Path "/"
        if (-not $status.enabled) {
            return [pscustomobject]@{ ok = $false; error = "OpenClaw browser 未启用"; hint = "请启用 browser.enabled 和 browser 插件" }
        }
        Invoke-OpenClawBrowserHttp -Method "POST" -Path "/start" | Out-Null
        Set-OpenClawTargetFromTabs
        return New-XBSuccess -Result $status
    }

    if ($command -eq "cleanup") {
        Initialize-OpenClawRuntime
        $result = Invoke-OpenClawBrowserHttp -Method "POST" -Path "/stop"
        $script:OpenClawTargetId = ""
        return New-XBSuccess -Result $result
    }

    if ($command -ne "run") {
        return [pscustomobject]@{ ok = $false; error = "不支持的 OpenClaw 兼容命令: $command"; hint = "脚本已不再使用 QClaw xbrowser" }
    }

    $actionArgs = @($Args[1..($Args.Count - 1)])
    if ($actionArgs.Count -ge 2 -and $actionArgs[0] -eq "--browser") {
        $script:Browser = $actionArgs[1]
        $actionArgs = if ($actionArgs.Count -gt 2) { @($actionArgs[2..($actionArgs.Count - 1)]) } else { @() }
    }
    if ($actionArgs.Count -eq 0) { throw "OpenClaw 浏览器 action 为空" }

    Initialize-OpenClawRuntime
    $action = $actionArgs[0]
    switch ($action) {
        "open" {
            $result = Invoke-OpenClawBrowserHttp -Method "POST" -Path "/tabs/open" -Body @{ url = [string]$actionArgs[1] }
            $script:OpenClawTargetId = [string]$result.targetId
            return New-XBSuccess -Result $result
        }
        "get" {
            if ($actionArgs.Count -lt 2 -or $actionArgs[1] -ne "url") { throw "不支持的 get 命令" }
            return New-XBSuccess -Result (Invoke-OpenClawEvaluate -Expression "(() => location.href)()")
        }
        "tab" {
            if ($actionArgs.Count -eq 1) { return New-XBSuccess -Result (Get-OpenClawTabs) }
            if ($actionArgs[1] -eq "new") {
                $url = if ($actionArgs.Count -gt 2) { [string]$actionArgs[2] } else { "about:blank" }
                $result = Invoke-OpenClawBrowserHttp -Method "POST" -Path "/tabs/open" -Body @{ url = $url }
                $script:OpenClawTargetId = [string]$result.targetId
                return New-XBSuccess -Result $result
            }
            $index = [int]$actionArgs[1]
            $tabs = @((Get-OpenClawTabs).tabs)
            if ($index -lt 0 -or $index -ge $tabs.Count) { throw "OpenClaw 标签页索引超出范围: $index" }
            $selectedTab = $tabs[$index]
            $result = Invoke-OpenClawBrowserHttp -Method "POST" -Path "/tabs/focus" -Body @{ targetId = [string]$selectedTab.targetId }
            $script:OpenClawTargetId = [string]$selectedTab.targetId
            return New-XBSuccess -Result $result
        }
        "wait" {
            $deadline = (Get-Date).AddSeconds(20)
            do {
                try {
                    $readyState = [string](Invoke-OpenClawEvaluate -Expression "(() => document.readyState)()")
                    if ($readyState -in @("interactive", "complete")) { break }
                }
                catch { }
                Start-Sleep -Milliseconds 300
            } while ((Get-Date) -lt $deadline)
            return New-XBSuccess -Result ([pscustomobject]@{ success = $true })
        }
        "eval" { return New-XBSuccess -Result (Invoke-OpenClawEvaluate -Expression ([string]$actionArgs[1])) }
        "press" {
            Invoke-OpenClawKeyPress -Key ([string]$actionArgs[1])
            return New-XBSuccess -Result ([pscustomobject]@{ success = $true })
        }
        default { throw "不支持的 OpenClaw 浏览器 action: $action" }
    }
}

function New-XBSuccess {
    param($Result)
    return [pscustomobject]@{ ok = $true; data = [pscustomobject]@{ result = $Result } }
}

function Test-LocalTcpPort {
    param([string]$HostName, [int]$Port, [int]$TimeoutMs = 500)
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $task = $client.ConnectAsync($HostName, $Port)
        return $task.Wait($TimeoutMs) -and $client.Connected
    }
    catch { return $false }
    finally { $client.Dispose() }
}

function Initialize-OpenClawRuntime {
    if (-not [string]::IsNullOrWhiteSpace($script:OpenClawAuthToken) -and
        -not [string]::IsNullOrWhiteSpace($script:OpenClawBrowserUrl) -and
        (Test-LocalTcpPort -HostName ([uri]$script:OpenClawBrowserUrl).Host -Port ([uri]$script:OpenClawBrowserUrl).Port)) { return }

    if ([string]::IsNullOrWhiteSpace($script:OpenClawResolvedCommand)) {
        $commandInfo = Get-Command $OpenClawCommand -ErrorAction SilentlyContinue
        if (-not $commandInfo) { throw "找不到 OpenClaw 命令: $OpenClawCommand。请先确认 openclaw --version 可用。" }
        $script:OpenClawResolvedCommand = $commandInfo.Source
    }

    if ([string]::IsNullOrWhiteSpace($script:OpenClawConfigPath)) {
        $script:OpenClawConfigPath = if ($env:OPENCLAW_CONFIG_PATH) { $env:OPENCLAW_CONFIG_PATH } else { Join-Path $HOME ".openclaw\openclaw.json" }
    }
    if (-not (Test-Path -LiteralPath $script:OpenClawConfigPath)) { throw "找不到 OpenClaw 配置: $($script:OpenClawConfigPath)" }

    $script:OpenClawConfig = Get-Content -LiteralPath $script:OpenClawConfigPath -Raw | ConvertFrom-Json
    $script:OpenClawAuthToken = if ($env:OPENCLAW_GATEWAY_TOKEN) { $env:OPENCLAW_GATEWAY_TOKEN } else { [string]$script:OpenClawConfig.gateway.auth.token }
    if ([string]::IsNullOrWhiteSpace($script:OpenClawAuthToken)) { throw "OpenClaw gateway.auth.token 未配置" }

    $gatewayPort = if ($script:OpenClawConfig.gateway.port) { [int]$script:OpenClawConfig.gateway.port } else { 18789 }
    if ([string]::IsNullOrWhiteSpace($script:OpenClawGatewayUrl)) { $script:OpenClawGatewayUrl = "http://127.0.0.1:$gatewayPort" }
    if ([string]::IsNullOrWhiteSpace($script:OpenClawBrowserUrl)) { $script:OpenClawBrowserUrl = "http://127.0.0.1:$($gatewayPort + 2)" }

    $gatewayUri = [uri]$script:OpenClawGatewayUrl
    $browserUri = [uri]$script:OpenClawBrowserUrl
    if (-not (Test-LocalTcpPort -HostName $gatewayUri.Host -Port $gatewayUri.Port)) {
        Write-Host "OpenClaw Gateway 未运行，正在后台启动..." -ForegroundColor Yellow
        $oldEager = $env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER
        try {
            $env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER = "1"
            Start-Process -FilePath $script:OpenClawResolvedCommand -ArgumentList @("gateway", "run") -WindowStyle Hidden | Out-Null
        }
        finally {
            if ($null -eq $oldEager) { Remove-Item Env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER -ErrorAction SilentlyContinue }
            else { $env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER = $oldEager }
        }
        for ($i = 0; $i -lt 40; $i++) {
            if (Test-LocalTcpPort -HostName $browserUri.Host -Port $browserUri.Port) { break }
            Start-Sleep -Milliseconds 500
        }
    }
    elseif (-not (Test-LocalTcpPort -HostName $browserUri.Host -Port $browserUri.Port)) {
        Restart-LocalOpenClawGatewayWithBrowser
        for ($i = 0; $i -lt 40; $i++) {
            if (Test-LocalTcpPort -HostName $browserUri.Host -Port $browserUri.Port) { break }
            Start-Sleep -Milliseconds 500
        }
    }

    if (-not (Test-LocalTcpPort -HostName $browserUri.Host -Port $browserUri.Port)) {
        throw "OpenClaw Gateway 已运行，但 browser control 服务未启动。请重启 Gateway，或设置 OPENCLAW_EAGER_BROWSER_CONTROL_SERVER=1 后再启动。"
    }
}

function Restart-LocalOpenClawGatewayWithBrowser {
    $gatewayUri = [uri]$script:OpenClawGatewayUrl
    if ($gatewayUri.Host -notin @("127.0.0.1", "localhost", "::1")) {
        throw "远程 OpenClaw Gateway 未暴露 browser control 服务，无法由本脚本重启: $gatewayUri"
    }

    $connection = Get-NetTCPConnection -LocalPort $gatewayUri.Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $connection) { return }
    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($connection.OwningProcess)" -ErrorAction SilentlyContinue
    if (-not $process -or [string]$process.CommandLine -notmatch "openclaw.*gateway") {
        throw "端口 $($gatewayUri.Port) 上的进程不是可识别的 OpenClaw Gateway，为避免误停已取消自动重启。"
    }

    Write-Host "OpenClaw browser control 未启动，正在重启本机 Gateway 并启用浏览器服务..." -ForegroundColor Yellow
    Stop-Process -Id $process.ProcessId -Force
    Start-Sleep -Seconds 1
    $oldEager = $env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER
    try {
        $env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER = "1"
        Start-Process -FilePath $script:OpenClawResolvedCommand -ArgumentList @("gateway", "run") -WindowStyle Hidden | Out-Null
    }
    finally {
        if ($null -eq $oldEager) { Remove-Item Env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER -ErrorAction SilentlyContinue }
        else { $env:OPENCLAW_EAGER_BROWSER_CONTROL_SERVER = $oldEager }
    }
}

function Invoke-OpenClawBrowserHttp {
    param([string]$Method, [string]$Path, $Body = $null)
    $separator = if ($Path.Contains("?")) { "&" } else { "?" }
    $uri = "$($script:OpenClawBrowserUrl)$Path$separator" + "profile=$([uri]::EscapeDataString($Browser))"
    $headers = @{ Authorization = "Bearer $($script:OpenClawAuthToken)" }
    $params = @{ Uri = $uri; Method = $Method; Headers = $headers; TimeoutSec = 90; UseBasicParsing = $true }
    if ($null -ne $Body) {
        $headers["Content-Type"] = "application/json"
        $params.Body = $Body | ConvertTo-Json -Depth 30 -Compress
    }
    try { return Invoke-RestMethod @params }
    catch {
        $detail = if ($_.ErrorDetails -and $_.ErrorDetails.Message) { $_.ErrorDetails.Message } else { $_.Exception.Message }
        throw "OpenClaw browser HTTP 请求失败 ($Method $Path): $detail"
    }
}

function Get-OpenClawTabs {
    $response = Invoke-OpenClawBrowserHttp -Method "GET" -Path "/tabs"
    $tabs = @()
    $index = 0
    foreach ($tab in @($response.tabs)) {
        if ([string]$tab.type -ne "page") { continue }
        $tabs += [pscustomobject]@{ index = $index; targetId = $tab.targetId; tabId = $tab.tabId; label = $tab.label; title = $tab.title; url = $tab.url; wsUrl = $tab.wsUrl }
        $index++
    }
    return [pscustomobject]@{ tabs = $tabs }
}

function Set-OpenClawTargetFromTabs {
    param([int]$PreferredIndex = -1)
    $tabs = @((Get-OpenClawTabs).tabs)
    if ($tabs.Count -eq 0) { $script:OpenClawTargetId = ""; return }
    $selected = if ($PreferredIndex -ge 0 -and $PreferredIndex -lt $tabs.Count) { $tabs[$PreferredIndex] } else { $tabs | Where-Object { $_.url -like "https://chatgpt.com*" } | Select-Object -First 1 }
    if (-not $selected) { $selected = $tabs[0] }
    $script:OpenClawTargetId = [string]$selected.targetId
}

function Get-OpenClawTargetWebSocketUrl {
    if ([string]::IsNullOrWhiteSpace($script:OpenClawTargetId)) { Set-OpenClawTargetFromTabs }
    $target = @((Get-OpenClawTabs).tabs) | Where-Object { $_.targetId -eq $script:OpenClawTargetId } | Select-Object -First 1
    if (-not $target) {
        Set-OpenClawTargetFromTabs
        $target = @((Get-OpenClawTabs).tabs) | Where-Object { $_.targetId -eq $script:OpenClawTargetId } | Select-Object -First 1
    }
    if (-not $target -or [string]::IsNullOrWhiteSpace([string]$target.wsUrl)) { throw "OpenClaw 当前没有可控制的页面标签" }
    return [string]$target.wsUrl
}

function Invoke-OpenClawCdpCommand {
    param([string]$Method, $Parameters = @{})
    $socket = New-Object System.Net.WebSockets.ClientWebSocket
    $stream = New-Object System.IO.MemoryStream
    try {
        $socket.ConnectAsync([uri](Get-OpenClawTargetWebSocketUrl), [Threading.CancellationToken]::None).GetAwaiter().GetResult()
        $requestJson = @{ id = 1; method = $Method; params = $Parameters } | ConvertTo-Json -Depth 40 -Compress
        $requestBytes = [Text.Encoding]::UTF8.GetBytes($requestJson)
        $requestSegment = New-Object 'System.ArraySegment[byte]' -ArgumentList (, $requestBytes)
        $socket.SendAsync($requestSegment, [Net.WebSockets.WebSocketMessageType]::Text, $true, [Threading.CancellationToken]::None).GetAwaiter().GetResult()
        $buffer = New-Object byte[] 65536
        while ($socket.State -eq [Net.WebSockets.WebSocketState]::Open) {
            $segment = New-Object 'System.ArraySegment[byte]' -ArgumentList (, $buffer)
            $received = $socket.ReceiveAsync($segment, [Threading.CancellationToken]::None).GetAwaiter().GetResult()
            if ($received.MessageType -eq [Net.WebSockets.WebSocketMessageType]::Close) { throw "CDP 连接被浏览器关闭" }
            $stream.Write($buffer, 0, $received.Count)
            if (-not $received.EndOfMessage) { continue }
            $json = [Text.Encoding]::UTF8.GetString($stream.ToArray())
            $stream.SetLength(0)
            $response = $json | ConvertFrom-Json
            if ($response.id -ne 1) { continue }
            if ($response.error) { throw "CDP $Method 失败: $($response.error.message)" }
            return $response.result
        }
        throw "CDP 连接意外结束"
    }
    finally {
        $stream.Dispose()
        if ($socket.State -eq [Net.WebSockets.WebSocketState]::Open) {
            $socket.CloseAsync([Net.WebSockets.WebSocketCloseStatus]::NormalClosure, "done", [Threading.CancellationToken]::None).GetAwaiter().GetResult()
        }
        $socket.Dispose()
    }
}

function Invoke-OpenClawEvaluate {
    param([string]$Expression)
    $result = Invoke-OpenClawCdpCommand -Method "Runtime.evaluate" -Parameters @{ expression = $Expression; returnByValue = $true; awaitPromise = $true; userGesture = $true }
    if ($result.exceptionDetails) { throw "页面 JavaScript 执行失败: $($result.exceptionDetails.text)" }
    return $result.result.value
}

function Invoke-OpenClawKeyPress {
    param([string]$Key)
    $keyCode = switch ($Key) { "Enter" { 13 } "Escape" { 27 } "Tab" { 9 } default { 0 } }
    $common = @{ key = $Key; code = $Key; windowsVirtualKeyCode = $keyCode; nativeVirtualKeyCode = $keyCode }
    if ($Key -eq "Enter") { $common.text = "`r" }
    $down = @{ type = "keyDown" }
    $up = @{ type = "keyUp" }
    foreach ($name in $common.Keys) { $down[$name] = $common[$name]; $up[$name] = $common[$name] }
    Invoke-OpenClawCdpCommand -Method "Input.dispatchKeyEvent" -Parameters $down | Out-Null
    Invoke-OpenClawCdpCommand -Method "Input.dispatchKeyEvent" -Parameters $up | Out-Null
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
            return $result.data.result
        }

        $detailText = Get-XBErrorDetail -Result $result
        if (($attempt -lt $maxAttempts) -and (Test-XBRecoverableError -Detail $detailText)) {
            Write-Host "  xbrowser 操作失败，准备重试 ($attempt/$($maxAttempts - 1)): $detailText" -ForegroundColor Yellow
            Repair-XBrowserSession -Reason $detailText
            continue
        }

        break
    }

    $hint = if ($lastResult.hint) { " 提示: $($lastResult.hint)" } else { "" }
    $detail = ""
    if ($lastResult.data -and $lastResult.data.raw_error) {
        $detail = " 原始错误: $($lastResult.data.raw_error)"
    }
    elseif ($lastResult.data -and $lastResult.data.result -and $lastResult.data.result.error) {
        $detail = " 原始错误: $($lastResult.data.result.error)"
    }
    elseif ($lastResult.data -and $lastResult.data.browser_running) {
        $detail = " 请先手动关闭 $Browser 浏览器窗口，然后重新运行。"
    }
    throw "xbrowser 操作失败: $($lastResult.error)$hint$detail"
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

function Test-Prerequisites {
    Write-Host "检查目录和文件..." -ForegroundColor Yellow

    if (-not (Test-Path $InputDir)) { throw "输入目录不存在: $InputDir" }
    if (-not (Test-Path $RequirementPath)) { throw "requirement.md 不存在: $RequirementPath" }
    if (-not (Test-Path $OutputDir)) {
        New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
    }
    $logParent = Split-Path -Path $LogPath -Parent
    if ($logParent -and -not (Test-Path $logParent)) {
        New-Item -ItemType Directory -Path $logParent -Force | Out-Null
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

    $entry = [PSCustomObject]@{
        "文件名" = $FileName
        "开始时间" = $StartTime
        "结束时间" = $EndTime
        "状态" = $Status
        "发送次数" = $SendCount
        "输出文件名" = (Split-Path $OutputFile -Leaf)
        "备注" = (($Remarks -replace "`r`n", " ") -replace "`n", " ")
    }

    $entry | Export-Csv -Path $LogPath -Append -NoTypeInformation -Encoding UTF8
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
    $isHeader = {
        param([string]$Line)
        $columns = $Line.Trim() -split "`t"
        return ($columns.Count -ge 12 -and $columns[0] -eq "主车型" -and ($columns -contains "max_length_in") -and ($columns -contains "迭代状态"))
    }
    $inTable = $false
    $count = 0

    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if (& $isHeader $trimmed) {
            $inTable = $true
            continue
        }
        if (-not $inTable) { continue }
        if ([string]::IsNullOrWhiteSpace($trimmed)) {
            if ($count -gt 0) { break }
            continue
        }
        if ($trimmed -like "---*") { break }
        if (($trimmed -split "`t").Count -ge 12) { $count++ }
    }

    return $count
}

function Format-CapturedReplyMarkdown {
    param([string]$Text)

    if ([string]::IsNullOrWhiteSpace($Text)) { return "" }

    $normalized = $Text -replace "`r`n", "`n"
    $normalized = $normalized -replace "[ \t]+`n", "`n"
    $normalized = $normalized -replace "`n{3,}", "`n`n"
    $normalized = $normalized -replace "(?m)^```[ \t]*`n(tsv|csv|markdown|md)[ \t]*`n", ('```$1' + "`n")
    $normalized = $normalized -replace "(?m)^tsv[ \t]*`n(主车型`t分类`t品牌)", ('```tsv' + "`n" + '$1')
    $normalized = $normalized -replace "(?m)(迭代状态[^\n]*`n(?:[^\n]*`t[^\n]*`n)+)(?!(?:[^\n]*`t[^\n]*`n)|```)", ('$1```' + "`n")

    return $normalized.Trim()
}

function Get-TSVDataRowsFromText {
    param([string]$Text)

    $rows = @()
    if ([string]::IsNullOrWhiteSpace($Text)) { return $rows }

    $lines = $Text -split "`r?`n"
    $isHeader = {
        param([string]$Line)
        $columns = $Line.Trim() -split "`t"
        return ($columns.Count -ge 12 -and $columns[0] -eq "主车型" -and ($columns -contains "max_length_in") -and ($columns -contains "迭代状态"))
    }
    $headerColumns = @()
    $inTable = $false

    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if (& $isHeader $trimmed) {
            $headerColumns = @($trimmed -split "`t")
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
        if ($columns.Count -ge 12) {
            $yearIndex = [array]::IndexOf($headerColumns, "年份区间")
            if ($yearIndex -lt 0) { $yearIndex = [array]::IndexOf($headerColumns, "年份") }
            $referenceIndex = [array]::IndexOf($headerColumns, "参考车型")
            $remarksIndex = [array]::IndexOf($headerColumns, "备注")
            $statusIndex = [array]::IndexOf($headerColumns, "迭代状态")
            $rows += [PSCustomObject]@{
                Year = if ($yearIndex -ge 0 -and $yearIndex -lt $columns.Count) { [string]$columns[$yearIndex] } else { "" }
                Reference = if ($referenceIndex -ge 0 -and $referenceIndex -lt $columns.Count) { [string]$columns[$referenceIndex] } else { "" }
                Remarks = if ($remarksIndex -ge 0 -and $remarksIndex -lt $columns.Count) { [string]$columns[$remarksIndex] } else { "" }
                Status = if ($statusIndex -ge 0 -and $statusIndex -lt $columns.Count) { [string]$columns[$statusIndex] } else { "" }
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

function Test-ReplyContainsTSV {
    param([string]$Reply)

    return ((Get-TSVDataRowCountFromText -Text $Reply) -gt 0)
}

function Test-ReplyHasNextDirection {
    param([string]$Reply)

    if ([string]::IsNullOrWhiteSpace($Reply)) { return $false }

    $patterns = @(
        "下一步优先处理",
        "下一步优先补缺失",
        "下一步优先补齐",
        "下一步优先核对",
        "(^|[\r\n])\s*下一步[：:]?",
        "后续优先",
        "继续补缺失",
        "继续核对",
        "继续补强",
        "优先处理"
    )

    foreach ($pattern in $patterns) {
        if ($Reply -match $pattern) { return $true }
    }

    return $false
}

function Test-ReplyHasRoundProgressSignals {
    param([string]$Reply)

    if ([string]::IsNullOrWhiteSpace($Reply)) { return $false }

    $hasTsv = Test-ReplyContainsTSV -Reply $Reply
    $hasUpdate = $Reply -match "更新点"
    $hasProgress = $Reply -match "当前批次进度"
    $hasNextDirection = Test-ReplyHasNextDirection -Reply $Reply

    return ($hasTsv -and $hasUpdate -and $hasProgress -and $hasNextDirection)
}

function Test-CapturedReplyShellOnly {
    param([string]$Reply)

    if ([string]::IsNullOrWhiteSpace($Reply)) { return $true }
    return ($Reply.Trim() -match "^(ChatGPT\s*(说|said)?|更新点|当前批次进度|下一步方向)\s*[:：]?\s*$")
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
    $allowCleanupRetry = $true

    while ($true) {
        $openResult = Invoke-XB @openArgs
        if ($openResult.ok) { break }

        $rawError = Get-XBErrorDetail -Result $openResult

        $currentUrl = ""
        try {
            $urlResult = Invoke-XBRun "get" "url"
            $urlValue = Get-XBValue $urlResult
            if ($urlValue -and $urlValue.url) { $currentUrl = [string]$urlValue.url }
            else { $currentUrl = [string]$urlValue }
        }
        catch { }

        if ($currentUrl -like "https://chatgpt.com*") { break }

        if ($rawError -like "*ERR_ABORTED*") {
            Write-Host "open 返回 ERR_ABORTED，改用新标签页打开 ChatGPT..." -ForegroundColor Yellow
            Invoke-XBRun "tab" "new" $ChatGptUrl | Out-Null
            break
        }

        $isSessionLost = Test-XBRecoverableError -Detail $rawError
        if ($allowCleanupRetry -and $isSessionLost) {
            Write-Host "检测到 xbrowser/CDP 会话失联，执行 cleanup 后重试一次..." -ForegroundColor Yellow
            try {
                Invoke-XB "cleanup" | Out-Null
            }
            catch {
                Write-Host "  cleanup 执行失败，继续尝试重新初始化: $($_.Exception.Message)" -ForegroundColor Yellow
            }
            Start-Sleep -Seconds 2
            Initialize-XBrowser
            $allowCleanupRetry = $false
            continue
        }

        $hint = if ($openResult.hint) { " 提示: $($openResult.hint)" } else { "" }
        throw "xbrowser 打开 ChatGPT 失败: $($openResult.error)$hint 原始错误: $rawError"
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
  const normalizeText = text => (text || '')
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  const cleanReplyText = text => (text || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(line => line.trimEnd())
    .filter(line => !/^\s*(ChatGPT\s*(说|said)?|You said|你说)\s*[:：]?\s*$/.test(line))
    .join('\n')
    .trim();
  const serializeTable = table => {
    const rows = Array.from(table.querySelectorAll('tr')).map(tr =>
      Array.from(tr.querySelectorAll('th,td')).map(cell => cleanReplyText(textOf(cell)).replace(/\|/g, '\\|'))
    ).filter(row => row.length > 0);
    if (!rows.length) return '';
    const header = rows[0];
    const divider = header.map(() => '---');
    return [header, divider, ...rows.slice(1)].map(row => `| ${row.join(' | ')} |`).join('\n');
  };
  const serializeNode = node => {
    if (!node) return '';
    if (node.nodeType === Node.TEXT_NODE) return node.textContent || '';
    if (node.nodeType !== Node.ELEMENT_NODE) return '';
    const tag = node.tagName.toLowerCase();
    if (['script', 'style', 'button', 'svg', 'form', 'textarea'].includes(tag)) return '';
    if (node.matches('[contenteditable="true"], [role="button"], [aria-hidden="true"]')) return '';
    if (tag === 'pre') {
      const code = node.querySelector('code');
      const codeText = normalizeText((code && (code.innerText || code.textContent)) || node.innerText || node.textContent || '');
      if (!codeText) return '';
      const langClass = code ? Array.from(code.classList).find(c => /^language-/.test(c)) : '';
      const lang = langClass ? langClass.replace(/^language-/, '') : (/主车型\t分类\t品牌/.test(codeText) ? 'tsv' : '');
      return `\`\`\`${lang}\n${codeText}\n\`\`\``;
    }
    if (tag === 'code' && !node.closest('pre')) return '`' + cleanReplyText(textOf(node)) + '`';
    if (tag === 'table') return serializeTable(node);
    if (tag === 'br') return '\n';
    if (tag === 'li') {
      const nested = Array.from(node.childNodes).map(serializeNode).join('').trim();
      return nested ? `- ${nested}` : '';
    }
    const childText = Array.from(node.childNodes).map(serializeNode).join('');
    const cleaned = cleanReplyText(childText || textOf(node));
    if (!cleaned) return '';
    if (/^h[1-6]$/.test(tag)) return `${'#'.repeat(Number(tag[1]))} ${cleaned}`;
    if (['p', 'div', 'section', 'article', 'ul', 'ol', 'blockquote'].includes(tag)) return cleaned;
    return cleaned;
  };
  const serializeMarkdown = root => {
    const source = root.querySelector('[data-testid="markdown"], [class*="markdown"], .markdown, [data-message-content]') || root;
    const blocks = Array.from(source.children).map(serializeNode).map(normalizeText).filter(Boolean);
    const text = blocks.length ? blocks.join('\n\n') : serializeNode(source);
    return cleanReplyText(normalizeText(text));
  };
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
        const markdown = serializeMarkdown(el);
        if (markdown) candidates.push(markdown);
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
  const assistantTexts = assistantNodes.map(extractReplyText).filter(t => t.length > 0);
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
  if (!editor) {
    return { ok: false, reason: 'no-editor' };
  }

  editor.focus();
  if (editor.scrollIntoView) editor.scrollIntoView({ block: 'center' });

  if ('value' in editor) {
    const proto = Object.getPrototypeOf(editor);
    const descriptor = proto ? Object.getOwnPropertyDescriptor(proto, 'value') : null;
    if (descriptor && descriptor.set) {
      descriptor.set.call(editor, nextValue);
    } else {
      editor.value = nextValue;
    }
    editor.dispatchEvent(new InputEvent('input', { bubbles: true, data: nextValue, inputType: 'insertText' }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
    return { ok: true, mode: 'value', length: editor.value.length };
  }

  if (editor.isContentEditable) {
    editor.innerHTML = '';
    const lines = nextValue.split(/\r?\n/);
    lines.forEach((line, index) => {
      if (index > 0) editor.appendChild(document.createElement('br'));
      editor.appendChild(document.createTextNode(line));
    });
    editor.dispatchEvent(new InputEvent('input', { bubbles: true, data: nextValue, inputType: 'insertText' }));
    editor.dispatchEvent(new Event('change', { bubbles: true }));
    return { ok: true, mode: 'contenteditable', length: (editor.innerText || editor.textContent || '').length };
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

function Copy-LastChatGPTReplyMarkdown {
    param([string]$FallbackReply = "")

    Ensure-ChatGPTActive
    $script = @'
(() => {
  const textOf = el => (el && (el.innerText || el.textContent || '') || '').trim();
  const normalizeText = text => (text || '')
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  const cleanReplyText = text => (text || '')
    .replace(/\r\n/g, '\n')
    .split('\n')
    .map(line => line.trimEnd())
    .filter(line => !/^\s*(ChatGPT\s*(说|said)?|You said|你说)\s*[:：]?\s*$/.test(line))
    .join('\n')
    .trim();
  const serializeTable = table => {
    const rows = Array.from(table.querySelectorAll('tr')).map(tr =>
      Array.from(tr.querySelectorAll('th,td')).map(cell => cleanReplyText(textOf(cell)).replace(/\|/g, '\\|'))
    ).filter(row => row.length > 0);
    if (!rows.length) return '';
    const header = rows[0];
    const divider = header.map(() => '---');
    return [header, divider, ...rows.slice(1)].map(row => `| ${row.join(' | ')} |`).join('\n');
  };
  const serializeNode = node => {
    if (!node) return '';
    if (node.nodeType === Node.TEXT_NODE) return node.textContent || '';
    if (node.nodeType !== Node.ELEMENT_NODE) return '';
    const tag = node.tagName.toLowerCase();
    if (['script', 'style', 'button', 'svg', 'form', 'textarea'].includes(tag)) return '';
    if (node.matches('[contenteditable="true"], [role="button"], [aria-hidden="true"]')) return '';
    if (tag === 'pre') {
      const code = node.querySelector('code');
      const codeText = normalizeText((code && (code.innerText || code.textContent)) || node.innerText || node.textContent || '');
      if (!codeText) return '';
      const langClass = code ? Array.from(code.classList).find(c => /^language-/.test(c)) : '';
      const lang = langClass ? langClass.replace(/^language-/, '') : (/主车型\t分类\t品牌/.test(codeText) ? 'tsv' : '');
      return `\`\`\`${lang}\n${codeText}\n\`\`\``;
    }
    if (tag === 'code' && !node.closest('pre')) return '`' + cleanReplyText(textOf(node)) + '`';
    if (tag === 'table') return serializeTable(node);
    if (tag === 'br') return '\n';
    if (tag === 'li') {
      const nested = Array.from(node.childNodes).map(serializeNode).join('').trim();
      return nested ? `- ${nested}` : '';
    }
    const childText = Array.from(node.childNodes).map(serializeNode).join('');
    const cleaned = cleanReplyText(childText || textOf(node));
    if (!cleaned) return '';
    if (/^h[1-6]$/.test(tag)) return `${'#'.repeat(Number(tag[1]))} ${cleaned}`;
    if (['p', 'div', 'section', 'article', 'ul', 'ol', 'blockquote'].includes(tag)) return cleaned;
    return cleaned;
  };
  const serializeMarkdown = root => {
    const source = root.querySelector('[data-testid="markdown"], [class*="markdown"], .markdown, [data-message-content]') || root;
    const blocks = Array.from(source.children).map(serializeNode).map(normalizeText).filter(Boolean);
    const text = blocks.length ? blocks.join('\n\n') : serializeNode(source);
    return cleanReplyText(normalizeText(text));
  };
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
        const markdown = serializeMarkdown(el);
        if (markdown) candidates.push(markdown);
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
  if (!text) {
    const container = last.closest('article') || last.closest('[data-testid*="conversation-turn"]') || last;
    const articleText = extractReplyText(container);
    if (!articleText) return { ok: false, reason: 'empty-reply' };
    return { ok: true, text: articleText };
  }
  if (/^(ChatGPT\s*(说|said)?|更新点|当前批次进度|下一步方向)\s*[:：]?\s*$/i.test(text)) {
    return { ok: false, reason: 'reply-shell-only' };
  }
  return { ok: true, text };
})()
'@
    $replyResult = Get-XBValue (Invoke-XBRun "eval" $script)
    if (-not $replyResult -or -not $replyResult.ok) {
        $reason = if ($replyResult -and $replyResult.reason) { [string]$replyResult.reason } else { "unknown" }
        throw "读取最后一条回复失败: $reason"
    }
    $copied = ([string]$replyResult.text).TrimEnd()
    if ([string]::IsNullOrWhiteSpace($copied)) {
        throw "读取到的最后一条回复为空"
    }

    if (-not [string]::IsNullOrWhiteSpace($FallbackReply)) {
        $fallbackTrimmed = $FallbackReply.Trim()
        if ($copied -eq "下一步" -or ($fallbackTrimmed.Length -gt 200 -and $copied.Length -lt [Math]::Min(120, [int]($fallbackTrimmed.Length * 0.2)))) {
            throw "读取到的内容不像完整回复，长度: $($copied.Length)，DOM 回复长度: $($fallbackTrimmed.Length)"
        }
    }

    return $copied
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
    $writeAttempts = if ($LargePayload) { 4 } else { 3 }
    $written = $false

    for ($writeAttempt = 1; $writeAttempt -le $writeAttempts; $writeAttempt++) {
        Set-ChatGPTEditorText -Text $Message

        $writeWaitSeconds = if ($LargePayload) { [Math]::Max($LargePayloadDelay, 12) } else { 5 }
        if (Wait-EditorTextReady -ExpectedText $Message -LargePayload:$LargePayload -TimeoutSeconds $writeWaitSeconds) {
            $written = $true
            break
        }

        Write-Host "  输入框内容未确认，重试写入 ($writeAttempt/$writeAttempts)..." -ForegroundColor Yellow
        Start-Sleep -Seconds 2
    }

    if (-not $written) {
        $composerState = Get-ChatGPTComposerState
        throw "写入未确认，输入框长度: $($composerState.editorLength)，composer长度: $($composerState.composerLength)，附件状态: $($composerState.hasAttachment)，发送按钮可用: $($composerState.sendEnabled)，预期长度: $($Message.Length)"
    }

    if ($LargePayload) {
        Write-Host "  大文本已确认写入，等待 $LargePayloadDelay 秒后发送..." -ForegroundColor Gray
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

    function Complete-WaitWithReply {
        param(
            [string]$Reply,
            [string]$CopyRemark
        )

        Start-Sleep -Seconds $PostReplyDelay
        try {
            $copiedReply = Copy-LastChatGPTReplyMarkdown -FallbackReply $Reply
            return @{ Ok = $true; Status = ""; Remark = "页面DOM读取"; Reply = $copiedReply; CopySource = "页面DOM读取" }
        }
        catch {
            Write-Host "  页面DOM读取失败，降级使用状态文本: $($_.Exception.Message)" -ForegroundColor Yellow
            if (Test-CapturedReplyShellOnly -Reply $Reply) {
                return @{ Ok = $false; Status = "继续等待"; Remark = "状态文本只是回复外壳"; Reply = "" }
            }
            return @{ Ok = $true; Status = ""; Remark = $CopyRemark; Reply = $Reply; CopySource = $CopyRemark }
        }
    }

    while ((Get-Date) -lt $deadline) {
        $state = Get-ChatGPTState
        if ($state.loggedOut) { return @{ Ok = $false; Status = "登录失效"; Remark = "ChatGPT 页面显示未登录"; Reply = "" } }
        if ($state.pageError) { return @{ Ok = $false; Status = "页面错误"; Remark = "页面出现错误提示"; Reply = [string]$state.reply } }

        $reply = [string]$state.reply
        if ($reply -ne $lastReply) {
            $lastReply = $reply
            $stableSince = Get-Date
        }
        elseif ($reply.Length -gt 0 -and $stableSince) {
            $stableSeconds = ((Get-Date) - $stableSince).TotalSeconds
            $hasReadyState = (-not $state.isGenerating) -and $state.inputReady -and ($stableSeconds -ge $ReplyStabilityDelay)
            $hasFallbackReadyState = (-not $state.isGenerating) -and ($stableSeconds -ge ($ReplyStabilityDelay + 8))
            $looksLikeUsableReply = (Test-CompletionSignal -Text $reply) -or (Test-ReplyContainsTSV -Reply $reply) -or (Test-ReplyHasNextDirection -Reply $reply) -or ($reply.Length -ge 500)
            $stuckButStable = $looksLikeUsableReply -and ($stableSeconds -ge $StuckGeneratingGraceSeconds)

            if ($hasReadyState -or $hasFallbackReadyState -or $stuckButStable) {
                if ($stuckButStable -and $state.isGenerating) {
                    Write-Host "  回复文本已稳定 $([int]$stableSeconds) 秒，但页面仍显示生成中；先捕捉当前回复并落盘。" -ForegroundColor Yellow
                }
                $copyRemark = if ($stuckButStable -and $state.isGenerating) { "页面状态疑似卡住，使用稳定文本" } else { "页面文本fallback" }
                $completed = Complete-WaitWithReply -Reply $reply -CopyRemark $copyRemark
                if ($completed.Ok) { return $completed }
                $lastReply = ""
                $stableSince = $null
                Start-Sleep -Seconds 2
                continue
            }
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
        $taskTitle = "【全量表更新】$($TSVFile.BaseName)"
        $minimumFullTableRows = [Math]::Max(0, (@($tsvContent -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }).Count - 1))
        $message = @"
【任务名称】
$taskTitle

【任务要求】
$requirementContent

【执行顺序】
$PhaseOrderReminder

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
            $reply = Format-CapturedReplyMarkdown -Text ([string]$wait.Reply)

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
                Send-ChatGPTMessage -Message $ContinueMessage
                $sendCount++
                continue
            }

            $hasFullTable = Test-ReplyContainsFullTable -Reply $reply -MinimumRows $minimumFullTableRows
            if ((Test-FullTableRequestSignal -Text $reply) -and (-not $hasFullTable)) {
                Write-Host "  检测到全部/所有可入库，但未给完整表，发送完整全量表请求..." -ForegroundColor Yellow
                if ($nextCount -ge $MaxNextSteps) {
                    $status = "次数上限终止"
                    $remarks = "达到最大下一步次数: $MaxNextSteps"
                    break
                }
                $requestedFullTable = $true
                $previousReply = $reply
                $nextCount++
                $round++
                Send-ChatGPTMessage -Message $FullTableRequestMessage
                $sendCount++
                continue
            }

            if (Test-CompletionSignal -Text $reply) {
                if (-not $hasFullTable) {
                    Write-Host "  检测到完成信号，但完整 TSV 行数不足，发送补表请求..." -ForegroundColor Yellow
                    if ($nextCount -ge $MaxNextSteps) {
                        $status = "次数上限终止"
                        $remarks = "完成信号缺少完整 TSV，且达到最大下一步次数: $MaxNextSteps"
                        break
                    }
                    $requestedFullTable = $true
                    $previousReply = $reply
                    $nextCount++
                    $round++
                    Send-ChatGPTMessage -Message $CompletionFixMessage
                    $sendCount++
                    continue
                }
                $status = "成功"
                $remarks = "检测到明确批次完成信号且包含完整表"
                break
            }

            if (-not (Test-ReplyHasRoundProgressSignals -Reply $reply)) {
                Write-Host "  回复缺少 TSV 或推进信号，发送格式纠偏提示..." -ForegroundColor Yellow
                if ($nextCount -ge $MaxNextSteps) {
                    $status = "偏离终止"
                    $remarks = "回复缺少 TSV / 更新点 / 当前进度 / 下一步方向等正常推进信号"
                    break
                }
                $previousReply = $reply
                $nextCount++
                $round++
                Send-ChatGPTMessage -Message $MissingSignalsMessage
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
            Send-ChatGPTMessage -Message $ContinueMessage
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

    $latestByFile = @{}
    foreach ($row in $rows) {
        $fileName = $row."文件名"
        if (-not $fileName) { $fileName = $row.FileName }
        if ([string]::IsNullOrWhiteSpace($fileName)) { continue }
        $latestByFile[$fileName] = $row
    }

    $currentRows = @($latestByFile.Values | Sort-Object { $_."文件名" }, { $_.FileName })

    $count = @{
        "成功" = 0
        "重复终止" = 0
        "次数上限终止" = 0
        "页面错误" = 0
        "登录失效" = 0
        "偏离终止" = 0
    }

    foreach ($row in $currentRows) {
        $status = $row."状态"
        if (-not $status) { $status = $row.Status }
        if ($count.ContainsKey($status)) { $count[$status]++ }
    }

    $failed = $count["重复终止"] + $count["次数上限终止"] + $count["页面错误"] + $count["登录失效"] + $count["偏离终止"]
    $unsuccessfulRows = @(
        $currentRows |
            Where-Object {
                $status = $_."状态"
                if (-not $status) { $status = $_.Status }
                $status -ne "成功"
            } |
            Sort-Object { $_."文件名" }, { $_.FileName }
    )

    $unsuccessfulText = if ($unsuccessfulRows.Count -eq 0) {
        "无"
    }
    else {
        ($unsuccessfulRows | ForEach-Object {
            $fileName = $_."文件名"
            if (-not $fileName) { $fileName = $_.FileName }
            $status = $_."状态"
            if (-not $status) { $status = $_.Status }
            $remarks = $_."备注"
            if (-not $remarks) { $remarks = $_.Remarks }
            if ([string]::IsNullOrWhiteSpace($remarks)) {
                " - $fileName [$status]"
            }
            else {
                " - $fileName [$status] $remarks"
            }
        }) -join "`r`n"
    }

    $summary = @"
总文件数：$($currentRows.Count)
成功数：$($count["成功"])
重复终止数：$($count["重复终止"])
次数上限终止数：$($count["次数上限终止"])
页面错误数：$($count["页面错误"])
登录失效数：$($count["登录失效"])
偏离终止数：$($count["偏离终止"])
失败数：$failed
当前未成功的文件数：$($unsuccessfulRows.Count)
当前未成功的文件：
$unsuccessfulText
输出目录：$OutputDir
完成时间：$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
"@

    $summaryParent = Split-Path -Path $SummaryPath -Parent
    if ($summaryParent -and -not (Test-Path $summaryParent)) {
        New-Item -ItemType Directory -Path $summaryParent -Force | Out-Null
    }
    Set-Content -Path $SummaryPath -Value $summary -Encoding UTF8
}

function Main {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "OpenClaw 全量表补强自动化" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan

    Test-Prerequisites
    Initialize-XBrowser
    Open-ChatGPT

    if ($OpenOnly) {
        try {
            $checkUrl = [string](Invoke-OpenClawEvaluate -Expression "(() => location.href)()")
            $checkTitle = [string](Invoke-OpenClawEvaluate -Expression "(() => document.title)()")
            if ([string]::IsNullOrWhiteSpace($checkUrl)) { throw "页面 URL 为空" }
            Write-Host "OpenClaw 页面控制验证成功: $checkTitle ($checkUrl)" -ForegroundColor Green
        }
        catch {
            throw "ChatGPT 已打开，但 OpenClaw 页面读取验证失败: $($_.Exception.Message)"
        }
        Write-Host "如页面尚未登录，请登录完成后重新运行脚本开始处理。" -ForegroundColor Yellow
        return
    }

    $state = Get-ChatGPTState
    if ($state.loggedOut -or -not $state.inputReady) {
        Write-Host "ChatGPT 当前不可输入。请在打开的浏览器里登录，并进入可发送消息的页面后再运行脚本。" -ForegroundColor Red
        exit 1
    }

    $tsvFiles = @(Get-ChildItem -Path $InputDir -Filter $InputFilePattern -File)
    if ($InputFileOrder -eq "name_desc") { $tsvFiles = @($tsvFiles | Sort-Object Name -Descending) }
    elseif ($InputFileOrder -eq "modified_asc") { $tsvFiles = @($tsvFiles | Sort-Object LastWriteTime) }
    elseif ($InputFileOrder -eq "modified_desc") { $tsvFiles = @($tsvFiles | Sort-Object LastWriteTime -Descending) }
    else { $tsvFiles = @($tsvFiles | Sort-Object Name) }
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
    if ($OnlyFiles.Count -eq 0 -and $SkipProcessedFiles) {
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

if ($env:FITMENT_OPENCLAW_LIBRARY_ONLY -ne "1") {
    Main
}
