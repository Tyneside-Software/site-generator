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
        tagline="Volume cleaning. Every pound to cleaners. Grow forever.",
        description=(
            "Market-rate £30/2-hour packs for reach and volume. All revenue to cleaner fees — "
            "no founder draw. Jobs, software customers, surplus to charity; postcode by postcode."
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
        tagline="Free cleans for new parents in Forest Hall.",
        description=(
            "Free 2-hour welcome-home deep cleans for new parents in Forest Hall "
            "(~400 births/year when fully scaled). Cleaners paid £15/hr."
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
        tagline="Software. Cleaning. Charity. Games. One North East vision.",
        description=(
            "Tyneside Group — the parent brand uniting software, local entrepreneurs, "
            "social impact, and hobby games across Tyneside."
        ),
        email="michael@tyneside.software",
        cta_label="Talk to Michael",
    ),
    Site(
        id="games",
        domain="tyneside.games",
        repo="tyneside.games",
        title="Tyneside Games",
        brand_word="GAMES",
        tagline="Hobby code. Small games. No rush.",
        description=(
            "A playground for hobby games and experiments from Tyneside. "
            "Nothing commercial — just code for fun. Maybe one will be finished one day."
        ),
        email="michael@tyneside.software",
        cta_label="Say hello",
    ),
    Site(
        id="store",
        domain="tyneside.store",
        repo="tyneside.store",
        title="Tyneside Store",
        brand_word="STORE",
        tagline="Craft blanks & wholesale — better storefront, charity built in.",
        description=(
            "Tyneside Store white-labels RST Wholesale. Same catalogue fulfilled by RST; "
            "we add 2% and donate it to Tyneside Charity."
        ),
        email="hello@tyneside.store",
        cta_label="Shop now",
    ),
)


def get_site(site_id: str) -> Site:
    for site in SITES:
        if site.id == site_id:
            return site
    known = ", ".join(s.id for s in SITES)
    raise KeyError(f"Unknown site '{site_id}'. Known: {known}")
