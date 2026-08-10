# logistics.tyneside.software

Brand site for **Tyneside Logistics** — static front door, product docs, and the logistics web app shell.

## Pairing

| Layer | Location |
|-------|----------|
| **Static site (this folder)** | `sites/logistics/` in [site-generator](https://github.com/Tyneside-Software/site-generator) |
| **API** | `app/brands/logistics/` in [tyneside-api](https://github.com/Tyneside-Software/tyneside-api) |
| **Pages repo** | `Tyneside-Software/logistics.tyneside.software` → domain `logistics.tyneside.software` |
| **Cloud Run** | Shared `tyneside-api` service; routes under `/v1/logistics/*` |

See monorepo [PAIRING.md](../../PAIRING.md) for the family-wide model.

## Site map

| Path | Purpose |
|------|---------|
| `/` | Brand home |
| `/docs/` | Project documentation hub (build tracker, decisions, overview) |
| `/app/` | Web app shell (placeholder until product UI is built) |

## Edit / build

```powershell
# from site-generator root
python -m site_generator logistics
# open output/logistics/index.html
```

## API base URL (app)

Configure in `static/app/app-config.js` once Cloud Run CORS includes `https://logistics.tyneside.software`.
