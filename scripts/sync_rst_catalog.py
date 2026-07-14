#!/usr/bin/env python3
"""Pull public Shopify catalogue from RST Wholesale and write local catalog JSON.

RST Wholesale: https://rst-wholesale.com/ (Shopify)

Tyneside Store model:
  - Mirror catalogue for a better storefront experience
  - Customer price = RST price + MARKUP_PCT (default 2%)
  - Markup is donated to Tyneside Charity
  - Fulfilment / wholesale supply remains RST Wholesale

Usage:
  python scripts/sync_rst_catalog.py
  python scripts/sync_rst_catalog.py --max-products 100
"""

from __future__ import annotations

import argparse
import json
import math
import ssl
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites" / "store" / "catalog"
RST_BASE = "https://rst-wholesale.com"
MARKUP_PCT = 2.0  # +2% donated to charity

# Avoid broken corporate TLS intercepts on some Windows setups
_CTX = ssl.create_default_context()


def _get_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "TynesideStoreCatalogSync/0.1 (+https://tyneside.store)",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, context=_CTX, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _money(amount: float) -> str:
    return f"{amount:.2f}"


def _customer_price(rst_price: str | float) -> dict:
    base = float(rst_price)
    charity = round(base * (MARKUP_PCT / 100.0), 2)
    # Round customer price to nearest penny, always >= base + charity
    total = math.ceil((base + charity) * 100) / 100
    charity = round(total - base, 2)
    return {
        "rst_gbp": _money(base),
        "charity_gbp": _money(charity),
        "customer_gbp": _money(total),
        "markup_pct": MARKUP_PCT,
    }


def fetch_collections() -> list[dict]:
    data = _get_json(f"{RST_BASE}/collections.json?limit=250")
    cols = []
    for c in data.get("collections", []):
        cols.append(
            {
                "id": c["id"],
                "title": c["title"],
                "handle": c["handle"],
                "products_count": c.get("products_count", 0),
                "image": (c.get("image") or {}).get("src"),
                "rst_url": f"{RST_BASE}/collections/{c['handle']}",
            }
        )
    cols.sort(key=lambda x: (-x["products_count"], x["title"].lower()))
    return cols


def fetch_products(max_products: int) -> list[dict]:
    products: list[dict] = []
    page = 1
    while len(products) < max_products:
        url = f"{RST_BASE}/products.json?limit=250&page={page}"
        try:
            data = _get_json(url)
        except urllib.error.HTTPError:
            break
        batch = data.get("products") or []
        if not batch:
            break
        for p in batch:
            variants = p.get("variants") or []
            if not variants:
                continue
            v0 = variants[0]
            images = p.get("images") or []
            pricing = _customer_price(v0.get("price") or "0")
            products.append(
                {
                    "id": p["id"],
                    "title": p["title"],
                    "handle": p["handle"],
                    "vendor": p.get("vendor"),
                    "tags": p.get("tags") or [],
                    "available": bool(v0.get("available")),
                    "image": images[0]["src"] if images else None,
                    "rst_url": f"{RST_BASE}/products/{p['handle']}",
                    "pricing": pricing,
                    "variant_count": len(variants),
                }
            )
            if len(products) >= max_products:
                break
        page += 1
        if page > 40:
            break
    return products


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-products", type=int, default=120)
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)

    print("Fetching collections…")
    collections = fetch_collections()
    print(f"  {len(collections)} collections")

    print(f"Fetching up to {args.max_products} products…")
    products = fetch_products(args.max_products)
    print(f"  {len(products)} products")

    catalog = {
        "source": {
            "name": "RST Wholesale Ltd",
            "url": RST_BASE,
            "shopify": "rst-wholesale.myshopify.com",
            "synced_at": datetime.now(timezone.utc).isoformat(),
        },
        "model": {
            "white_label": True,
            "fulfililment": "RST Wholesale",
            "markup_pct": MARKUP_PCT,
            "markup_destination": "Tyneside Charity (tyneside.charity)",
            "notes": (
                "Customer pays RST wholesale price + markup_pct. "
                "Orders are fulfilled via RST; markup is donated to charity."
            ),
        },
        "collections": collections,
        "products": products,
    }

    out_path = OUT / "catalog.json"
    out_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")

    # Lightweight index for templates
    index = {
        "synced_at": catalog["source"]["synced_at"],
        "collection_count": len(collections),
        "product_count": len(products),
        "markup_pct": MARKUP_PCT,
        "top_collections": collections[:12],
        "featured_products": products[:24],
    }
    (OUT / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT / 'index.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
