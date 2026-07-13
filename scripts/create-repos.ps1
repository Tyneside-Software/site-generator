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
