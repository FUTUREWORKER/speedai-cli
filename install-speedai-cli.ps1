$ErrorActionPreference = 'Stop'

$RepoRawBase = if ($env:SPEEDAI_CLI_RAW_BASE) { $env:SPEEDAI_CLI_RAW_BASE.TrimEnd('/') } else { 'https://raw.githubusercontent.com/FUTUREWORKER/speedai-cli/main' }
$ScriptDir = if ($PSCommandPath) { Split-Path -Parent $PSCommandPath } else { '' }
$LocalCliScript = if ($ScriptDir) { Join-Path $ScriptDir 'speedai_cli.py' } else { '' }

$InstallRoot = if ($env:SPEEDAI_CLI_HOME) { $env:SPEEDAI_CLI_HOME } else { Join-Path $env:USERPROFILE '.speed-ai' }
$InstallDir = if ($env:SPEEDAI_CLI_INSTALL_DIR) { $env:SPEEDAI_CLI_INSTALL_DIR } else { Join-Path $InstallRoot 'bin' }
$LibDir = Join-Path $InstallRoot 'lib'
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
New-Item -ItemType Directory -Path $LibDir -Force | Out-Null

$CliScript = Join-Path $LibDir 'speedai_cli.py'
if ($LocalCliScript -and (Test-Path -LiteralPath $LocalCliScript -PathType Leaf)) {
  Copy-Item -LiteralPath $LocalCliScript -Destination $CliScript -Force
} else {
  Invoke-WebRequest -UseBasicParsing -Uri "$RepoRawBase/speedai_cli.py" -OutFile $CliScript
}

$CmdPath = Join-Path $InstallDir 'speedai.cmd'
$Ps1Path = Join-Path $InstallDir 'speedai.ps1'

$cmdContent = @"
@echo off
python "$CliScript" %*
"@
Set-Content -Path $CmdPath -Value $cmdContent -Encoding ASCII

$ps1Content = @"
& python "$CliScript" @args
exit `$LASTEXITCODE
"@
Set-Content -Path $Ps1Path -Value $ps1Content -Encoding UTF8

if ($env:SPEEDAI_CLI_SKIP_PATH -ne '1') {
  $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
  if ($null -eq $userPath) { $userPath = '' }
  $entries = $userPath.Split(';') | Where-Object { $_ -ne '' }
  $already = $false
  foreach ($entry in $entries) {
    if ([string]::Equals($entry.TrimEnd([char]92), $InstallDir.TrimEnd([char]92), [System.StringComparison]::OrdinalIgnoreCase)) {
      $already = $true
      break
    }
  }
  if (-not $already) {
    $nextPath = if ($userPath) { "$InstallDir;$userPath" } else { $InstallDir }
    [Environment]::SetEnvironmentVariable('Path', $nextPath, 'User')
  }
}

Write-Host "Installed speedai CLI: $CmdPath"
Write-Host "If the current terminal cannot find speedai, open a new terminal or run: `$env:Path = '$InstallDir;' + `$env:Path"
