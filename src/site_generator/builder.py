"""Build static HTML for one or all Tyneside sites."""

from __future__ import annotations

import shutil
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

from site_generator.sites import SITES, Site, get_site

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
SITES_DIR = ROOT / "sites"
OUTPUT_DIR = ROOT / "output"


def _env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )


def _load_page_meta(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def _render_markdown(path: Path) -> str:
    if not path.exists():
        return ""
    return markdown.markdown(
        path.read_text(encoding="utf-8"),
        extensions=["extra", "sane_lists"],
    )


def _copy_static(site: Site, dest: Path) -> None:
    shared = STATIC_DIR
    site_static = SITES_DIR / site.id / "static"

    if shared.exists():
        for item in shared.iterdir():
            target = dest / item.name
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)

    if site_static.exists():
        for item in site_static.iterdir():
            target = dest / item.name
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target)


def _write_cname(site: Site, dest: Path) -> None:
    (dest / "CNAME").write_text(f"{site.domain}\n", encoding="utf-8")


def _write_nojekyll(dest: Path) -> None:
    (dest / ".nojekyll").write_text("", encoding="utf-8")


def _load_games_catalog(content_dir: Path) -> list[dict]:
    """Optional games.yaml shelf for the games site."""
    path = content_dir / "games.yaml"
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {path}")
    return data


def _site_context(site: Site, meta: dict, body_html: str = "") -> dict:
    content_dir = SITES_DIR / site.id
    return {
        "site": site,
        "page": {
            "title": meta.get("title", site.title),
            "description": meta.get("description", site.description),
            "body_html": body_html,
        },
        "sites": SITES,
        "games": _load_games_catalog(content_dir),
    }


def build_site(site: Site) -> Path:
    """Render one site into output/<id>/ and return that directory."""
    env = _env()
    dest = OUTPUT_DIR / site.id
    content_dir = SITES_DIR / site.id

    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)

    meta = _load_page_meta(content_dir / "meta.yaml")
    body_html = _render_markdown(content_dir / "index.md")
    template_name = meta.get("template", "page.html")

    context = _site_context(site, meta, body_html)
    template = env.get_template(template_name)
    html = template.render(**context)
    (dest / "index.html").write_text(html, encoding="utf-8")

    # Extra pages: any other *.md next to index.md
    for md_path in sorted(content_dir.glob("*.md")):
        if md_path.name == "index.md":
            continue
        stem = md_path.stem
        page_meta = _load_page_meta(content_dir / f"{stem}.yaml")
        page_body = _render_markdown(md_path)
        page_template = page_meta.get("template", "page.html")
        page_context = _site_context(site, {
            "title": page_meta.get("title", stem.replace("-", " ").title()),
            "description": page_meta.get("description", site.description),
            **page_meta,
        }, page_body)
        # Prefer explicit page meta title/description over site defaults
        page_context["page"] = {
            "title": page_meta.get("title", stem.replace("-", " ").title()),
            "description": page_meta.get("description", site.description),
            "body_html": page_body,
        }
        page_html = env.get_template(page_template).render(**page_context)
        (dest / f"{stem}.html").write_text(page_html, encoding="utf-8")

    _copy_static(site, dest)
    _write_cname(site, dest)
    _write_nojekyll(dest)

    return dest


def build_all(site_ids: list[str] | None = None) -> list[Path]:
    """Build selected sites (default: all)."""
    if site_ids:
        selected = [get_site(sid) for sid in site_ids]
    else:
        selected = list(SITES)
    return [build_site(site) for site in selected]
