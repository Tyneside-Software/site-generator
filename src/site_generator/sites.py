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
    # When True: listed on tyneside.group/next.html (sketchbook), not a live door.
    aspirational: bool = False
    # Family nav/footer order. None = not in the top bar; reach it from tyneside.group.
    nav_order: int | None = None
    # When True: lives in its own repo. Not built or deployed by this generator.
    standalone: bool = False

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
    def phone_e164(self) -> str:
        return PHONE_E164

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
        nav_order=1,
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
        nav_order=2,
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
        nav_order=5,
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
        nav_order=3,
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
        nav_order=4,
    ),
    Site(
        id="logistics",
        domain="logistics.tyneside.software",
        repo="logistics.tyneside.software",
        title="Tyneside Logistics",
        brand_word="LOGISTICS",
        tagline="Field ops web app — routes, jobs, and the docs beside them.",
        description=(
            "Logistics and field-operations product for the Tyneside family: "
            "web app shell, project documentation, and paired API on tyneside-api."
        ),
        email=CONTACT_EMAIL,
        cta_label="Open app",
    ),
    Site(
        id="green",
        domain="tyneside.green",
        repo="tyneside.green",
        title="Tyneside Green",
        brand_word="GREEN",
        tagline="A lifetime of CO₂, in reach. Pay Greenacres. Volunteers go further.",
        description=(
            "A lifetime of personal CO₂ looking like ~£25k. "
            "Easy: pay Greenacres in Northumberland. Further: volunteer planting. "
            "Stretch: tyneside.charity + Gift Aid once registered. Not started."
        ),
        email=CONTACT_EMAIL,
        cta_label="WhatsApp the sketch",
        aspirational=True,
    ),
    Site(
        id="garden",
        domain="tyneside.garden",
        repo="tyneside.garden",
        title="Tyneside Garden",
        brand_word="GARDEN",
        tagline="Lawns, beds, and the outside of the house. Someone already does this work.",
        description=(
            "Paid local gardening and outdoor house maintenance. "
            "A person who already looks after Michael's house could take on gardens. "
            "Different from tyneside.green (carbon / Greenacres). Not a public booking yet."
        ),
        email=CONTACT_EMAIL,
        cta_label="WhatsApp the sketch",
        aspirational=True,
    ),
    Site(
        id="beer",
        domain="tyneside.beer",
        repo="tyneside.beer",
        title="Tyneside Beer",
        brand_word="BEER",
        tagline="Order here. Dynamite Valley ships it. 2% to charity. Sketch, not a till.",
        description=(
            "Joke domain, real brewery friend (Dynamite Valley, Cornwall). "
            "Dropship: order through tyneside.beer, they fulfil. "
            "+2% to tyneside.charity. No shop yet."
        ),
        email=CONTACT_EMAIL,
        cta_label="WhatsApp the sketch",
        aspirational=True,
    ),
    Site(
        id="academy",
        domain="tyneside.academy",
        repo="tyneside.academy",
        title="Tyneside Academy",
        brand_word="ACADEMY",
        tagline="Lewis is sitting GCSEs early. Dad is tutoring. The notes could become a door.",
        description=(
            "Michael is tutoring his son Lewis for early GCSEs. "
            "Lewis is building a site of everything he has learned. "
            "Possible next: publish that, and/or tutor other children (maybe as a group). Sketch only."
        ),
        email=CONTACT_EMAIL,
        cta_label="Open the course",
        aspirational=True,
        standalone=True,
    ),
    Site(
        id="church",
        domain="tyneside.church",
        repo="tyneside.church",
        title="Tyneside Church",
        brand_word="CHURCH",
        tagline="Bought on a whim. Multi-faith conversation for learning — maybe a monthly meetup.",
        description=(
            "Domain bought on a whim. Michael has been talking with local church people "
            "and friends from other religions, for his own education. "
            "Maybe a monthly multi-faith meetup. Not a congregation. Sketch only."
        ),
        email=CONTACT_EMAIL,
        cta_label="WhatsApp the sketch",
        aspirational=True,
    ),
    Site(
        id="store",
        domain="tyneside.store",
        repo="tyneside.store",
        title="fidget squish",
        brand_word="STORE",
        tagline="Katie's squishy and fidget shop. Email to buy.",
        description=(
            "Katie's shop: squishies, homemade, and slime. "
            "Email katie@tyneside.software to buy. Not a Tyneside checkout."
        ),
        email="katie@tyneside.software",
        cta_label="Email Katie",
    ),
)


def get_site(site_id: str) -> Site:
    for site in SITES:
        if site.id == site_id:
            return site
    known = ", ".join(s.id for s in SITES)
    raise KeyError(f"Unknown site '{site_id}'. Known: {known}")
