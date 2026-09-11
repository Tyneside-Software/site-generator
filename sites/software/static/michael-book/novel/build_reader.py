# -*- coding: utf-8 -*-
"""Build the ΑΩ web edition from novel/chapters/*.md — Perfect is the only bar."""
from __future__ import annotations

import html
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHAPTERS = ROOT / "chapters"
# Reader lives with the novel AND is copied to site static root for /michael-book/
OUT_LOCAL = ROOT / "index.html"
OUT_SITE = ROOT.parent / "index.html"  # sites/.../michael-book/index.html


def parse_chapter(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()
    num = 0
    m = re.search(r"ch-(\d+)", path.name)
    if m:
        num = int(m.group(1))
    title = path.stem
    body_lines: list[str] = []
    i = 0
    if lines and lines[0].startswith("# "):
        # # Chapter N
        i = 1
    if i < len(lines) and lines[i].startswith("## "):
        title = lines[i][3:].strip()
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    body = "\n".join(lines[i:]).strip()
    return {"num": num, "title": title, "body": body, "path": path.name}


def md_lite_to_html(text: str) -> str:
    """Minimal markdown: paragraphs, **bold**, *italic*, `code`, fenced code, ---."""
    # Extract fenced blocks
    fences: list[str] = []

    def save_fence(m: re.Match) -> str:
        fences.append(m.group(1))
        return f"\x00FENCE{len(fences) - 1}\x00"

    text = re.sub(r"```[^\n]*\n(.*?)```", save_fence, text, flags=re.DOTALL)

    parts = re.split(r"\n\s*\n", text)
    out: list[str] = []
    for part in parts:
        p = part.strip()
        if not p:
            continue
        if p.strip() == "---":
            out.append("<hr>")
            continue
        # single-line heading leftovers
        if p.startswith("#"):
            p = re.sub(r"^#+\s*", "", p)
        esc = html.escape(p)
        esc = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc)
        esc = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", esc)
        esc = re.sub(r"`([^`]+)`", r"<code>\1</code>", esc)
        esc = esc.replace("\n", "<br>\n")
        # restore fences
        for i, code in enumerate(fences):
            esc = esc.replace(
                f"\x00FENCE{i}\x00",
                f"<pre><code>{html.escape(code.rstrip())}</code></pre>",
            )
        if esc.startswith("<pre>"):
            out.append(esc)
        else:
            out.append(f"<p>{esc}</p>")
    return "\n".join(out)


def build() -> Path:
    files = sorted(CHAPTERS.glob("ch-*.md"), key=lambda p: parse_chapter(p)["num"])
    chapters = [parse_chapter(p) for p in files]
    total_words = sum(len(c["body"].split()) for c in chapters)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    nav = []
    sections = []
    for c in chapters:
        cid = f"ch-{c['num']:02d}"
        nav.append(
            f'<a class="nav-item" href="#{cid}">'
            f'<span class="n">{c["num"]}</span>'
            f'<span class="t">{html.escape(c["title"])}</span></a>'
        )
        body_html = md_lite_to_html(c["body"])
        w = len(c["body"].split())
        sections.append(
            f'<article class="chapter" id="{cid}">'
            f'<header class="ch-head">'
            f'<p class="kicker">Chapter {c["num"]}</p>'
            f'<h2>{html.escape(c["title"])}</h2>'
            f'<p class="meta">{w} words</p>'
            f"</header>"
            f'<div class="body">{body_html}</div>'
            f"</article>"
        )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>ΑΩ — by Me, God</title>
  <meta name="description" content="ΑΩ by Me, God. A comic philosophical novel in ninety-nine chapters.">
  <meta name="robots" content="noindex, nofollow, noarchive">
  <style>
    :root {{
      --bg: #0f1419;
      --panel: #1a222c;
      --border: #2c3a4a;
      --text: #e8eef4;
      --muted: #8b9aab;
      --accent: #e8b84a;
      --accent-dim: rgba(232, 184, 74, 0.12);
      --measure: 40rem;
      --serif: "Iowan Old Style", Palatino, Georgia, serif;
      --sans: "Segoe UI", system-ui, sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: var(--serif);
      background: var(--bg);
      color: var(--text);
      line-height: 1.7;
      min-height: 100vh;
    }}
    body::before {{
      content: "";
      position: fixed; inset: 0;
      background:
        radial-gradient(ellipse 70% 40% at 50% -8%, rgba(232,184,74,0.1), transparent),
        radial-gradient(ellipse 50% 30% at 100% 100%, rgba(80,120,180,0.06), transparent);
      pointer-events: none;
      z-index: -1;
    }}
    /* No z-index here — a stacking context was trapping the drawer under the backdrop */
    .shell {{
      position: relative;
      display: grid;
      grid-template-columns: minmax(0, 15rem) minmax(0, 1fr);
      max-width: 74rem;
      margin: 0 auto;
      min-height: 100vh;
    }}
    .side {{
      background: rgba(15,20,25,0.97);
      border-right: 1px solid var(--border);
      padding: 1.25rem 0.9rem 2rem;
      max-height: 100vh;
      overflow: auto;
    }}
    .side-spacer {{
      /* Holds the left grid column; real sidebar is position:fixed */
      min-height: 1px;
    }}
    /* Desktop: fixed sidebar aligned to centered 74rem shell */
    @media (min-width: 901px) {{
      .side {{
        position: fixed;
        top: 0;
        left: max(0px, calc((100vw - 74rem) / 2));
        width: 15rem;
        height: 100vh;
        z-index: 5;
        pointer-events: auto;
      }}
      .nav-toggle,
      .nav-close,
      .nav-backdrop {{
        display: none !important;
      }}
    }}
    .nav-toggle,
    .nav-close,
    .nav-backdrop {{
      display: none;
    }}
    @media (max-width: 900px) {{
      .shell {{ grid-template-columns: 1fr; }}
      .side-spacer {{ display: none; }}
      .main {{ padding-top: 4.25rem; }}
      .nav-toggle {{
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        position: fixed;
        top: 0.75rem;
        left: 0.75rem;
        z-index: 300;
        font-family: var(--sans);
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--accent);
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 999px;
        padding: 0.55rem 0.95rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
      }}
      .nav-toggle:active {{ transform: scale(0.98); }}
      /* Backdrop BELOW the drawer so chapter taps hit the links */
      .nav-backdrop {{
        display: block;
        position: fixed;
        inset: 0;
        z-index: 200;
        background: rgba(0,0,0,0.55);
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s ease;
      }}
      body.nav-open .nav-backdrop {{
        opacity: 1;
        pointer-events: auto;
      }}
      .side {{
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        width: min(20rem, 88vw);
        max-height: none;
        height: 100%;
        z-index: 250;
        border-right: 1px solid var(--border);
        border-bottom: none;
        padding-top: 3.25rem;
        transform: translateX(-105%);
        transition: transform 0.22s ease;
        box-shadow: 12px 0 40px rgba(0,0,0,0.45);
        -webkit-overflow-scrolling: touch;
        pointer-events: none; /* closed: do not intercept */
        overscroll-behavior: contain;
      }}
      body.nav-open .side {{
        transform: translateX(0);
        pointer-events: auto; /* open: links receive taps */
      }}
      body.nav-open {{
        overflow: hidden;
      }}
      .nav-close {{
        display: flex;
        align-items: center;
        justify-content: center;
        position: absolute;
        top: 0.65rem;
        right: 0.65rem;
        z-index: 2;
        width: 2.4rem;
        height: 2.4rem;
        border-radius: 999px;
        border: 1px solid var(--border);
        background: var(--panel);
        color: var(--text);
        font-family: var(--sans);
        font-size: 1.25rem;
        line-height: 1;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
      }}
      .side-head {{
        padding-right: 2.5rem;
      }}
      .nav {{
        max-height: none;
        padding-bottom: 3rem;
        position: relative;
        z-index: 1;
      }}
      .nav-item {{
        pointer-events: auto;
        cursor: pointer;
        touch-action: manipulation;
      }}
    }}
    .brand {{
      font-family: var(--sans);
      font-size: 0.68rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 0.5rem;
    }}
    .side h1 {{
      font-size: 1.5rem;
      font-weight: 600;
      letter-spacing: -0.02em;
      margin-bottom: 0.25rem;
    }}
    .side .sub {{
      font-family: var(--sans);
      font-size: 0.8rem;
      color: var(--muted);
      margin-bottom: 0.85rem;
    }}
    .epigraph {{
      font-family: var(--sans);
      font-size: 0.72rem;
      background: var(--accent-dim);
      border: 1px solid rgba(232,184,74,0.35);
      color: var(--accent);
      padding: 0.45rem 0.6rem;
      border-radius: 8px;
      margin-bottom: 0.85rem;
      line-height: 1.4;
    }}
    .stats {{
      font-family: var(--sans);
      font-size: 0.75rem;
      color: var(--muted);
      margin-bottom: 1rem;
      line-height: 1.45;
    }}
    .stats strong {{ color: var(--text); }}
    .nav {{
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
    }}
    .nav-item {{
      display: grid;
      grid-template-columns: 1.6rem 1fr;
      gap: 0.4rem;
      text-decoration: none;
      color: var(--text);
      font-family: var(--sans);
      font-size: 0.76rem;
      padding: 0.32rem 0.4rem;
      border-radius: 6px;
      border: 1px solid transparent;
      opacity: 1;
    }}
    /* Kill browser default purple/grey on visited anchors — they looked disabled */
    .nav-item:link,
    .nav-item:visited,
    .nav-item:active {{
      color: var(--text);
      opacity: 1;
    }}
    .nav-item .t {{
      color: var(--text);
      opacity: 1;
    }}
    .nav-item .n {{
      color: var(--accent);
      font-variant-numeric: tabular-nums;
      opacity: 1;
    }}
    .nav-item:hover,
    .nav-item:focus-visible {{
      color: #fff;
      background: var(--accent-dim);
      border-color: rgba(232,184,74,0.2);
      outline: none;
    }}
    .nav-item:hover .t,
    .nav-item:focus-visible .t {{
      color: #fff;
    }}
    .nav-item:hover .n,
    .nav-item:focus-visible .n {{
      color: var(--accent);
    }}
    .main {{ padding: 1.75rem 1.25rem 4rem; }}
    .hero {{
      max-width: var(--measure);
      margin: 0 auto 2.5rem;
      text-align: center;
    }}
    .hero .badge {{
      font-family: var(--sans);
      font-size: 0.68rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent);
      border: 1px solid rgba(232,184,74,0.3);
      background: var(--accent-dim);
      display: inline-block;
      padding: 0.3rem 0.65rem;
      border-radius: 999px;
      margin-bottom: 0.85rem;
    }}
    .hero h1 {{
      font-size: clamp(2rem, 5vw, 2.75rem);
      margin-bottom: 0.5rem;
    }}
    .hero p {{
      color: var(--muted);
      font-style: italic;
      font-size: 1.05rem;
    }}
    .chapter {{
      max-width: var(--measure);
      margin: 0 auto 3.25rem;
      padding-top: 0.25rem;
    }}
    .ch-head {{
      margin-bottom: 1.35rem;
      padding-bottom: 0.85rem;
      border-bottom: 1px solid var(--border);
    }}
    .kicker {{
      font-family: var(--sans);
      font-size: 0.7rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 0.25rem;
    }}
    .ch-head h2 {{
      font-size: 1.55rem;
      font-weight: 600;
      letter-spacing: -0.02em;
    }}
    .meta {{
      font-family: var(--sans);
      font-size: 0.72rem;
      color: var(--muted);
      margin-top: 0.3rem;
    }}
    .body p {{
      margin-bottom: 0.95rem;
      font-size: 1.08rem;
    }}
    .body p:last-child {{ margin-bottom: 0; }}
    .body strong {{ color: #fff8e7; }}
    .body em {{ color: #d5e0ea; }}
    .body code {{
      font-family: ui-monospace, Consolas, monospace;
      font-size: 0.92em;
      background: var(--panel);
      padding: 0.1em 0.35em;
      border-radius: 4px;
    }}
    .body pre {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 0.85rem 1rem;
      overflow: auto;
      margin: 0.85rem 0 1.1rem;
      font-size: 0.88rem;
    }}
    .body hr {{
      border: none;
      border-top: 1px solid var(--border);
      margin: 1.5rem 0;
    }}
    .foot {{
      max-width: var(--measure);
      margin: 0 auto;
      font-family: var(--sans);
      font-size: 0.8rem;
      color: var(--muted);
      border-top: 1px solid var(--border);
      padding-top: 1.1rem;
    }}
    .top {{
      position: fixed;
      right: 1rem;
      bottom: 1rem;
      font-family: var(--sans);
      font-size: 0.75rem;
      background: var(--panel);
      color: var(--accent);
      border: 1px solid var(--border);
      padding: 0.5rem 0.75rem;
      border-radius: 999px;
      text-decoration: none;
      z-index: 5;
      box-shadow: 0 8px 24px rgba(0,0,0,0.35);
    }}
    .top:hover {{ background: var(--accent-dim); }}
    @media (max-width: 900px) {{
      .top {{ bottom: 1rem; right: 1rem; left: auto; }}
    }}
  </style>
</head>
<body>
  <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="chapter-side">
    Chapters
  </button>
  <div class="nav-backdrop" id="nav-backdrop" hidden></div>
  <!-- Drawer is a direct child of body so it is never under the dimmer layer -->
  <aside class="side" id="chapter-side" aria-label="Chapter navigation">
    <button type="button" class="nav-close" id="nav-close" aria-label="Close chapters">×</button>
    <div class="side-head">
      <div class="brand">tyneside.software · michael-book</div>
      <h1>ΑΩ</h1>
      <p class="sub">by Me, God</p>
      <div class="epigraph">
        Ninety-nine chapters. Experience exists. No pure outside.
        Ends: <em>It's a funny old life.</em>
      </div>
      <div class="stats">
        <div><strong>{len(chapters)}</strong> chapters</div>
        <div><strong>{total_words:,}</strong> words</div>
        <div>{html.escape(now)}</div>
      </div>
    </div>
    <nav class="nav" aria-label="Chapters">
      {"".join(nav)}
    </nav>
  </aside>
  <div class="shell">
    <div class="side-spacer" aria-hidden="true"></div>
    <main class="main">
      <header class="hero">
        <div class="badge">by Me, God</div>
        <h1>ΑΩ</h1>
        <p>From experience exists to a funny old life — both/and all the way down.</p>
      </header>
      {"".join(sections)}
      <footer class="foot">
        ΑΩ · by Me, God · ninety-nine chapters · the only kitchen · the dual monogram · the funny old life.
      </footer>
    </main>
  </div>
  <a class="top" href="#">Top</a>
  <script>
    (function () {{
      var body = document.body;
      var toggle = document.getElementById("nav-toggle");
      var closeBtn = document.getElementById("nav-close");
      var backdrop = document.getElementById("nav-backdrop");
      var side = document.getElementById("chapter-side");
      if (!toggle || !side) return;

      function isMobileNav() {{
        return window.matchMedia("(max-width: 900px)").matches;
      }}

      function openNav() {{
        body.classList.add("nav-open");
        toggle.setAttribute("aria-expanded", "true");
        if (backdrop) {{
          backdrop.hidden = false;
        }}
      }}
      function closeNav() {{
        body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
        if (backdrop) {{
          backdrop.hidden = true;
        }}
      }}

      toggle.addEventListener("click", function (e) {{
        e.preventDefault();
        e.stopPropagation();
        if (body.classList.contains("nav-open")) closeNav();
        else openNav();
      }});
      if (closeBtn) {{
        closeBtn.addEventListener("click", function (e) {{
          e.preventDefault();
          e.stopPropagation();
          closeNav();
        }});
      }}
      if (backdrop) {{
        backdrop.addEventListener("click", function (e) {{
          e.preventDefault();
          closeNav();
        }});
      }}

      // Chapter pick: navigate, then close drawer on phone
      side.querySelectorAll("a.nav-item").forEach(function (a) {{
        a.addEventListener("click", function () {{
          if (isMobileNav()) {{
            // allow hash navigation, then close after a tick
            setTimeout(closeNav, 10);
          }}
        }});
      }});

      document.addEventListener("keydown", function (e) {{
        if (e.key === "Escape") closeNav();
      }});

      window.addEventListener("resize", function () {{
        if (!isMobileNav()) closeNav();
      }});
    }})();
  </script>
</body>
</html>
"""
    OUT_LOCAL.write_text(page, encoding="utf-8")
    OUT_SITE.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT_LOCAL}")
    print(f"Wrote {OUT_SITE}")
    print(f"Chapters: {len(chapters)}  Words: {total_words}")
    return OUT_SITE


if __name__ == "__main__":
    build()
