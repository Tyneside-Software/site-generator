# Practical programming

Not a third exam paper. OCR still expects **real coding hours**. Paper 2 will punish anyone who has only *read* about loops.

Lewis already ships games. This page is **exam-shaped Python** and **Exam Reference Language** — the boring cousin of `tyneside.games`. Jump to any kata.

## Python — the three constructs {#t-py-core}

Type these. Do not only read them.

**Sequence**

```python
print("Tyneside")
print("Academy")
```

**Selection**

```python
age = int(input("Age? "))
if age >= 16:
    print("GCSE sitting is plausible")
elif age >= 13:
    print("Early sitting needs a plan")
else:
    print("Plenty of time")
```

**Iteration — count**

```python
for n in range(1, 6):
    print(n * n)
```

**Iteration — condition**

```python
secret = "tyne"
guess = ""
while guess != secret:
    guess = input("Password: ")
print("In")
```

**Nesting** — a times table is the classic:

```python
for row in range(1, 5):
    line = ""
    for col in range(1, 5):
        line = line + str(row * col) + "\t"
    print(line)
```

If you can trace that nested loop on paper, Section B gets easier.

## Python — strings, lists, files, functions {#t-py-extra}

**Strings:** `s[0]`, `s[-1]`, `s[2:5]`, `len(s)`, `s.lower()`, `s.split()`, `s.replace("a", "o")`.

**Lists (1D arrays):**

```python
scores = [8, 3, 9]
scores.append(7)
print(scores[0], len(scores), sum(scores))
```

**2D:**

```python
board = [
    [".", ".", "."],
    [".", "X", "."],
    [".", ".", "O"],
]
print(board[1][1])  # X
```

**Function:**

```python
def clamp(n, lo, hi):
    if n < lo:
        return lo
    if n > hi:
        return hi
    return n
```

**File (read all lines):**

```python
with open("highscores.txt", "r") as f:
    for line in f:
        print(line.strip())
```

`with` closes the file even if you error — nicer than GCSE ERL, still worth using.

## OCR Exam Reference Language {#t-erl}

Paper 2 is allowed in Python **or** ERL. Learn both so a question never looks foreign.

Common ERL shapes:

```
x = int(input("x"))
if x MOD 2 == 0 then
  print("even")
else
  print("odd")
endif

for i = 0 to 4
  print(i)
next i

while x > 0
  x = x - 1
endwhile

array names[2]
names[0] = "Lewis"
print(names[0])

function double(n)
  return n * 2
endfunction
```

**MOD** is `%`. **DIV** is `//`. `==` for compare. `=` for assign. `then` / `endif` / `next i` are the visual difference from Python.

Translate one way then the other: Python → ERL → Python. That is the exercise.

## Trace tables and dry-runs {#t-trace}

Every Section B has a “what is the output” or “complete the table”.

Rules:

1. One column per variable (and output)
2. New row when **any** of them change
3. Conditions get a True/False column if they control a loop
4. Do not skip the last failing `while` check

```python
a = 1
b = 1
for _ in range(5):
    c = a + b
    a = b
    b = c
print(a, b)
```

That is Fibonacci-ish. Trace it. Final print is the point.

## Paper 2 Section B scenarios {#t-section-b}

A typical paper: a **story** (library, game, shop), some data stored in arrays, then:

- Finish a procedure  
- Fix a logic error  
- Write a validation loop  
- Compute a total / max / count  
- Maybe a 2D array or a file  

**Method:**

1. Underline **inputs, processes, outputs**  
2. Name the arrays and their indexes as the paper does — do not invent a different structure  
3. Write **ERL or Python consistently**  
4. Trace your own answer once with their sample data  
5. Validation and sensible names are cheap marks  

There is **no time gate** on this site. In the real hall you have 90 minutes for the **whole** of Paper 2. When you want pressure, set a kitchen timer yourself — the page will not do it to you.

---

Katas below. Pick any. Reveal a model. Then change the model (different limit, 2D, file) so it is yours.
