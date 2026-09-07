# tyneside.academy

Aspirational brand site. Domain is held; **not a school and not taking pupils**.

What is already happening: Michael is tutoring his son Lewis for **early GCSEs**. Lewis wants to sit **Computer Science first**. The course map is `computer-science.html` (OCR J277). Each unit is a full open lesson in `sites/academy/cs/` (teach + exercises + quiz, no gates). Multiple-choice mocks that auto-score live at `cs/mock.html`. Lewis is also building a website of everything he has learned.

Possible next steps, both still ideas:

1. Do something with Lewis’s notes site (publish, share, grow it).
2. Tutor other children for money — perhaps as a group.

Different from [tyneside.software/school.html](https://tyneside.software/school.html) (the Mr Merrit one-day-a-month proposal) and from [tyneside.games](https://tyneside.games/) (Lewis’s one-night games shelf).

Listed on the group sketchbook: [tyneside.group/next.html](https://tyneside.group/next.html).

## Local preview

```powershell
python -m site_generator academy
```

Open `output/academy/index.html` or `output/academy/computer-science.html`.

## When it is ready to stand with the others

1. Set `aspirational=False` on the `academy` entry in `src/site_generator/sites.py`.
2. Add a live doorway on `templates/group_home.html`.
3. Point DNS for `tyneside.academy` at GitHub Pages.
4. Enable Pages on this repo (`main` / root).
