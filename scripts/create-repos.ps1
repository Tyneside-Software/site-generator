#Requires -Version 5.1
<#
.SYNOPSIS
  Create the Tyneside-Software public repos (idempotent).
.NOTES
  Must run as a GitHub user with admin on the org.
#>
$ErrorActionPreference = "Stop"
$Org = "Tyneside-Software"

$repos = @(
    @{
        name = "site-generator"
        description = "Python static site generator for Tyneside brand websites"
    },
    @{
        name = "tyneside.software"
        description = "GitHub Pages site for tyneside.software"
    },
    @{
        name = "tyneside.cleaning"
        description = "GitHub Pages site for tyneside.cleaning"
    },
    @{
        name = "tyneside.charity"
        description = "GitHub Pages site for tyneside.charity"
    },
    @{
        name = "tyneside.group"
        description = "GitHub Pages site for tyneside.group"
    },
    @{
        name = "tyneside.games"
        description = "GitHub Pages site for tyneside.games — hobby games playground"
    },
    @{
        name = "tyneside.technology"
        description = "Tyneside Technology — second-hand working computers; profit funds free-gear appeals"
    },
    @{
        name = "logistics.tyneside.software"
        description = "GitHub Pages site for logistics.tyneside.software — field ops web app + docs"
    },
    @{
        name = "tyneside.green"
        description = "GitHub Pages site for tyneside.green — Tyneside Green (aspirational / not live yet)"
    },
    @{
        name = "tyneside.garden"
        description = "GitHub Pages site for tyneside.garden — Tyneside Garden (aspirational / not live yet)"
    },
    @{
        name = "tyneside.beer"
        description = "GitHub Pages site for tyneside.beer — Tyneside Beer (aspirational / joke domain)"
    },
    @{
        name = "tyneside.academy"
        description = "Standalone GitHub Pages site for tyneside.academy — Lewis's GCSE notes (not built by site-generator)"
    },
    @{
        name = "tyneside.church"
        description = "GitHub Pages site for tyneside.church — Tyneside Church (aspirational / multi-faith conversation)"
    },
    @{
        name = "tyneside.store"
        description = "GitHub Pages site for tyneside.store — Tyneside Store (aspirational / RST Wholesale sketch)"
    }
)

gh auth status | Out-Host

foreach ($r in $repos) {
    $full = "$Org/$($r.name)"
    $exists = gh repo view $full 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "exists  $full"
        continue
    }

    Write-Host "create  $full"
    gh repo create $full `
        --public `
        --description $r.description `
        --add-readme
}

Write-Host ""
Write-Host "Done. Next:"
Write-Host "  1. Push site-generator from this folder"
Write-Host "  2. Add secret PAGES_DEPLOY_TOKEN on site-generator"
Write-Host "  3. Enable Pages (main / root) + custom domain on each site repo"
