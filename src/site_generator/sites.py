"""Site registry — one entry per brand / GitHub Pages repo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Site:
    """A single deployable static site."""

    id: str
    domain: str
    repo: str
    title: str
    brand_word: str
    tagline: str
    description: str
    email: str
    cta_label: str

    @property
    def content_dir(self) -> Path:
        return Path("sites") / self.id

    @property
    def output_dir(self) -> Path:
        return Path("output") / self.id

    @property
    def mailto(self) -> str:
        return f"mailto:{self.email}"


SITES: tuple[Site, ...] = (
    Site(
        id="software",
        domain="tyneside.software",
        repo="tyneside.software",
        title="Tyneside Software",
        brand_word="SOFTWARE",
        tagline="Software with purpose. Built from the North East.",
        description=(
            "Vertical logistics and work-management software for field services. "
            "Starting with cleaning — free for local businesses."
        ),
        email="michael@tyneside.software",
        cta_label="Talk to Michael",
    ),
    Site(
        id="cleaning",
        domain="tyneside.cleaning",
        repo="tyneside.cleaning",
        title="Tyneside Cleaning",
        brand_word="CLEANING",
        tagline="Local cleaners. Real support. Professional results.",
        description=(
            "Supporting North East cleaning entrepreneurs with free software, "
            "websites, and paid work through community programmes."
        ),
        email="hello@tyneside.cleaning",
        cta_label="Get in touch",
    ),
    Site(
        id="charity",
        domain="tyneside.charity",
        repo="tyneside.charity",
        title="Tyneside Charity",
        brand_word="CHARITY",
        tagline="Welcome home packages for new parents.",
        description=(
            "Free deep-clean welcome home packages for new parents in the North East. "
            "Cleaners get paid work. Families get practical help."
        ),
        email="hello@tyneside.charity",
        cta_label="Get involved",
    ),
    Site(
        id="group",
        domain="tyneside.group",
        repo="tyneside.group",
        title="Tyneside Group",
        brand_word="GROUP",
        tagline="Software. Cleaning. Charity. One North East vision.",
        description=(
            "Tyneside Group — the parent brand uniting software, local entrepreneurs, "
            "and social impact across Tyneside."
        ),
        email="michael@tyneside.software",
        cta_label="Talk to Michael",
    ),
)


def get_site(site_id: str) -> Site:
    for site in SITES:
        if site.id == site_id:
            return site
    known = ", ".join(s.id for s in SITES)
    raise KeyError(f"Unknown site '{site_id}'. Known: {known}")
