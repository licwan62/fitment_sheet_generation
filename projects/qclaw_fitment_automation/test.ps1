[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$powerShellExecutable = (Get-Process -Id $PID).Path
python -m pytest (Join-Path $root "tests_py") -q
if ($LASTEXITCODE -ne 0) { throw "Python tests failed" }
Get-ChildItem (Join-Path $root "tests") -Filter "*_smoke.ps1" | Sort-Object Name | ForEach-Object {
    Write-Host "Running $($_.Name)..." -ForegroundColor DarkCyan
    & $powerShellExecutable -NoProfile -ExecutionPolicy Bypass -File $_.FullName
    if ($LASTEXITCODE -ne 0) { throw "PowerShell smoke test failed: $($_.Name)" }
}
Write-Host "QClaw tests: OK" -ForegroundColor Green
