# SantientPHP Game Engine - Build & Automation Script
[CmdletBinding()]
param (
    [switch]$Run,
    [switch]$CheckOnly,
    [switch]$Clean,
    [switch]$Release,
    [switch]$DebugMode
)

$ErrorActionPreference = "Stop"

$sphcCandidates = @(
    "C:\Users\waula\OneDrive\Desktop\santientphp\build\bin\sphc.exe",
    "C:\Program Files\SantientPHP\bin\sphc.exe",
    (Get-Command sphc -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Source -ErrorAction SilentlyContinue)
)

$sphcPath = $null
foreach ($cand in $sphcCandidates) {
    if ($cand -and (Test-Path $cand)) {
        $sphcPath = $cand
        break
    }
}

if (-not $sphcPath) {
    Write-Host "[ERROR] SantientPHP compiler 'sphc' not found." -ForegroundColor Red
    exit 1
}

$env:SPH_HOME = "C:\Users\waula\OneDrive\Desktop\santientphp"

if ($Clean) {
    Write-Host "[CLEAN] Purging build artifacts..." -ForegroundColor Yellow
    Remove-Item "bin" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item "*.s", "*.exe" -Force -ErrorAction SilentlyContinue
    Write-Host "[OK] Clean complete." -ForegroundColor Green
    if (-not $Run -and -not $CheckOnly) { exit 0 }
}

Write-Host "[1/2] Checking syntax and semantics..." -ForegroundColor Cyan
& $sphcPath check src/main.sph
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Semantic check failed." -ForegroundColor Red
    exit $LASTEXITCODE
}
Write-Host "[OK] Semantic validation passed." -ForegroundColor Green

if ($CheckOnly) { exit 0 }

if (-not (Test-Path "bin")) {
    New-Item -ItemType Directory -Path "bin" | Out-Null
}

$opt = if ($Release) { "-O3" } elseif ($DebugMode) { "-O0" } else { "-O2" }
Write-Host "[2/2] Compiling game engine binary ($opt --gui)..." -ForegroundColor Cyan

& $sphcPath build src/main.sph --gui $opt -o bin/game.exe
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "[OK] Build succeeded: bin/game.exe" -ForegroundColor Green

if ($Run) {
    Write-Host "`nLaunching game engine..." -ForegroundColor Magenta
    Start-Process -FilePath "bin/game.exe"
}
