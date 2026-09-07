"""Build audio-manifest.json from Winfred Henson's WEB chapter MP3s.

Professional single-narrator recording (LibriVox 4.4/5). Public domain.
Chapter files live at https://ebible.org/eng-web/audio/

eBible forbids directory listing from some clients (HTTP 403) but serves
the files and the 5.4 GB zip. This script reads the zip central directory
with a Range request so it never downloads the audio.

Usage:
  python scripts/fetch_bible_audio.py
"""
from __future__ import annotations

import json
import re
import struct
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sites" / "software" / "static" / "bible" / "audio-manifest.json"
INDEX = "https://ebible.org/eng-web/audio/"
ZIP_URL = INDEX + "eng-web_audio.zip"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

STEMS = [
    "genesis", "exodus", "leviticus", "numbers", "deuteronomy",
    "joshua", "judges", "ruth", "1samuel", "2samuel",
    "1kings", "2kings", "1chronicles", "2chronicles", "ezra",
    "nehemiah", "esther", "job", "psalms", "proverbs",
    "ecclesiastes", "songofsolomon", "isaiah", "jeremiah", "lamentations",
    "ezekiel", "daniel", "hosea", "joel", "amos",
    "obadiah", "jonah", "micah", "nahum", "habakkuk",
    "zephaniah", "haggai", "zechariah", "malachi",
    "matthew", "mark", "luke", "john", "acts",
    "romans", "1corinthians", "2corinthians", "galatians", "ephesians",
    "philippians", "colossians", "1thessalonians", "2thessalonians",
    "1timothy", "2timothy", "titus", "philemon", "hebrews",
    "james", "1peter", "2peter", "1john", "2john", "3john", "jude",
    "revelation",
]

EXPECTED = {
    "genesis": 50, "exodus": 40, "leviticus": 27, "numbers": 36, "deuteronomy": 34,
    "joshua": 24, "judges": 21, "ruth": 4, "1samuel": 31, "2samuel": 24,
    "1kings": 22, "2kings": 25, "1chronicles": 29, "2chronicles": 36, "ezra": 10,
    "nehemiah": 13, "esther": 10, "job": 42, "psalms": 150, "proverbs": 31,
    "ecclesiastes": 12, "songofsolomon": 8, "isaiah": 66, "jeremiah": 52,
    "lamentations": 5, "ezekiel": 48, "daniel": 12, "hosea": 14, "joel": 3,
    "amos": 9, "obadiah": 1, "jonah": 4, "micah": 7, "nahum": 3, "habakkuk": 3,
    "zephaniah": 3, "haggai": 2, "zechariah": 14, "malachi": 4,
    "matthew": 28, "mark": 16, "luke": 24, "john": 21, "acts": 28,
    "romans": 16, "1corinthians": 16, "2corinthians": 13, "galatians": 6,
    "ephesians": 6, "philippians": 4, "colossians": 4, "1thessalonians": 5,
    "2thessalonians": 3, "1timothy": 6, "2timothy": 4, "titus": 3, "philemon": 1,
    "hebrews": 13, "james": 5, "1peter": 5, "2peter": 3, "1john": 5,
    "2john": 1, "3john": 1, "jude": 1, "revelation": 22,
}

ONES = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
}
TENS = {
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
    "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90,
}


def request(url: str, *, headers: dict | None = None, timeout: int = 60):
    last: Exception | None = None
    base = {
        "User-Agent": UA,
        "Accept": "*/*",
        "Referer": INDEX,
    }
    if headers:
        base.update(headers)
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers=base)
            return urllib.request.urlopen(req, timeout=timeout)
        except Exception as exc:  # noqa: BLE001
            last = exc
            import time

            time.sleep(1.5 * (attempt + 1))
    raise last or RuntimeError(url)


def get(url: str) -> str:
    with request(url) as resp:
        return resp.read().decode("utf-8", "replace")


class HrefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        for k, v in attrs:
            if k == "href" and v:
                self.hrefs.append(v)


def hrefs(html: str) -> list[str]:
    p = HrefParser()
    p.feed(html)
    return p.hrefs


def words_to_int(tokens: list[str]) -> int | None:
    n = 0
    hundred = 0
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t == "hundred":
            hundred = (hundred or 1) * 100
            i += 1
            continue
        if t in TENS:
            hundred += TENS[t]
            i += 1
            continue
        if t in ONES:
            hundred += ONES[t]
            i += 1
            continue
        i += 1
    n += hundred
    return n or None


def chapter_from_name(name: str) -> int | None:
    """Chapter number from Henson's messy filenames.

    Prefer English words after Chapter / Psalms. Do not treat the second
    underscore number as the chapter — 1 Samuel ch.1 is
    ``09_37_First_Samuel_Chapter_One.mp3`` (37 is a catalogue id).
    """
    raw = urllib.parse.unquote(name)
    raw = re.sub(r"\.mp3$", "", raw, flags=re.I)
    base = Path(raw.replace("\\", "/")).name
    if re.search(r"\(\d+\)\s*$", base):
        return None
    stem = base.replace("_", " ").replace("-", " ")
    low = stem.lower()
    skip = {
        "chapter", "psalm", "psalms", "revelations", "revelation",
        "genesis", "exodus", "the", "of", "and", "first", "second", "third",
        "samuel", "kings", "chronicles", "corinthians", "thessalonians",
        "timothy", "peter", "john", "song", "solomon",
    }
    if "chapter" in low:
        tail = low.split("chapter", 1)[1]
        m = re.search(r"\d+", tail)
        if m:
            n = int(m.group(0))
            if 1 <= n <= 150:
                return n
        tokens = [t for t in re.findall(r"[a-z]+", tail) if t not in skip]
        n = words_to_int(tokens)
        if n:
            return n
    if "psalm" in low:
        parts = re.split(r"psalms|psalm", low, maxsplit=1)
        tail = parts[-1] if len(parts) > 1 else low
        tokens = [t for t in re.findall(r"[a-z]+", tail) if t not in skip]
        n = words_to_int(tokens)
        if n:
            return n
    m = re.search(r"(?:^|/)\d{2}_(\d{1,3})_", name)
    if m:
        n = int(m.group(1))
        if 1 <= n <= 150:
            return n
    return None


def sort_key(filename: str) -> tuple:
    raw = urllib.parse.unquote(filename)
    base = Path(raw.replace("\\", "/")).name
    m = re.search(r"(?:^|/)\d{2}_(\d{1,3})_", filename)
    if m:
        return (0, int(m.group(1)), raw)
    m = re.match(r"^(\d{2,4})\b", base.strip())
    if m:
        return (1, int(m.group(1)), raw)
    nums = re.findall(r"\d+", base)
    if nums:
        return (2, int(nums[-1] if len(nums) > 1 else nums[0]), raw)
    return (3, 0, raw)


def pick_files(names: list[str], want: int) -> list[str]:
    mp3s = [n for n in names if n.lower().endswith(".mp3")]
    mp3s = [n for n in mp3s if "(1)" not in urllib.parse.unquote(n)]
    by_ch: dict[int, str] = {}
    for n in mp3s:
        ch = chapter_from_name(n)
        if ch and 1 <= ch <= want and ch not in by_ch:
            by_ch[ch] = n
    if len(by_ch) == want:
        return [by_ch[i] for i in range(1, want + 1)]
    missing = [i for i in range(1, want + 1) if i not in by_ch]
    ordered = sorted(mp3s, key=sort_key)
    if len(by_ch) + len([x for x in ordered if x not in by_ch.values()]) >= want and missing:
        leftovers = [x for x in ordered if x not in by_ch.values()]
        for ch, name in zip(missing, leftovers):
            by_ch[ch] = name
        if len(by_ch) == want:
            return [by_ch[i] for i in range(1, want + 1)]
    if len(ordered) >= want:
        return ordered[:want]
    raise SystemExit(
        f"only {len(ordered)} mp3s, want {want}; parsed {len(by_ch)} "
        f"(missing {missing[:12]})"
    )


def zip_names(url: str = ZIP_URL) -> list[str]:
    """Filenames from a ZIP/ZIP64 central directory via Range request."""
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Referer": INDEX}, method="HEAD"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        length = resp.headers.get("Content-Length")
    if not length:
        raise SystemExit("zip has no Content-Length")
    size = int(length)
    print(f"zip: {size} bytes", flush=True)

    tail_len = min(size, 4 * 1024 * 1024)
    start = size - tail_len
    with request(url, headers={"Range": f"bytes={start}-{size - 1}"}, timeout=120) as resp:
        tail = resp.read()
    if len(tail) < 22:
        raise SystemExit("zip tail too small")

    sig_eocd = b"PK\x05\x06"
    pos = tail.rfind(sig_eocd)
    if pos < 0:
        raise SystemExit("zip EOCD not found")
    comment_len = struct.unpack_from("<H", tail, pos + 20)[0]
    if pos + 22 + comment_len > len(tail):
        raise SystemExit("zip EOCD truncated")

    cd_size = struct.unpack_from("<I", tail, pos + 12)[0]
    cd_offset = struct.unpack_from("<I", tail, pos + 16)[0]
    n_entries = struct.unpack_from("<H", tail, pos + 10)[0]

    if cd_size == 0xFFFFFFFF or cd_offset == 0xFFFFFFFF or n_entries == 0xFFFF:
        loc_sig = b"PK\x06\x07"
        loc = tail.rfind(loc_sig, 0, pos)
        if loc < 0:
            raise SystemExit("zip64 locator not found")
        zip64_off = struct.unpack_from("<Q", tail, loc + 8)[0]
        rel = zip64_off - start
        if rel < 0 or rel + 56 > len(tail):
            with request(
                url,
                headers={"Range": f"bytes={zip64_off}-{zip64_off + 128}"},
                timeout=60,
            ) as resp:
                z64 = resp.read()
            rel = 0
            rec = z64
        else:
            rec = tail[rel:]
        if rec[:4] != b"PK\x06\x06":
            raise SystemExit("zip64 EOCD missing")
        n_entries = struct.unpack_from("<Q", rec, 32)[0]
        cd_size = struct.unpack_from("<Q", rec, 40)[0]
        cd_offset = struct.unpack_from("<Q", rec, 48)[0]

    print(f"zip: {n_entries} entries, cd {cd_size} bytes at {cd_offset}", flush=True)
    cd_end = cd_offset + cd_size - 1
    if cd_offset >= start:
        cd = tail[cd_offset - start : cd_offset - start + cd_size]
    else:
        with request(url, headers={"Range": f"bytes={cd_offset}-{cd_end}"}, timeout=120) as resp:
            cd = resp.read()
    if len(cd) < cd_size:
        raise SystemExit(f"central directory short: {len(cd)} < {cd_size}")

    names: list[str] = []
    i = 0
    while i + 46 <= len(cd):
        if cd[i : i + 4] != b"PK\x01\x02":
            break
        fn_len, extra_len, comm_len = struct.unpack_from("<HHH", cd, i + 28)
        name = cd[i + 46 : i + 46 + fn_len].decode("utf-8", "replace")
        names.append(name)
        i += 46 + fn_len + extra_len + comm_len
    print(f"zip: parsed {len(names)} names", flush=True)
    return names


def book_index_from_path(path: str) -> int | None:
    rel = path.replace("\\", "/").lstrip("/")
    m = re.match(r"(?:.*/)?(\d{2})_[^/]+/", rel)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d{2})_", Path(rel).name)
    if m:
        return int(m.group(1))
    return None


def url_for(path: str, folders: dict[int, str]) -> str:
    rel = path.replace("\\", "/").lstrip("/")
    # zip may store 01_Genesis/file.mp3 or file.mp3
    if "/" in rel:
        folder, name = rel.rsplit("/", 1)
        folder = folder.split("/")[-1] + "/"
        return urllib.parse.urljoin(INDEX, folder) + urllib.parse.quote(name)
    idx = book_index_from_path(rel)
    if idx and idx in folders:
        return urllib.parse.urljoin(folders[idx], urllib.parse.quote(rel))
    return urllib.parse.urljoin(INDEX, urllib.parse.quote(rel))


def list_folders() -> dict[int, str]:
    index = get(INDEX)
    folders: dict[int, str] = {}
    for h in hrefs(index):
        m = re.match(r"^(\d{2})_[^/]+/$", h)
        if m:
            folders[int(m.group(1))] = urllib.parse.urljoin(INDEX, h)
    if len(folders) != 66:
        raise SystemExit(f"expected 66 book folders, got {sorted(folders)}")
    return folders


def books_from_zip(folders: dict[int, str]) -> dict[str, dict[str, str]]:
    names = zip_names()
    mp3s = [n for n in names if n.lower().endswith(".mp3") and not n.endswith("/")]
    by_book: dict[int, list[str]] = {i: [] for i in range(1, 67)}
    unmatched: list[str] = []
    for n in mp3s:
        idx = book_index_from_path(n)
        if idx and 1 <= idx <= 66:
            by_book[idx].append(n)
        else:
            unmatched.append(n)
    if unmatched:
        print(f"warning: {len(unmatched)} mp3s with no book index", flush=True)
        for n in unmatched[:8]:
            print(f"  {n}", flush=True)

    books: dict[str, dict[str, str]] = {}
    for i, stem in enumerate(STEMS, 1):
        want = EXPECTED[stem]
        chosen = pick_files(by_book[i], want)
        books[stem] = {
            str(ch): url_for(name, folders)
            for ch, name in enumerate(chosen, 1)
        }
        print(f"  {stem}: {want} ok  e.g. {Path(chosen[0]).name}", flush=True)
    return books


def books_from_listings(folders: dict[int, str]) -> dict[str, dict[str, str]]:
    books: dict[str, dict[str, str]] = {}
    partial = OUT.with_suffix(".partial.json")
    if partial.is_file():
        try:
            prev = json.loads(partial.read_text(encoding="utf-8"))
            if isinstance(prev, dict):
                books.update(prev)
                print(f"resume {len(books)} books", flush=True)
        except json.JSONDecodeError:
            books = {}
    for i, stem in enumerate(STEMS, 1):
        if stem in books and len(books[stem]) == EXPECTED[stem]:
            print(f"  {stem}: skip", flush=True)
            continue
        folder = folders[i]
        html = get(folder)
        names = [h for h in hrefs(html) if h.lower().endswith(".mp3")]
        want = EXPECTED[stem]
        chosen = pick_files(names, want)
        books[stem] = {
            str(ch): urllib.parse.urljoin(folder, name)
            for ch, name in enumerate(chosen, 1)
        }
        partial.write_text(json.dumps(books, ensure_ascii=False), encoding="utf-8")
        print(f"  {stem}: {want} ok  e.g. {chosen[0]}", flush=True)
    if partial.is_file():
        partial.unlink()
    return books


def main() -> None:
    folders = list_folders()
    try:
        books = books_from_zip(folders)
    except Exception as exc:  # noqa: BLE001
        print(f"zip listing failed ({exc!r}); falling back to folder crawl", flush=True)
        books = books_from_listings(folders)

    n = sum(len(v) for v in books.values())
    if n != 1189:
        raise SystemExit(f"expected 1189 chapters, got {n}")
    payload = {
        "source": {
            "name": "World English Bible, read by Winfred Wardell Henson",
            "list_url": INDEX,
            "license": "Public domain",
            "audio_by": "Winfred Wardell Henson (professional voice artist)",
            "text_by": "eBible.org",
            "reviews": "LibriVox 4.4/5 from 97 ratings; one narrator for the whole Bible",
            "note": (
                "Human reading of the classic World English Bible (matches the on-page text, "
                "including Yahweh). American English. Public domain. "
                "Chosen over the British Edition recording, which was poorly read."
            ),
        },
        "chapter_count": n,
        "books": books,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({n} chapters, {len(books)} books)", flush=True)


if __name__ == "__main__":
    main()
