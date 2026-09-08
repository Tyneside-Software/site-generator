# Brand pairing model

Each Tyneside brand is ideally a **pair**:

| Side | Repo | Path pattern |
|------|------|----------------|
| **Static site** | [site-generator](https://github.com/Tyneside-Software/site-generator) | `sites/<id>/` |
| **API brand** | [tyneside-api](https://github.com/Tyneside-Software/tyneside-api) | `app/brands/<id>/` |

Pages publish from separate `tyneside.<domain>` repos. The API is one Cloud Run service with per-brand routers under `/v1/<id>/…`.

Marketing-only brands may skip the API package until they need secrets or server logic.

Family nav/footer only includes sites with `nav_order` set (software, cleaning, technology, games, group). Other live doors (charity, logistics) and aspirational sketches are reached from **tyneside.group**. Sketches (`aspirational=True`) also appear on **tyneside.group/next.html**.

## Current brands

| id | Domain | Site content | API package | Notes |
|----|--------|--------------|-------------|-------|
| `software` | tyneside.software | yes | optional later | Marketing + books |
| `cleaning` | tyneside.cleaning | yes | planned | Booking UI points at API; calendar routes TBD |
| `charity` | tyneside.charity | yes | yes (`charity`) | `POST /v1/donate/intent` |
| `group` | tyneside.group | yes | no | Portal only |
| `technology` | tyneside.technology | yes | optional later | Client Tide shop |
| `games` | tyneside.games | yes | no | Static games |
| `logistics` | logistics.tyneside.software | yes | yes (`logistics`) | App shell + docs + `/v1/logistics/*` |
| `green` | tyneside.green | yes | no | Aspirational. Lifetime carbon via Greenacres + volunteers; Gift Aid via charity later. Not in family nav. Listed on `tyneside.group/next.html` |
| `garden` | tyneside.garden | yes | no | Aspirational. Paid local gardening / outdoor maintenance. Not in family nav. Listed on `tyneside.group/next.html` |
| `beer` | tyneside.beer | yes | no | Aspirational. Dropship Dynamite Valley; order here, +2% to charity. Not in family nav. Listed on `tyneside.group/next.html` |
| `academy` | tyneside.academy | yes | no | Aspirational. Lewis early GCSEs + notes site; possible group tutoring. Not in family nav. Listed on `tyneside.group/next.html` |
| `church` | tyneside.church | yes | no | Aspirational. Multi-faith conversation / maybe monthly meetup. Not in family nav. Listed on `tyneside.group/next.html` |
| `store` | tyneside.store | yes | no | Katie’s squishy shop (fidget squish). Email to buy. Not in family nav. |

## Logistics layout (reference pair)

```
site-generator                          tyneside-api
sites/logistics/                        app/brands/logistics/
  meta.yaml + index.md                    router.py   → /v1/logistics/*
  docs/     project tracker & ADRs        README.md
  static/app/   web app shell
```

## GitHub teams (who can write)

Add people to a **team**, not as one-off collaborators on each repo.

| Team | Who | Repos (write) |
|------|-----|----------------|
| [internal](https://github.com/orgs/Tyneside-Software/teams/internal) | Tyneside staff | `logistics.tyneside.software` + `tyneside-api` |
| [lauren-outsource](https://github.com/orgs/Tyneside-Software/teams/lauren-outsource) | Lauren contractors (Indian firm, two days/week; practice project done, awaiting review then a private sandbox) | `lauren` only — never `site-generator` / tyneside.software |

Logistics **source** still lives in `site-generator` (`sites/logistics/`). That repo is public; grant write there separately if an internal person ships the site, not only the Pages repo.

## Adding a brand that needs both

1. Register `Site` in `src/site_generator/sites.py`.
2. Add `sites/<id>/` content + template/theme if needed.
3. Add deploy step + Pages repo (`scripts/create-repos.ps1`).
4. Add `app/brands/<id>/router.py` and include it from `app/main.py`.
5. Extend Cloud Run `CORS_ORIGINS` for the new domain.
6. Document the pair in this file and the brand READMEs.
