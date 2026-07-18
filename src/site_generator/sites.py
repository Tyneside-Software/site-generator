"""Site registry — one entry per brand / GitHub Pages repo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Shared contact — WhatsApp is primary (where Michael pays attention)
PHONE_E164 = "447411949215"
PHONE_DISPLAY = "+44 7411 949215"
CONTACT_EMAIL = "michael@tyneside.software"


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

    @property
    def phone_display(self) -> str:
        return PHONE_DISPLAY

    @property
    def whatsapp(self) -> str:
        return f"https://wa.me/{PHONE_E164}"


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
        email=CONTACT_EMAIL,
        cta_label="WhatsApp Michael",
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
        email=CONTACT_EMAIL,
        cta_label="Book a clean",
    ),
    Site(
        id="charity",
        domain="tyneside.charity",
        repo="tyneside.charity",
        title="Tyneside Charity",
        brand_word="CHARITY",
        tagline="Free cleans for new parents in Howden Ward.",
        description=(
            "Free welcome-home cleans for new parents in Howden Ward. Not a registered charity yet — "
            "donations paid into Tyneside Cleaning. Promise: every £30 raised delivers one 2-hour free clean."
        ),
        email=CONTACT_EMAIL,
        cta_label="Donate",
    ),
    Site(
        id="group",
        domain="tyneside.group",
        repo="tyneside.group",
        title="Tyneside Group",
        brand_word="GROUP",
        tagline="One vision. Several doors. Jobs, care, kit, practice.",
        description=(
            "Main entrance to Tyneside: software jobs engine, volume cleaning, "
            "welcome-home charity, second-hand technology, and games for coding practice."
        ),
        email=CONTACT_EMAIL,
        cta_label="WhatsApp Michael",
    ),
    Site(
        id="technology",
        domain="tyneside.technology",
        repo="tyneside.technology",
        title="Tyneside Technology",
        brand_word="TECH",
        tagline="Working second-hand computers. Cheap for people who need them.",
        description=(
            "For-profit: still-working second-hand hardware at low prices. "
            "Profit funds good stories — appeals system for free gear when it matters."
        ),
        email=CONTACT_EMAIL,
        cta_label="Shop · £250",
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
        email=CONTACT_EMAIL,
        cta_label="WhatsApp",
    ),
)


def get_site(site_id: str) -> Site:
    for site in SITES:
        if site.id == site_id:
            return site
    known = ", ".join(s.id for s in SITES)
    raise KeyError(f"Unknown site '{site_id}'. Known: {known}")
