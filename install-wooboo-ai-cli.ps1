$ErrorActionPreference = 'Stop'

$RepoRawBase = if ($env:WOOBOO_AI_CLI_RAW_BASE) { $env:WOOBOO_AI_CLI_RAW_BASE.TrimEnd('/') } else { 'https://raw.githubusercontent.com/FUTUREWORKER/wooboo-ai-cli/main' }
$ScriptDir = if ($PSCommandPath) { Split-Path -Parent $PSCommandPath } else { '' }
$LocalCliScript = if ($ScriptDir) { Join-Path $ScriptDir 'wooboo_ai_cli.py' } else { '' }

$InstallRoot = if ($env:WOOBOO_AI_CLI_HOME) { $env:WOOBOO_AI_CLI_HOME } else { Join-Path $env:USERPROFILE '.wooboo-ai' }
$InstallDir = if ($env:WOOBOO_AI_CLI_INSTALL_DIR) { $env:WOOBOO_AI_CLI_INSTALL_DIR } else { Join-Path $InstallRoot 'bin' }
$LibDir = Join-Path $InstallRoot 'lib'
New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
New-Item -ItemType Directory -Path $LibDir -Force | Out-Null

$CliScript = Join-Path $LibDir 'wooboo_ai_cli.py'
if ($LocalCliScript -and (Test-Path -LiteralPath $LocalCliScript -PathType Leaf)) {
  Copy-Item -LiteralPath $LocalCliScript -Destination $CliScript -Force
} else {
  Invoke-WebRequest -UseBasicParsing -Uri "$RepoRawBase/wooboo_ai_cli.py" -OutFile $CliScript
}

$CmdPath = Join-Path $InstallDir 'wooboo.cmd'
$Ps1Path = Join-Path $InstallDir 'wooboo.ps1'

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

if ($env:WOOBOO_AI_CLI_SKIP_PATH -ne '1') {
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

Write-Host "Installed Wooboo AI CLI (wooboo command): $CmdPath"
Write-Host "If the current terminal cannot find wooboo, open a new terminal or run: `$env:Path = '$InstallDir;' + `$env:Path"
