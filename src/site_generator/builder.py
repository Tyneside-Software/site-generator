"""Build static HTML for one or all Tyneside sites."""

from __future__ import annotations

import json
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


def _load_store_catalog(content_dir: Path) -> dict:
    """Optional RST-synced catalogue for the store site."""
    path = content_dir / "catalog" / "index.json"
    if not path.exists():
        return {
            "collection_count": 0,
            "product_count": 0,
            "markup_pct": 2.0,
            "top_collections": [],
            "featured_products": [],
            "synced_at": None,
        }
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected object in {path}")
    return data


def _root_prefix(depth: int = 0) -> str:
    """Relative path from a page to the site root (empty string at root)."""
    if depth <= 0:
        return ""
    return "../" * depth


def _site_context(
    site: Site,
    meta: dict,
    body_html: str = "",
    *,
    depth: int = 0,
) -> dict:
    content_dir = SITES_DIR / site.id
    root = _root_prefix(depth)
    return {
        "site": site,
        "page": {
            "title": meta.get("title", site.title),
            "description": meta.get("description", site.description),
            "body_html": body_html,
            "body_class": meta.get("body_class", ""),
        },
        "sites": SITES,
        "games": _load_games_catalog(content_dir),
        "store": _load_store_catalog(content_dir),
        # Relative path to site root for local file:// and nested pages
        "root": root,
        "home_href": f"{root}index.html" if root else "index.html",
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

    # Extra pages: *.md next to index.md that have a matching *.yaml (or not README)
    skip_md = {"index.md", "readme.md"}
    for md_path in sorted(content_dir.glob("*.md")):
        if md_path.name.lower() in skip_md:
            continue
        stem = md_path.stem
        # Only build if there is explicit page meta, or stem is a known content page
        page_meta_path = content_dir / f"{stem}.yaml"
        if not page_meta_path.exists():
            continue
        page_meta = _load_page_meta(page_meta_path)
        page_body = _render_markdown(md_path)
        page_template = page_meta.get("template", "page.html")
        page_context = _site_context(site, {
            "title": page_meta.get("title", stem.replace("-", " ").title()),
            "description": page_meta.get("description", site.description),
            **page_meta,
        }, page_body)
        page_context["page"] = {
            "title": page_meta.get("title", stem.replace("-", " ").title()),
            "description": page_meta.get("description", site.description),
            "body_html": page_body,
            "body_class": page_meta.get("body_class", ""),
        }
        page_html = env.get_template(page_template).render(**page_context)
        (dest / f"{stem}.html").write_text(page_html, encoding="utf-8")

    _copy_static(site, dest)
    _copy_site_app(site, dest)

    # Store catalogue JSON (if present) for client/debug + future checkout
    catalog_src = content_dir / "catalog"
    if catalog_src.exists():
        catalog_dest = dest / "catalog"
        if catalog_dest.exists():
            shutil.rmtree(catalog_dest)
        shutil.copytree(catalog_src, catalog_dest)

    _write_cname(site, dest)
    _write_nojekyll(dest)

    return dest


def _copy_site_app(site: Site, dest: Path) -> None:
    """Copy optional Node app bits (server, package.json) for sites that need them.

    Technology uses Express + Tide; cleaning booking is fully static.
    Never copies .env secrets.
    """
    content_dir = SITES_DIR / site.id
    for name in (
        "package.json",
        "package-lock.json",
        ".env.example",
        "README.md",
        "PROGRESS_SINCE_STRIPE_REMOVAL.txt",
        ".gitignore",
    ):
        src = content_dir / name
        if src.is_file():
            shutil.copy2(src, dest / name)

    for folder in ("server", "data"):
        src = content_dir / folder
        if not src.is_dir():
            continue
        target = dest / folder
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(
            src,
            target,
            ignore=shutil.ignore_patterns(".env", "orders.json", "*.log"),
        )


def build_all(site_ids: list[str] | None = None) -> list[Path]:
    """Build selected sites (default: all)."""
    if site_ids:
        selected = [get_site(sid) for sid in site_ids]
    else:
        selected = list(SITES)
    return [build_site(site) for site in selected]
