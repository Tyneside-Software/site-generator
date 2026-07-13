"""CLI entry point: python -m site_generator [sites...]"""

from __future__ import annotations

import argparse
import sys

from site_generator.builder import build_all
from site_generator.sites import SITES


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build static HTML for Tyneside brand sites.",
    )
    parser.add_argument(
        "sites",
        nargs="*",
        help=f"Site ids to build (default: all). Known: {', '.join(s.id for s in SITES)}",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List registered sites and exit.",
    )
    args = parser.parse_args(argv)

    if args.list:
        for site in SITES:
            print(f"{site.id:12}  {site.domain:22}  -> {site.repo}")
        return 0

    try:
        paths = build_all(args.sites or None)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    for path in paths:
        print(f"built {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
