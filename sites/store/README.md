# tyneside.store

**Katie's squishy shop** — [fidget squish](https://tyneside.store/).

Squishies, homemade, and slime. Email [katie@tyneside.software](mailto:katie@tyneside.software) to buy. Not a Tyneside checkout.

The shop lives in `static/` (its own look, not the family chrome). Old links on tyneside.software `/katie/` redirect here.

## Build

```powershell
python -m site_generator store
```

Open `output/store/index.html`. Deploy: `.\scripts\deploy-pages.ps1 store`.

RST Wholesale was an earlier idea for this domain. It is not this site. Leftover `catalog/` JSON is unused and is not published.
