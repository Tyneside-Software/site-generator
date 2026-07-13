#Requires -Version 5.1
# Build all sites and open the software site in the default browser.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path $PSScriptRoot -Parent)

python -m site_generator
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$index = Join-Path (Get-Location) "output\software\index.html"
if (Test-Path $index) {
    Start-Process $index
    Write-Host "Opened $index"
} else {
    Write-Error "Build did not produce $index"
}
