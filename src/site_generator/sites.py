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
            "Starting Howden Ward. Market-rate £30/2-hour packs for reach and volume. "
            "All revenue to cleaner fees — no founder draw. Based at Howden Community Hub."
        ),
        email="michael@tyneside.software",
        cta_label="Get in touch",
    ),
    Site(
        id="charity",
        domain="tyneside.charity",
        repo="tyneside.charity",
        title="Tyneside Charity",
        brand_word="CHARITY",
        tagline="Free cleans for new parents in Howden Ward.",
        description=(
            "Free 2-hour welcome-home deep cleans for new parents — starting Howden Ward "
            "(~150 births/year est.). Based at Howden Community Hub. Cleaners paid £15/hr."
        ),
        email="michael@tyneside.software",
        cta_label="Get involved",
    ),
    Site(
        id="group",
        domain="tyneside.group",
        repo="tyneside.group",
        title="Tyneside Group",
        brand_word="GROUP",
        tagline="One vision. Four doors. Jobs, care, software, practice.",
        description=(
            "Main entrance to Tyneside: software jobs engine, volume cleaning, "
            "welcome-home charity, and games for newbie coding practice."
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
        tagline="Built by Lewis, aged 12 — one night, standing start.",
        description=(
            "Everything here was built completely and 100% by Lewis in one night "
            "from a standing start, aged 12. That is what we can teach newbies."
        ),
        email="michael@tyneside.software",
        cta_label="Say hello",
    ),
)


def get_site(site_id: str) -> Site:
    for site in SITES:
        if site.id == site_id:
            return site
    known = ", ".join(s.id for s in SITES)
    raise KeyError(f"Unknown site '{site_id}'. Known: {known}")
