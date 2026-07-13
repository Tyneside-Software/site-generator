# site-generator

Python static site generator for the **Tyneside** brand websites. One repo builds HTML; GitHub Pages repos publish each site.

| Domain | Site id | Pages repo |
|--------|---------|------------|
| [tyneside.software](https://tyneside.software) | `software` | `Tyneside-Software/tyneside.software` |
| [tyneside.cleaning](https://tyneside.cleaning) | `cleaning` | `Tyneside-Software/tyneside.cleaning` |
| [tyneside.charity](https://tyneside.charity) | `charity` | `Tyneside-Software/tyneside.charity` |
| [tyneside.group](https://tyneside.group) | `group` | `Tyneside-Software/tyneside.group` |
| [tyneside.games](https://tyneside.games) | `games` | `Tyneside-Software/tyneside.games` |

## Layout

```
sites/<id>/          # content per brand (meta.yaml + markdown)
templates/           # shared Jinja2 templates
static/              # shared CSS/assets
src/site_generator/  # build pipeline
output/<id>/         # local build output (gitignored)
.github/workflows/   # build + push to Pages repos
```

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
