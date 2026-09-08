# site-generator

Python static site generator for the **Tyneside** brand websites. One repo builds HTML; GitHub Pages repos publish each site.

| Domain | Site id | Pages repo |
|--------|---------|------------|
| [tyneside.software](https://tyneside.software) | `software` | `Tyneside-Software/tyneside.software` |
| [tyneside.cleaning](https://tyneside.cleaning) | `cleaning` | `Tyneside-Software/tyneside.cleaning` |
| [tyneside.charity](https://tyneside.charity) | `charity` | `Tyneside-Software/tyneside.charity` |
| [tyneside.group](https://tyneside.group) | `group` | `Tyneside-Software/tyneside.group` |
| [tyneside.games](https://tyneside.games) | `games` | `Tyneside-Software/tyneside.games` |
| [tyneside.technology](https://tyneside.technology) | `technology` | `Tyneside-Software/tyneside.technology` |
| [logistics.tyneside.software](https://logistics.tyneside.software) | `logistics` | `Tyneside-Software/logistics.tyneside.software` |
| [tyneside.green](https://tyneside.green) | `green` | `Tyneside-Software/tyneside.green` (aspirational — not in family nav yet) |
| [tyneside.garden](https://tyneside.garden) | `garden` | `Tyneside-Software/tyneside.garden` (aspirational — not in family nav yet) |
| [tyneside.beer](https://tyneside.beer) | `beer` | `Tyneside-Software/tyneside.beer` (aspirational — not in family nav yet) |
| [tyneside.academy](https://tyneside.academy) | `academy` | `Tyneside-Software/tyneside.academy` (aspirational — not in family nav yet) |
| [tyneside.church](https://tyneside.church) | `church` | `Tyneside-Software/tyneside.church` (aspirational — not in family nav yet) |
| [tyneside.store](https://tyneside.store) | `store` | `Tyneside-Software/tyneside.store` (Katie’s squishy shop — not in family nav) |

Interactive brands pair with **[tyneside-api](https://github.com/Tyneside-Software/tyneside-api)** (`app/brands/<id>/`). See **[PAIRING.md](./PAIRING.md)**.

## Layout

```
sites/<id>/          # content per brand (meta.yaml + markdown)
sites/logistics/     # docs/ + static/app/ shell (API-paired brand)
sites/games/         # games.yaml shelf + static/play/<slug>/index.html
templates/           # shared Jinja2 templates
static/              # shared CSS/assets
src/site_generator/  # build pipeline
output/<id>/         # local build output (gitignored)
.github/workflows/   # build + push to Pages repos
PAIRING.md           # site ↔ API brand pairing model
```

The top nav/footer only lists doors with `nav_order` set (currently software, cleaning, tech, games, group). Everything else is reached from [tyneside.group](https://tyneside.group). Aspirational brands (`aspirational=True`) also appear on [tyneside.group/next.html](https://tyneside.group/next.html).

### Adding a game (tyneside.games)

1. Put the game at `sites/games/static/play/<slug>/index.html`
2. Register it in `sites/games/games.yaml`
3. `python -m site_generator games` and deploy


## Local build

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
pip install -r requirements.txt

python -m site_generator              # all sites
python -m site_generator software     # one site
python -m site_generator --list
```

Output lands in `output/<site_id>/` (includes `index.html`, `CNAME`, `.nojekyll`, assets).

## Audio (xAI TTS)

Josh-book and church `/bible` voice text via `https://api.x.ai/v1/tts` (`scripts/xai_tts.py`). **Never commit the key.**

1. Copy `secrets/xai.key.example` to `secrets/xai.key` and paste a key from [console.x.ai](https://console.x.ai) (gitignored).
2. From this folder:

```powershell
python scripts/church_bible.py check-key
.\scripts\tts-bible.ps1            # Genesis 1 + Revelation 22 only
.\scripts\tts-bible.ps1 -Force     # regenerate those two
```

Details: `secrets/README.md` and `sites/church/README.md`.

## Bible (tyneside.software/bible)

Whole Protestant canon in the public-domain **World English Bible**, same reader chrome as `/michael-book/`.

```powershell
python scripts/build_bible.py
python -m site_generator software
```

Writes `sites/software/static/bible/` (index + one HTML file per book). CI copies static into the Pages repo.

## Org bootstrap (one-time)

The GitHub MCP identity used earlier (`michaelthomsoncc`) does **not** currently have admin on [Tyneside-Software](https://github.com/Tyneside-Software). Use an account that **owns** the org (or invite that account as Owner), then:

```powershell
# 1) Auth as an org admin
gh auth login

# 2) Create the five public repos
.\scripts\create-repos.ps1

# 3) Push this generator
git init
git add .
git commit -m "Initial site-generator scaffold"
git branch -M main
git remote add origin https://github.com/Tyneside-Software/site-generator.git
git push -u origin main
```

### Deploy token (required for CI)

Cross-repo push needs a secret on **site-generator**:

1. Create a fine-grained PAT (or classic `repo` PAT) that can write to the four site repos.
2. Org → **site-generator** → Settings → Secrets → Actions → new secret:
   - Name: `PAGES_DEPLOY_TOKEN`
   - Value: the PAT

On every push to `main`, the workflow builds all sites and force-updates each Pages repo’s `main` branch with the generated files.

If `PAGES_DEPLOY_TOKEN` is missing, CI will build and then fail on the first Pages checkout. Local fallback (same copy-and-push as the Action):

```powershell
python -m site_generator
.\scripts\deploy-pages.ps1
```

### GitHub Pages + custom domains

For each of the four site repos:

1. Settings → Pages → Source: **Deploy from a branch** → `main` / `/ (root)`.
2. Custom domain: set `tyneside.software` (etc.). The build already writes a matching `CNAME` file.
3. At your DNS provider, point each domain at GitHub Pages (A/AAAA or CNAME per [GitHub docs](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)).

## Editing a site

1. Change `sites/<id>/index.md` and/or `meta.yaml`.
2. Adjust shared chrome in `templates/` or `static/styles.css`.
3. `python -m site_generator <id>` to preview under `output/`.
4. Merge to `main` → CI deploys.

## Licence

Private brand sites — all rights reserved unless stated otherwise.
