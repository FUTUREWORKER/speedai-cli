$ErrorActionPreference = 'Stop'

$ScriptDir = Split-Path -Parent $PSCommandPath
$CliScript = Join-Path $ScriptDir 'speedai_cli.py'
if (-not (Test-Path -LiteralPath $CliScript -PathType Leaf)) {
  Write-Error "speedai_cli.py not found: $CliScript"
  exit 1
}

$InstallDir = if ($env:SPEEDAI_CLI_INSTALL_DIR) { $env:SPEEDAI_CLI_INSTALL_DIR } else { Join-Path $env:USERPROFILE '.speed-ai\bin' }
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null

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
