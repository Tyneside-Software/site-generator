"""Build the tyneside.software/bible reader from the World English Bible.

Public-domain modern English. Same chrome as michael-book: sidebar nav,
serif reading column, gold on dark. One HTML file per book (the whole
Bible is ~780k words — too large for a single page).

Usage:
  python scripts/build_bible.py
"""
from __future__ import annotations

import json
import re
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "sites" / "software" / "bible-source" / "web"
OVERVIEW_PATH = ROOT / "sites" / "software" / "bible-source" / "overview.json"
CHAPTERS_PATH = ROOT / "sites" / "software" / "bible-source" / "chapters.json"
CHURCH_WEB = ROOT / "sites" / "church" / "bible-source" / "web"
OUT_DIR = ROOT / "sites" / "software" / "static" / "bible"
BOOKS_DIR = OUT_DIR / "books"
WEB_URL = "https://raw.githubusercontent.com/TehShrike/world-english-bible/master/json/{stem}.json"
UA = "tyneside.software-bible/1.0 (public-domain World English Bible reader)"

# name, json stem, testament, group, aliases
BOOKS: list[tuple[str, str, str, str, list[str]]] = [
    ("Genesis", "genesis", "ot", "Law", ["gen", "ge", "gn"]),
    ("Exodus", "exodus", "ot", "Law", ["exod", "exo", "ex"]),
    ("Leviticus", "leviticus", "ot", "Law", ["lev", "le", "lv"]),
    ("Numbers", "numbers", "ot", "Law", ["num", "nu", "nm"]),
    ("Deuteronomy", "deuteronomy", "ot", "Law", ["deut", "de", "dt"]),
    ("Joshua", "joshua", "ot", "History", ["josh", "jos", "jsh"]),
    ("Judges", "judges", "ot", "History", ["judg", "jdg", "jg"]),
    ("Ruth", "ruth", "ot", "History", ["rth", "ru"]),
    ("1 Samuel", "1samuel", "ot", "History", ["1sam", "1sa", "1sm", "isamuel"]),
    ("2 Samuel", "2samuel", "ot", "History", ["2sam", "2sa", "2sm", "iisamuel"]),
    ("1 Kings", "1kings", "ot", "History", ["1kgs", "1ki", "1k", "ikings"]),
    ("2 Kings", "2kings", "ot", "History", ["2kgs", "2ki", "2k", "iikings"]),
    ("1 Chronicles", "1chronicles", "ot", "History", ["1chr", "1ch", "ichronicles"]),
    ("2 Chronicles", "2chronicles", "ot", "History", ["2chr", "2ch", "iichronicles"]),
    ("Ezra", "ezra", "ot", "History", ["ezr"]),
    ("Nehemiah", "nehemiah", "ot", "History", ["neh", "ne"]),
    ("Esther", "esther", "ot", "History", ["est", "es"]),
    ("Job", "job", "ot", "Wisdom", ["jb"]),
    ("Psalms", "psalms", "ot", "Wisdom", ["ps", "psa", "psalm", "pss"]),
    ("Proverbs", "proverbs", "ot", "Wisdom", ["prov", "pro", "prv"]),
    ("Ecclesiastes", "ecclesiastes", "ot", "Wisdom", ["eccl", "ecc", "eccles"]),
    ("Song of Solomon", "songofsolomon", "ot", "Wisdom", ["song", "sos", "so", "cant"]),
    ("Isaiah", "isaiah", "ot", "Prophets", ["isa", "is"]),
    ("Jeremiah", "jeremiah", "ot", "Prophets", ["jer", "je"]),
    ("Lamentations", "lamentations", "ot", "Prophets", ["lam", "la"]),
    ("Ezekiel", "ezekiel", "ot", "Prophets", ["ezek", "eze", "ezk"]),
    ("Daniel", "daniel", "ot", "Prophets", ["dan", "da", "dn"]),
    ("Hosea", "hosea", "ot", "Prophets", ["hos", "ho"]),
    ("Joel", "joel", "ot", "Prophets", ["jl"]),
    ("Amos", "amos", "ot", "Prophets", ["am"]),
    ("Obadiah", "obadiah", "ot", "Prophets", ["obad", "ob"]),
    ("Jonah", "jonah", "ot", "Prophets", ["jon", "jnh"]),
    ("Micah", "micah", "ot", "Prophets", ["mic", "mc"]),
    ("Nahum", "nahum", "ot", "Prophets", ["nah", "na"]),
    ("Habakkuk", "habakkuk", "ot", "Prophets", ["hab", "hb"]),
    ("Zephaniah", "zephaniah", "ot", "Prophets", ["zeph", "zep", "zp"]),
    ("Haggai", "haggai", "ot", "Prophets", ["hag", "hg"]),
    ("Zechariah", "zechariah", "ot", "Prophets", ["zech", "zec", "zc"]),
    ("Malachi", "malachi", "ot", "Prophets", ["mal", "ml"]),
    ("Matthew", "matthew", "nt", "Gospels", ["matt", "mt", "mat"]),
    ("Mark", "mark", "nt", "Gospels", ["mrk", "mk", "mr"]),
    ("Luke", "luke", "nt", "Gospels", ["luk", "lk"]),
    ("John", "john", "nt", "Gospels", ["joh", "jhn", "jn"]),
    ("Acts", "acts", "nt", "History", ["act", "ac"]),
    ("Romans", "romans", "nt", "Letters", ["rom", "ro", "rm"]),
    ("1 Corinthians", "1corinthians", "nt", "Letters", ["1cor", "1co", "icorinthians"]),
    ("2 Corinthians", "2corinthians", "nt", "Letters", ["2cor", "2co", "iicorinthians"]),
    ("Galatians", "galatians", "nt", "Letters", ["gal", "ga"]),
    ("Ephesians", "ephesians", "nt", "Letters", ["eph", "ep"]),
    ("Philippians", "philippians", "nt", "Letters", ["phil", "php", "pp"]),
    ("Colossians", "colossians", "nt", "Letters", ["col", "co"]),
    ("1 Thessalonians", "1thessalonians", "nt", "Letters", ["1thess", "1th", "ithessalonians"]),
    ("2 Thessalonians", "2thessalonians", "nt", "Letters", ["2thess", "2th", "iithessalonians"]),
    ("1 Timothy", "1timothy", "nt", "Letters", ["1tim", "1ti", "itimothy"]),
    ("2 Timothy", "2timothy", "nt", "Letters", ["2tim", "2ti", "iitimothy"]),
    ("Titus", "titus", "nt", "Letters", ["tit", "ti"]),
    ("Philemon", "philemon", "nt", "Letters", ["phlm", "phm", "pm"]),
    ("Hebrews", "hebrews", "nt", "Letters", ["heb", "he"]),
    ("James", "james", "nt", "Letters", ["jas", "jm"]),
    ("1 Peter", "1peter", "nt", "Letters", ["1pet", "1pe", "1pt", "ipeter"]),
    ("2 Peter", "2peter", "nt", "Letters", ["2pet", "2pe", "2pt", "iipeter"]),
    ("1 John", "1john", "nt", "Letters", ["1jn", "1jo", "1jhn", "ijohn"]),
    ("2 John", "2john", "nt", "Letters", ["2jn", "2jo", "2jhn", "iijohn"]),
    ("3 John", "3john", "nt", "Letters", ["3jn", "3jo", "3jhn", "iiijohn"]),
    ("Jude", "jude", "nt", "Letters", ["jud", "jd"]),
    ("Revelation", "revelation", "nt", "Revelation", ["rev", "re", "apoc", "apocalypse"]),
]

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _fetch(stem: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    church = CHURCH_WEB / f"{stem}.json"
    if church.is_file() and church.stat().st_size > 200:
        shutil.copy2(church, dest)
        return dest
    url = WEB_URL.format(stem=stem)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())
    return dest


def ensure_sources() -> None:
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    missing = []
    for _name, stem, *_rest in BOOKS:
        path = SRC_DIR / f"{stem}.json"
        if not path.is_file() or path.stat().st_size < 200:
            missing.append(stem)
    if not missing:
        return
    print(f"Fetching {len(missing)} World English Bible JSON files…")
    errors: list[str] = []

    def one(stem: str) -> tuple[str, Exception | None]:
        try:
            _fetch(stem, SRC_DIR / f"{stem}.json")
            return stem, None
        except Exception as exc:  # noqa: BLE001
            return stem, exc

    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = [pool.submit(one, stem) for stem in missing]
        for fut in as_completed(futs):
            stem, err = fut.result()
            if err:
                errors.append(f"{stem}: {err}")
            else:
                print(f"  {stem}.json")
    if errors:
        raise SystemExit("Failed to fetch:\n  " + "\n  ".join(errors))


def vn_html(chapter: int, verse: int, first: bool) -> str:
    cls = "vn first" if first else "vn"
    vid = f"c-{chapter}-v-{verse}"
    return (
        f'<span class="{cls}" id="{vid}">'
        f'<a href="#{vid}">{verse}</a></span>'
    )


def parse_book(tokens: list[dict]) -> dict[int, dict]:
    """Return {chapter: {verses, words, html}} preserving WEB paragraphs/stanzas."""
    chapters: dict[int, dict] = {}
    mode: str | None = None
    buf: list[str] = []
    last_verse: int | None = None
    current_ch: int | None = None
    verse_first = True

    def ensure(ch: int) -> dict:
        if ch not in chapters:
            chapters[ch] = {"verses": set(), "words": 0, "parts": []}
        return chapters[ch]

    def flush() -> None:
        nonlocal buf, last_verse, verse_first
        if current_ch is None or not buf:
            buf = []
            return
        html = "".join(buf).strip()
        buf = []
        last_verse = None
        verse_first = True
        if not html:
            return
        tag = "p class=\"stanza\"" if mode == "stanza" else "p"
        close = "p"
        chapters[current_ch]["parts"].append(f"<{tag}>{html}</{close}>")

    def add_text(ch: int, verse: int, text: str, linebreak: bool = False) -> None:
        nonlocal last_verse, current_ch, verse_first
        if current_ch != ch:
            flush()
            current_ch = ch
        rec = ensure(ch)
        rec["verses"].add(verse)
        rec["words"] += len(text.split())
        piece = escape(re.sub(r"\s+", " ", text).strip())
        if not piece and not linebreak:
            return
        if verse != last_verse:
            marker = vn_html(ch, verse, verse_first)
            verse_first = False
            last_verse = verse
            if buf and not buf[-1].endswith((" ", ">")):
                buf.append(" ")
            buf.append(marker)
        if piece:
            if buf and not buf[-1].endswith((" ", ">")):
                buf.append(" ")
            buf.append(piece)
        if linebreak:
            buf.append("<br>\n")

    for tok in tokens:
        kind = tok.get("type")
        if kind in ("paragraph start", "stanza start"):
            flush()
            mode = "stanza" if kind.startswith("stanza") else "para"
        elif kind in ("paragraph end", "stanza end", "break"):
            flush()
            mode = None
        elif kind == "line break":
            if buf:
                buf.append("<br>\n")
        elif kind in ("paragraph text", "line text"):
            ch = int(tok["chapterNumber"])
            verse = int(tok["verseNumber"])
            add_text(ch, verse, tok.get("value") or "", linebreak=False)

    flush()
    return chapters


def load_book(stem: str) -> dict[int, dict]:
    tokens = json.loads((SRC_DIR / f"{stem}.json").read_text(encoding="utf-8"))
    chapters = parse_book(tokens)
    if not chapters:
        raise ValueError(f"No chapters in {stem}")
    return chapters


def page_shell(
    title: str,
    description: str,
    asset_prefix: str,
    body_attrs: str,
    toggle_label: str,
    aside: str,
    main: str,
) -> str:
    css = f"{asset_prefix}bible.css?v=audio9"
    canon = f"{asset_prefix}canon.js"
    js = f"{asset_prefix}bible.js?v=audio9"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="theme-color" content="#121018">
  <link rel="stylesheet" href="{css}">
  <script defer src="{canon}"></script>
  <script defer src="{js}"></script>
</head>
<body {body_attrs}>
  <a class="skip" href="#main">Skip to reading</a>
  <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="chapter-side">{escape(toggle_label)}</button>
  <div class="nav-backdrop" id="nav-backdrop" hidden></div>
  <aside class="side" id="chapter-side" aria-label="Navigation">
    <button type="button" class="nav-close" id="nav-close" aria-label="Close navigation">×</button>
    {aside}
  </aside>
  <div class="shell">
    <div class="side-spacer" aria-hidden="true"></div>
    <main class="main" id="main">
      {main}
    </main>
  </div>
  <a class="top" href="#">Top</a>
  <audio id="bible-audio" preload="none" playsinline webkit-playsinline></audio>
  <div id="audio-dock" hidden>
    <button type="button" id="dock-toggle">Pause</button>
    <span id="dock-label"></span>
    <span id="dock-time"></span>
  </div>
</body>
</html>
"""


def write_canon(stats: list[dict]) -> None:
    payload = [
        {
            "name": s["name"],
            "slug": s["stem"],
            "chapters": s["chapter_count"],
            "testament": s["testament"],
            "group": s["group"],
            "aliases": s["aliases"],
        }
        for s in stats
    ]
    (OUT_DIR / "canon.js").write_text(
        "window.BIBLE_CANON = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )


def grouped_book_nav_fixed(stats: list[dict], current: str | None = None) -> str:
    """Book nav with OT/NT group labels, History split correctly."""
    parts: list[str] = []
    last_key = None
    for s in stats:
        key = (s["testament"], s["group"])
        if key != last_key:
            prefix = "OT · " if s["testament"] == "ot" else "NT · "
            parts.append(f'<div class="nav-group">{prefix}{escape(s["group"])}</div>')
            last_key = key
        active = " is-active" if current == s["stem"] else ""
        href = f'{s["stem"]}.html' if current else f'books/{s["stem"]}.html'
        filt = escape(s["name"] + " " + s["stem"] + " " + " ".join(s["aliases"]))
        parts.append(
            f'<a class="nav-item book-link{active}" href="{href}" data-filter="{filt}">'
            f'<span class="t">{escape(s["name"])}</span>'
            f'<span class="ch">{s["chapter_count"]}</span></a>'
        )
    return "".join(parts)


def load_overview() -> dict:
    if not OVERVIEW_PATH.is_file():
        raise SystemExit(f"Missing {OVERVIEW_PATH}")
    data = json.loads(OVERVIEW_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("books"), dict):
        raise SystemExit(f"overview.json must be an object with a books map")
    books = data["books"]
    about_path = OVERVIEW_PATH.parent / "about.json"
    if about_path.is_file():
        abouts = json.loads(about_path.read_text(encoding="utf-8"))
        if not isinstance(abouts, dict):
            raise SystemExit("about.json must be an object keyed by book stem")
        for stem, paras in abouts.items():
            if stem not in books:
                raise SystemExit(f"about.json unknown book: {stem}")
            books[stem]["about"] = paras
    extra: dict = {}
    if CHAPTERS_PATH.is_file():
        extra = json.loads(CHAPTERS_PATH.read_text(encoding="utf-8"))
    guides_dir = OVERVIEW_PATH.parent / "chapter-guides"
    if guides_dir.is_dir():
        for path in sorted(guides_dir.glob("*.json")):
            chunk = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(chunk, dict):
                raise SystemExit(f"{path.name} must be an object keyed by book stem")
            extra.update(chunk)
    if not isinstance(extra, dict):
        raise SystemExit("chapter guides must be an object keyed by book stem")
    for stem, notes in extra.items():
        if stem not in books:
            raise SystemExit(f"chapter guide unknown book: {stem}")
        if not isinstance(notes, list):
            raise SystemExit(f"chapter guide {stem} must be a list of notes")
        books[stem]["chapters"] = [str(n).strip() for n in notes]
    return data


def load_audio() -> dict:
    path = OUT_DIR / "audio-manifest.json"
    if not path.is_file():
        raise SystemExit(
            f"Missing {path}. Run: python scripts/fetch_bible_audio.py"
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    books = data.get("books") if isinstance(data, dict) else None
    if not isinstance(books, dict):
        raise SystemExit("audio-manifest.json must have a books map")
    return data


def chapter_audio_html(stem: str, name: str, n: int, url: str) -> str:
    if not url:
        return ""
    label = f"Psalm {n}" if name == "Psalms" else f"{name} chapter {n}"
    fname = f"henson-{stem}-{n:03d}.mp3"
    src = escape(url)
    return (
        f'<div class="ch-audio" data-src="{src}" data-label="{escape(label)}">'
        f'<button type="button" class="btn-play" aria-label="Play {escape(label)}">Play</button>'
        f'<a class="btn-dl" href="{src}" download="{escape(fname)}">Download</a>'
        f'<span class="audio-time" hidden>0:00</span>'
        f'<span class="audio-err" hidden></span>'
        f'<div class="progress-wrap" hidden>'
        f'<div class="progress-bar" role="slider" aria-label="Seek">'
        f'<div class="progress-fill"></div></div></div>'
        f"</div>"
    )


def about_html(meta: dict, *, teaser: bool = False, stem: str = "") -> str:
    about = meta.get("about") or ""
    paras = [str(p).strip() for p in (about if isinstance(about, list) else [about]) if str(p).strip()]
    if not paras:
        return ""
    if teaser and len(paras) > 2:
        shown = paras[:2]
        rest = len(paras) - 2
        href = f"books/{stem}.html#about" if stem else "#about"
        more = (
            f'<p class="ov-more"><a href="{escape(href)}">'
            f"Full summary on the book page ({rest} more "
            f"{'paragraphs' if rest != 1 else 'paragraph'}) →</a></p>"
        )
        return "".join(f'<p class="ov-about">{escape(p)}</p>' for p in shown) + more
    return "".join(f'<p class="ov-about">{escape(p)}</p>' for p in paras)


def chapter_guide_html(
    stem: str,
    name: str,
    notes: list[str],
    *,
    href_prefix: str,
    details: bool,
    open_by_default: bool = False,
) -> str:
    if not notes:
        return ""
    label = "Psalm" if name == "Psalms" else "Chapter"
    items = []
    for i, note in enumerate(notes, 1):
        href = f"{href_prefix}#c-{i}"
        items.append(
            f'<li><a href="{href}">{escape(label)} {i}</a>'
            f'<span>{escape(note)}</span></li>'
        )
    ol = f'<ol class="ov-chapters">{"".join(items)}</ol>'
    heading = f"Chapter guide · {len(notes)}"
    if not details:
        return (
            f'<section class="book-guide" id="guide">'
            f"<h2>Chapter guide</h2>"
            f"<p class=\"guide-lead\">One line on each {label.lower()}, then the text below. "
            f"Jump to a chapter from here or the sidebar.</p>"
            f"{ol}</section>"
        )
    open_attr = " open" if open_by_default else ""
    return (
        f'<details class="ov-guide"{open_attr}>'
        f"<summary>{escape(heading)}</summary>{ol}</details>"
    )


def _group_anchor(testament: str, group: str) -> str:
    raw = f"{testament}-{group}".lower()
    return "g-" + re.sub(r"[^a-z0-9]+", "-", raw).strip("-")


def render_overview(
    stats: list[dict],
    overview: dict,
    total_chapters: int,
    total_words: int,
    built: str,
) -> str:
    books_meta = overview.get("books") or {}
    groups_meta = overview.get("groups") or {}
    missing = [s["stem"] for s in stats if s["stem"] not in books_meta]
    if missing:
        raise SystemExit("overview.json missing books: " + ", ".join(missing))
    no_guide = [
        s["stem"]
        for s in stats
        if not (books_meta[s["stem"]].get("chapters") or [])
    ]
    if no_guide:
        raise SystemExit("chapters.json missing guides: " + ", ".join(no_guide))

    group_nav: list[str] = []
    parts: list[str] = []
    last_test: str | None = None
    last_group: str | None = None
    open_block = False

    for s in stats:
        if s["testament"] != last_test:
            if open_block:
                parts.append("</div></section>")
                open_block = False
            last_test = s["testament"]
            last_group = None
            heading = "Old Testament" if last_test == "ot" else "New Testament"
            hid = "ot" if last_test == "ot" else "nt"
            blurb = overview.get(hid) or ""
            parts.append(f'<h2 id="{hid}">{escape(heading)}</h2>')
            if blurb:
                parts.append(f'<p class="ov-test-lead">{escape(blurb)}</p>')
        if s["group"] != last_group:
            if open_block:
                parts.append("</div></section>")
            last_group = s["group"]
            gk = f"{s['testament']}:{s['group']}"
            anchor = _group_anchor(s["testament"], s["group"])
            prefix = "OT" if s["testament"] == "ot" else "NT"
            group_nav.append(
                f'<a class="nav-item" href="#{anchor}">'
                f'<span class="t">{escape(prefix)} · {escape(s["group"])}</span></a>'
            )
            gblurb = groups_meta.get(gk) or ""
            parts.append(f'<section class="ov-group" id="{anchor}">')
            parts.append(f"<h3>{escape(s['group'])}</h3>")
            if gblurb:
                parts.append(f'<p class="ov-group-lead">{escape(gblurb)}</p>')
            parts.append('<div class="ov-books">')
            open_block = True

        meta = books_meta[s["stem"]]
        tag = str(meta.get("tagline") or "")
        nch = s["chapter_count"]
        notes = meta.get("chapters") or []
        if notes and len(notes) != nch:
            raise SystemExit(
                f"{s['stem']}: chapter guide has {len(notes)} notes, book has {nch} chapters"
            )
        ch_label = "1 chapter" if nch == 1 else f"{nch} chapters"
        tag_html = f'<p class="ov-tag">{escape(tag)}</p>' if tag else ""
        guide = chapter_guide_html(
            s["stem"],
            s["name"],
            notes,
            href_prefix=f"books/{s['stem']}.html",
            details=True,
            open_by_default=nch <= 8,
        )
        parts.append(
            f'<article class="ov-book" id="{escape(s["stem"])}">'
            f"<header>{tag_html}"
            f"<h4><a href=\"books/{s['stem']}.html\">{escape(s['name'])}</a></h4>"
            f'<p class="ov-meta">{ch_label} · {s["words"]:,} words</p>'
            f"</header>"
            f"{about_html(meta, teaser=True, stem=s['stem'])}"
            f"{guide}"
            f'<p class="ov-actions">'
            f'<a href="books/{s["stem"]}.html">Read {escape(s["name"])} →</a>'
            f'<a href="books/{s["stem"]}.html#guide">Chapter guide</a>'
            f"</p></article>"
        )

    if open_block:
        parts.append("</div></section>")

    lead = str(overview.get("lead") or "")
    nav = grouped_book_nav_fixed(stats)
    aside = f"""
    <div class="side-head">
      <div class="brand"><a href="../index.html">tyneside.software</a> · <a href="index.html">bible</a></div>
      <h1>The whole story</h1>
      <p class="sub">What each book is about</p>
      <div class="epigraph">
        A map of the sixty-six: a proper summary of each book, then a chapter guide.
      </div>
      <div class="stats">
        <div><strong>{len(stats)}</strong> books</div>
        <div><strong>{total_chapters:,}</strong> chapters</div>
        <div><strong>{total_words:,}</strong> words</div>
        <div>{escape(built)}</div>
      </div>
      {jump_block()}
    </div>
    <p class="side-lib"><a href="index.html">← All books</a></p>
    <nav class="nav" aria-label="Sections">{"".join(group_nav)}</nav>
    <nav class="nav" aria-label="Books">{nav}</nav>
    """

    main = f"""
      <header class="hero">
        <div class="badge">Overview · sixty-six books</div>
        <h1>The whole story</h1>
        <p>{escape(lead)}</p>
        <div class="hero-actions">
          <a class="btn-fill" href="#ot">Old Testament</a>
          <a class="btn-ghost" href="#nt">New Testament</a>
          <a class="btn-ghost" href="index.html">Library of books</a>
        </div>
      </header>
      <section class="overview" id="overview">
        {"".join(parts)}
      </section>
      <footer class="foot">
        World English Bible · overview · <a href="index.html">Holy Bible</a>
      </footer>
    """
    return page_shell(
        title="The whole story — Holy Bible",
        description="A map of the whole Bible: a longer summary of each of the sixty-six books, and a chapter guide for every book.",
        asset_prefix="",
        body_attrs='data-page="overview"',
        toggle_label="Books",
        aside=aside,
        main=main,
    )


def jump_block() -> str:
    return """
      <form class="jump" id="jump-form" action="#" method="get">
        <input id="jump-input" type="search" placeholder="John 3:16" autocomplete="off" aria-label="Jump to a verse">
        <button type="submit">Go</button>
      </form>
      <p class="jump-err" id="jump-err" role="status"></p>
      <input class="filter" id="nav-filter" type="search" placeholder="Filter books or chapters" aria-label="Filter navigation">
    """


def render_index(stats: list[dict], total_chapters: int, total_words: int, built: str) -> str:
    nav = grouped_book_nav_fixed(stats)
    aside = f"""
    <div class="side-head">
      <div class="brand"><a href="../index.html">tyneside.software</a> · bible</div>
      <h1>Holy Bible</h1>
      <p class="sub">World English Bible</p>
      <div class="epigraph">
        Sixty-six books. Public-domain modern English.
        From <em>In the beginning</em> to Amen.
      </div>
      <div class="stats">
        <div><strong>{len(stats)}</strong> books</div>
        <div><strong>{total_chapters:,}</strong> chapters</div>
        <div><strong>{total_words:,}</strong> words</div>
        <div>{escape(built)}</div>
      </div>
      {jump_block()}
    </div>
    <p class="side-lib"><a href="overview.html">The whole story — what each book is about</a></p>
    <nav class="nav" aria-label="Books">{nav}</nav>
    """

    def cards(testament: str, heading: str) -> str:
        out = [f"<h2>{escape(heading)}</h2>"]
        last_group = None
        open_cards = False
        for s in stats:
            if s["testament"] != testament:
                continue
            if s["group"] != last_group:
                if open_cards:
                    out.append("</div>")
                out.append(f'<h3>{escape(s["group"])}</h3><div class="cards">')
                open_cards = True
                last_group = s["group"]
            nch = s["chapter_count"]
            ch_label = "1 chapter" if nch == 1 else f"{nch} chapters"
            out.append(
                f'<a class="card" href="books/{s["stem"]}.html">'
                f'<span class="card-name">{escape(s["name"])}</span>'
                f'<span class="card-meta">{ch_label} · {s["words"]:,} words</span>'
                f"</a>"
            )
        if open_cards:
            out.append("</div>")
        return "".join(out)

    main = f"""
      <header class="hero">
        <div class="badge">World English Bible · public domain</div>
        <h1>Holy Bible</h1>
        <p>The whole Protestant canon in modern English, laid out like a book — chapters you can sit with, a sidebar that knows where you are, a jump box for John 3:16, and play or download audio for every chapter.</p>
        <div class="hero-actions">
          <a class="btn-fill" href="books/genesis.html#c-1">Begin Genesis</a>
          <a class="btn-ghost" href="overview.html">The whole story</a>
          <a class="btn-ghost" href="books/john.html#c-1">Open John</a>
          <a class="btn-ghost" id="resume-link" href="books/genesis.html" hidden>Continue reading</a>
        </div>
      </header>
      <p class="library-lead"><a href="overview.html">What each book is about →</a> Summaries and a chapter guide for every book, then the text itself. Each chapter has audio read by Winfred Henson — play in the page, or download the MP3.</p>
      <section class="library" id="library">
        {cards("ot", "Old Testament")}
        {cards("nt", "New Testament")}
      </section>
      <footer class="foot">
        World English Bible (public domain) · {len(stats)} books · {total_chapters:,} chapters ·
        audio: Winfred Henson, public domain ·
        <a href="../michael-book/">ΑΩ</a> · tyneside.software
      </footer>
    """
    return page_shell(
        title="Holy Bible — World English Bible",
        description="The whole Bible in modern English. World English Bible, public domain. Read with chapter navigation at tyneside.software/bible.",
        asset_prefix="",
        body_attrs='data-page="index"',
        toggle_label="Books",
        aside=aside,
        main=main,
    )


def render_book(
    spec: tuple,
    chapters: dict[int, dict],
    stats: list[dict],
    prev_book: dict | None,
    next_book: dict | None,
    built: str,
    book_meta: dict | None = None,
    audio_chapters: dict | None = None,
) -> str:
    name, stem, testament, group, aliases = spec
    nchap = max(chapters)
    words = sum(ch["words"] for ch in chapters.values())
    verses = sum(len(ch["verses"]) for ch in chapters.values())
    testament_label = "Old Testament" if testament == "ot" else "New Testament"
    kicker_book = "Psalm" if name == "Psalms" else name

    chap_nav = []
    for n in sorted(chapters):
        title = f"Psalm {n}" if name == "Psalms" else f"Chapter {n}"
        chap_nav.append(
            f'<a class="nav-item" href="#c-{n}" data-filter="{n} {title}">'
            f'<span class="n">{n}</span><span class="t">{escape(title)}</span></a>'
        )

    sections = []
    ordered = sorted(chapters)
    for i, n in enumerate(ordered):
        rec = chapters[n]
        heading = f"Psalm {n}" if name == "Psalms" else f"Chapter {n}"
        prev_link = (
            f'<a href="#c-{ordered[i-1]}">← {("Psalm" if name == "Psalms" else "Chapter")} {ordered[i-1]}</a>'
            if i
            else "<span></span>"
        )
        next_link = (
            f'<a href="#c-{ordered[i+1]}">{("Psalm" if name == "Psalms" else "Chapter")} {ordered[i+1]} →</a>'
            if i < len(ordered) - 1
            else "<span></span>"
        )
        url = ""
        if audio_chapters:
            url = str(audio_chapters.get(str(n)) or audio_chapters.get(n) or "")
        audio = chapter_audio_html(stem, name, n, url)
        sections.append(
            f'<article class="chapter" id="c-{n}">'
            f'<header class="ch-head">'
            f'<p class="kicker">{escape(kicker_book)}</p>'
            f"<h2>{escape(heading)}</h2>"
            f'<p class="meta">{len(rec["verses"])} verses · {rec["words"]:,} words · World English Bible</p>'
            f"{audio}"
            f"</header>"
            f'<div class="body">{"".join(rec["parts"])}</div>'
            f'<p class="ch-end">{prev_link}{next_link}</p>'
            f"</article>"
        )

    prev_html = (
        f'<a href="{prev_book["stem"]}.html">← {escape(prev_book["name"])}</a>'
        if prev_book
        else '<a href="../index.html">← All books</a>'
    )
    next_html = (
        f'<a href="{next_book["stem"]}.html">{escape(next_book["name"])} →</a>'
        if next_book
        else '<a href="../index.html">All books →</a>'
    )

    meta = book_meta or {}
    notes = meta.get("chapters") or []
    if notes and len(notes) != nchap:
        raise SystemExit(
            f"{stem}: chapter guide has {len(notes)} notes, book has {nchap} chapters"
        )
    about = about_html(meta)
    guide = chapter_guide_html(
        stem,
        name,
        notes,
        href_prefix="",
        details=False,
    )
    summary_block = ""
    if about or guide:
        summary_block = (
            f'<section class="book-summary" id="about">{about}{guide}</section>'
        )

    aside = f"""
    <div class="side-head">
      <div class="brand"><a href="../../index.html">tyneside.software</a> · <a href="../index.html">bible</a></div>
      <h1>{escape(name)}</h1>
      <p class="sub">{escape(testament_label)} · {escape(group)}</p>
      <div class="epigraph">World English Bible. Public domain modern English.</div>
      <div class="stats">
        <div><strong>{nchap}</strong> chapters</div>
        <div><strong>{verses:,}</strong> verses</div>
        <div><strong>{words:,}</strong> words</div>
        <div>{escape(built)}</div>
      </div>
      {jump_block()}
    </div>
    <nav class="nav" aria-label="Chapters">{"".join(chap_nav)}</nav>
    <p class="side-lib"><a href="../index.html">← All books</a> · <a href="../overview.html#{stem}">What this book is</a></p>
    """

    main = f"""
      <header class="hero">
        <div class="badge">{escape(testament_label)} · {escape(group)}</div>
        <h1>{escape(name)}</h1>
        <p>{nchap} chapters · {verses:,} verses · {words:,} words</p>
        <div class="hero-actions">
          <a class="btn-ghost" href="#guide">Chapter guide</a>
          <a class="btn-ghost" href="#c-1">Begin chapter 1</a>
          <a class="btn-ghost" href="../overview.html#{stem}">In the whole story</a>
        </div>
      </header>
      <nav class="book-nav" aria-label="Nearby books">{prev_html}{next_html}</nav>
      {summary_block}
      {"".join(sections)}
      <nav class="book-nav" aria-label="Nearby books">{prev_html}{next_html}</nav>
      <footer class="foot">
        {escape(name)} · World English Bible · audio: Winfred Henson (public domain) ·
        <a href="../overview.html#{stem}">Overview</a> · <a href="../index.html">Holy Bible</a>
      </footer>
    """
    return page_shell(
        title=f"{name} — World English Bible",
        description=f"{name} in the World English Bible. {nchap} chapters of public-domain modern English.",
        asset_prefix="../",
        body_attrs=(
            f'data-page="book" data-book="{stem}"'
            + (f' data-next="{next_book["stem"]}"' if next_book else "")
        ),
        toggle_label="Chapters",
        aside=aside,
        main=main,
    )


def write_readme() -> None:
    (OUT_DIR / "README.md").write_text(
        r"""# Holy Bible — World English Bible

**Live:** https://tyneside.software/bible/

Public-domain modern English. Same reader chrome as [michael-book](https://tyneside.software/michael-book/).

## Build

```powershell
cd C:\\Users\\MichaelThomson\\source\\TTS
python scripts/build_bible.py
python -m site_generator software
```

Writes `sites/software/static/bible/index.html`, `overview.html`, and `books/*.html`.
Book summaries live in `sites/software/bible-source/about.json` (merged into overview.json at build).
Chapter guides live in `sites/software/bible-source/chapter-guides/` (one note per chapter).
Chapter audio URLs live in `sites/software/static/bible/audio-manifest.json`
(refresh with `python scripts/fetch_bible_audio.py`). Files are streamed from
eBible.org — the zip is ~5.4 GB and does not belong in GitHub Pages.
The site generator copies `static/` into `output/software/bible/`.
Push `site-generator` `main` and CI publishes tyneside.software. If the token is missing: `.\scripts\deploy-pages.ps1 software`.

## Translation

[World English Bible](https://worldenglish.bible/) — public domain modern English
from the American Standard Version, with paragraph and poetic line data from
[TehShrike/world-english-bible](https://github.com/TehShrike/world-english-bible).
Sixty-six book Protestant canon. Not NIV/NLT/ESV.

## Audio

Each chapter has play and download. Source:
[Winfred Wardell Henson](https://ebible.org/eng-web/audio/) reading the classic
World English Bible. Professional voice artist, one narrator, public domain.
LibriVox 4.4/5 (97 ratings). Matches the on-page WEB text.
""",
        encoding="utf-8",
    )


def build() -> None:
    ensure_sources()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    built = _now()

    parsed: list[tuple[tuple, dict[int, dict]]] = []
    stats: list[dict] = []
    for spec in BOOKS:
        name, stem, testament, group, aliases = spec
        chapters = load_book(stem)
        parsed.append((spec, chapters))
        stats.append(
            {
                "name": name,
                "stem": stem,
                "testament": testament,
                "group": group,
                "aliases": aliases,
                "chapter_count": max(chapters),
                "words": sum(ch["words"] for ch in chapters.values()),
                "verses": sum(len(ch["verses"]) for ch in chapters.values()),
            }
        )
        print(f"  parsed {name}: {max(chapters)} ch, {stats[-1]['words']:,} words")

    write_canon(stats)
    total_chapters = sum(s["chapter_count"] for s in stats)
    total_words = sum(s["words"] for s in stats)
    overview = load_overview()
    audio = load_audio()
    audio_books = audio.get("books") or {}
    for s in stats:
        notes = audio_books.get(s["stem"]) or {}
        if len(notes) != s["chapter_count"]:
            raise SystemExit(
                f"{s['stem']}: audio has {len(notes)} files, book has {s['chapter_count']} chapters"
            )
    (OUT_DIR / "index.html").write_text(
        render_index(stats, total_chapters, total_words, built), encoding="utf-8"
    )
    (OUT_DIR / "overview.html").write_text(
        render_overview(stats, overview, total_chapters, total_words, built),
        encoding="utf-8",
    )

    for i, (spec, chapters) in enumerate(parsed):
        prev_book = stats[i - 1] if i else None
        next_book = stats[i + 1] if i < len(stats) - 1 else None
        html = render_book(
            spec,
            chapters,
            stats,
            prev_book,
            next_book,
            built,
            book_meta=(overview.get("books") or {}).get(spec[1]) or {},
            audio_chapters=audio_books.get(spec[1]) or {},
        )
        (BOOKS_DIR / f"{spec[1]}.html").write_text(html, encoding="utf-8")

    write_readme()
    print(f"Wrote {OUT_DIR}")
    print(f"Books: {len(stats)}  Chapters: {total_chapters}  Words: {total_words:,}")


if __name__ == "__main__":
    build()
