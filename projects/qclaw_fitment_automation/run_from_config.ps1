[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$ConfigPath = "",
    [ValidateSet("", "work", "check", "dry_run")]
    [string]$Mode = ""
)

$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($ConfigPath)) { $ConfigPath = Join-Path $PSScriptRoot "config.yaml" }

function Get-Value {
    param($Object, [string]$Name, $Default = $null)
    if ($null -ne $Object -and $Object.PSObject.Properties.Name -contains $Name) { return $Object.$Name }
    return $Default
}

function Resolve-ConfigPath {
    param([string]$Path, [string]$Base)
    if ([string]::IsNullOrWhiteSpace($Path)) { return "" }
    if ([System.IO.Path]::IsPathRooted($Path)) { return [System.IO.Path]::GetFullPath($Path) }
    return [System.IO.Path]::GetFullPath((Join-Path $Base $Path))
}

function Test-AnyPattern {
    param([string]$Name, [object[]]$Patterns)
    foreach ($pattern in @($Patterns)) { if ($Name -like [string]$pattern) { return $true } }
    return $false
}

$resolvedConfig = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($ConfigPath)
$loader = Join-Path $PSScriptRoot "load_fitment_config.py"
$json = & python $loader $resolvedConfig
if ($LASTEXITCODE -ne 0) { throw "读取 config.yaml 失败" }
$config = $json | ConvertFrom-Json
$configDir = [string]$config._meta.config_dir
$effectiveMode = if ($Mode) { $Mode } else { [string](Get-Value $config "mode" "work") }

$workspace = $config.workspace
$traversal = $workspace.traversal
$workspaceRoot = Resolve-ConfigPath ([string](Get-Value $workspace "root" ".")) $configDir
if (-not (Test-Path -LiteralPath $workspaceRoot -PathType Container)) { throw "workspace.root 不存在: $workspaceRoot" }

$strategy = [string](Get-Value $traversal "strategy" "directories")
$include = @((Get-Value $traversal "include" @("*")))
$exclude = @((Get-Value $traversal "exclude" @()))
$projects = @()

if ($strategy -eq "explicit") {
    foreach ($item in @((Get-Value $traversal "projects" @()))) {
        $projectPath = Resolve-ConfigPath ([string]$item) $workspaceRoot
        if (-not (Test-Path -LiteralPath $projectPath -PathType Container)) { throw "项目目录不存在: $projectPath" }
        $projects += Get-Item -LiteralPath $projectPath
    }
}
elseif ($strategy -eq "glob") {
    foreach ($pattern in $include) {
        $projects += Get-ChildItem -Path (Join-Path $workspaceRoot ([string]$pattern)) -Directory -ErrorAction SilentlyContinue
    }
}
else {
    $projects = @(Get-ChildItem -LiteralPath $workspaceRoot -Directory | Where-Object { Test-AnyPattern $_.Name $include })
}

$projects = @($projects | Where-Object { -not (Test-AnyPattern $_.Name $exclude) } | Sort-Object FullName -Unique)
$order = [string](Get-Value $traversal "order" "name_asc")
if ($order -eq "name_desc") { $projects = @($projects | Sort-Object Name -Descending) }
elseif ($order -eq "modified_asc") { $projects = @($projects | Sort-Object LastWriteTime) }
elseif ($order -eq "modified_desc") { $projects = @($projects | Sort-Object LastWriteTime -Descending) }
else { $projects = @($projects | Sort-Object Name) }
$maxProjects = [int](Get-Value $traversal "max_projects" 0)
if ($maxProjects -gt 0) { $projects = @($projects | Select-Object -First $maxProjects) }
if ($projects.Count -eq 0) { throw "遍历结果为空，请检查 workspace.traversal" }

$layout = $config.project_layout
$runtime = $config.runtime
$contract = $config.data_contract
$requirementPath = [string]$config._meta.requirement_path
if (-not (Test-Path -LiteralPath $requirementPath -PathType Leaf)) { throw "requirement 文件不存在: $requirementPath" }

$fullColumns = @($contract.full_table.columns | ForEach-Object { [string]$_ })
$subseriesEnabled = [bool](Get-Value $contract.subseries_match "enabled" $false)
$subseriesColumns = if ($subseriesEnabled) { @($contract.subseries_match.columns | ForEach-Object { [string]$_ }) } else { @() }
$oldEnvironment = @{}
$environmentMap = @{
    FITMENT_TSV_HEADER = $fullColumns -join "`t"
    FITMENT_AUTO_EMPTY_COLUMNS_DEFINED = "true"
    FITMENT_AUTO_EMPTY_COLUMNS = @($contract.full_table.auto_empty_columns) -join "、"
    FITMENT_SUBSERIES_ENABLED = $subseriesEnabled.ToString().ToLowerInvariant()
    FITMENT_SUBSERIES_HEADER = $subseriesColumns -join "`t"
    FITMENT_SUBSERIES_AUTO_EMPTY_COLUMNS_DEFINED = "true"
    FITMENT_SUBSERIES_AUTO_EMPTY_COLUMNS = @($contract.subseries_match.auto_empty_columns) -join "、"
    FITMENT_DATA_INSTRUCTIONS = @($contract.instructions) -join "；"
    FITMENT_INPUT_PATTERN = [string](Get-Value $runtime.input_files "pattern" "*.tsv")
    FITMENT_INPUT_ORDER = [string](Get-Value $runtime.input_files "order" "name_asc")
    FITMENT_SKIP_PROCESSED = ([bool](Get-Value $runtime.input_files "skip_processed" $true)).ToString().ToLowerInvariant()
}
foreach ($key in $environmentMap.Keys) {
    $oldEnvironment[$key] = [Environment]::GetEnvironmentVariable($key, "Process")
    [Environment]::SetEnvironmentVariable($key, [string]$environmentMap[$key], "Process")
}

Write-Host "配置: $resolvedConfig" -ForegroundColor Cyan
Write-Host "模式: $effectiveMode；项目数: $($projects.Count)" -ForegroundColor Cyan
Write-Host "Requirement: $requirementPath" -ForegroundColor DarkCyan
Write-Host "全量表列数: $($fullColumns.Count)；子车系匹配表: $(if ($subseriesEnabled) { "$($subseriesColumns.Count) 列" } else { "禁用" })" -ForegroundColor DarkCyan
foreach ($project in $projects) { Write-Host "  - $($project.FullName)" }
if ($effectiveMode -eq "dry_run") { exit 0 }

$scriptPath = Join-Path $PSScriptRoot "qclaw_fitment_automation.ps1"
$continueOnError = [bool](Get-Value $runtime "continue_on_error" $false)
$failures = @()
try {
    $runProjects = if ($effectiveMode -eq "check") { @($projects | Select-Object -First 1) } else { $projects }
    foreach ($project in $runProjects) {
        $inputPath = Join-Path $project.FullName ([string](Get-Value $layout "input" "input"))
        $outputPath = Join-Path $project.FullName ([string](Get-Value $layout "output" "output"))
        $logPath = Join-Path $project.FullName ([string](Get-Value $layout "log" "log.csv"))
        $summaryPath = Join-Path $project.FullName ([string](Get-Value $layout "summary" "summary.txt"))
        $arguments = @(
            "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $scriptPath,
            "-Project", $project.FullName, "-InputDir", $inputPath, "-OutputDir", $outputPath,
            "-LogPath", $logPath, "-SummaryPath", $summaryPath, "-RequirementPath", $requirementPath,
            "-MaxRounds", [string](Get-Value $runtime "max_rounds" 30),
            "-Browser", [string](Get-Value $runtime "browser" "openclaw")
        )
        $onlyFiles = @((Get-Value $runtime "only_files" @()))
        if ($onlyFiles.Count -gt 0) { $arguments += @("-OnlyFiles", ($onlyFiles -join ",")) }
        if ($effectiveMode -eq "check") { $arguments += "-OpenOnly" }

        Write-Host "`n[$effectiveMode] $($project.Name)" -ForegroundColor Green
        & powershell.exe @arguments
        if ($LASTEXITCODE -ne 0) {
            $failures += $project.FullName
            if (-not $continueOnError) { throw "项目执行失败: $($project.FullName)" }
        }
    }
}
finally {
    foreach ($key in $oldEnvironment.Keys) { [Environment]::SetEnvironmentVariable($key, $oldEnvironment[$key], "Process") }
}

if ($failures.Count -gt 0) { throw "以下项目执行失败: $($failures -join ', ')" }
