#Requires -Version 5.1
<#
.SYNOPSIS
  Push built output/<id>/ into each GitHub Pages repo (local fallback for CI).

.DESCRIPTION
  Mirrors .github/actions/deploy-site: clone the Pages repo, replace its files
  with output/<id>/, commit, push origin main.

  Official path is still: push site-generator main → Actions.
  Use this when PAGES_DEPLOY_TOKEN is missing so CI cannot cross-push.

.EXAMPLE
  python -m site_generator
  .\scripts\deploy-pages.ps1
  .\scripts\deploy-pages.ps1 software
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

$all = @(
    @{ id = "software";    repo = "tyneside.software" }
    @{ id = "cleaning";    repo = "tyneside.cleaning" }
    @{ id = "charity";     repo = "tyneside.charity" }
    @{ id = "group";       repo = "tyneside.group" }
    @{ id = "games";       repo = "tyneside.games" }
    @{ id = "technology";  repo = "tyneside.technology" }
    @{ id = "logistics";   repo = "logistics.tyneside.software" }
    @{ id = "green";       repo = "tyneside.green" }
    @{ id = "garden";      repo = "tyneside.garden" }
    @{ id = "beer";        repo = "tyneside.beer" }
    @{ id = "church";      repo = "tyneside.church" }
    @{ id = "store";       repo = "tyneside.store" }
)

$filter = @()
if ($args.Count -gt 0) {
    $filter = ($args[0] -split ",") | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ }
}

if ($filter -contains "academy") {
    Write-Host "skip  academy  (standalone — https://github.com/Tyneside-Software/tyneside.academy)"
    $filter = @($filter | Where-Object { $_ -ne "academy" })
    if ($filter.Count -eq 0) { exit 0 }
}

$sha = (git -C $Root rev-parse --short HEAD).Trim()
$work = Join-Path $env:TEMP "tyneside-pages-deploy"
New-Item -ItemType Directory -Force -Path $work | Out-Null

$ok = 0
$skip = 0
$fail = 0

foreach ($s in $all) {
    if ($filter.Count -gt 0 -and $filter -notcontains $s.id) { continue }

    $src = Join-Path $Root "output\$($s.id)"
    if (-not (Test-Path $src)) {
        Write-Host "skip  $($s.id)  (no output\$($s.id))"
        $skip++
        continue
    }

    $dest = Join-Path $work $s.id
    if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }

    Write-Host "clone $($s.repo)"
    git clone --depth 1 "https://github.com/Tyneside-Software/$($s.repo).git" $dest
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAIL  $($s.id)  clone"
        $fail++
        continue
    }

    Get-ChildItem $dest -Force | Where-Object { $_.Name -ne ".git" } | Remove-Item -Recurse -Force
    Copy-Item -Path (Join-Path $src "*") -Destination $dest -Recurse -Force
    if (-not (Test-Path (Join-Path $dest ".nojekyll"))) {
        New-Item -ItemType File -Path (Join-Path $dest ".nojekyll") | Out-Null
    }

    git -C $dest add -A
    git -C $dest diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "ok    $($s.id)  no changes"
        $ok++
        continue
    }

    git -C $dest commit -m "Deploy from site-generator $sha"
    git -C $dest push origin HEAD:main
    if ($LASTEXITCODE -ne 0) {
        Write-Host "FAIL  $($s.id)  push"
        $fail++
        continue
    }
    Write-Host "ok    $($s.id)  pushed"
    $ok++
}

Write-Host ""
Write-Host "done  ok=$ok  skip=$skip  fail=$fail"
if ($fail -gt 0) { exit 1 }
