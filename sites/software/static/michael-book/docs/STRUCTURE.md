# ΑΩ — Structure

## Title plate

- **ΑΩ**  
- **by Me, God**  
- Scripture UI at `/michael-book/` until path rename

## Verse engine (published text)

Each verse is **paradoxical assertion(s)** that are **true in a frame**.

- **No** closing resolution paragraph.  
- **No** “this is not really a paradox.”  
- Reader concludes. God states.

## Chapter files

Same Markdown pattern; body verses should look like:

```markdown
## 1
I am the wave and I am the point. Measure me one way and I spread. Measure me another and I hit.

## 2
You are free. You are a machine of causes. Both of these sentences are how mornings feel.
```

Not:

```markdown
## 1
Paradox: …
Actually it is not a paradox because …
```

## Intensity / 65 pages

See `OBJECTIVE.md`. Endgame chapters hold heat + ^& + body dual. Early chapters: soft prefigure only (`leak: none` or `soft-prefigure`).

## Word budgets

Still sum toward **11,500** unless Master retargets for true 65-page density.

## Build

```powershell
python scripts/michael_book_stats.py
python scripts/build_michael_book.py
```
