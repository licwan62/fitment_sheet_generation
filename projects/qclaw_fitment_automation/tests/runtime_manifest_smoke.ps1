$ErrorActionPreference = "Stop"
$module = Join-Path (Split-Path $PSScriptRoot -Parent) "powershell/QClaw.Runtime.psm1"
Import-Module $module -Force
$testRoot = Join-Path ([IO.Path]::GetTempPath()) ("qclaw-manifest-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $testRoot | Out-Null
try {
    $input = Join-Path $testRoot "input.tsv"
    [IO.File]::WriteAllText($input, "Ktype`n1`n2`n", (New-Object Text.UTF8Encoding($false)))
    $tasks = @(1..10 | ForEach-Object {
        [pscustomobject]@{ TaskId = "task-$_"; DisplayName = "Task $_"; SourceName = "input.tsv"; CheckpointPath = (Join-Path $testRoot "checkpoints/task-$_.json") }
    })
    $manifestPath = Join-Path $testRoot "partition_manifest.json"
    $manifest = New-QClawRunManifest -Tasks $tasks -InputFiles @((Get-Item $input)) `
        -ProjectRoot $testRoot -Path $manifestPath -PartitionCount 4 -Strategy contiguous `
        -ConfigHash "aa" -RequirementHash "bb" -PromptHash "cc" -CodeHash "dd" -GitCommit "commit"
    Assert-QClawRunManifest -Manifest $manifest -Tasks $tasks -InputFiles @((Get-Item $input)) `
        -ProjectRoot $testRoot -PartitionCount 4 -Strategy contiguous `
        -ConfigHash "aa" -RequirementHash "bb" -PromptHash "cc" -CodeHash "dd"
    $counts = @(1..4 | ForEach-Object {
        @(Select-QClawManifestPartition -Manifest $manifest -Tasks $tasks -PartitionIndex $_).Count
    })
    if (($counts -join ",") -ne "3,3,2,2") { throw "分片数量错误: $counts" }
    Write-Host "runtime_manifest_smoke: OK"
}
finally {
    if (Test-Path -LiteralPath $testRoot) { Remove-Item -LiteralPath $testRoot -Recurse -Force }
}
