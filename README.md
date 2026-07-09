# 🔐 Password Strength Checker

---

## What This Project Does

A password strength checker that classifies any password as **WEAK**, **MEDIUM**, or **STRONG** based on:
- Length validation (< 8 chars = immediate fail)
- Character variety: uppercase, lowercase, digits, symbols
- Detection of commonly used / leaked passwords
- Detection of repeated character patterns

Built in **Python** (core logic + CLI), **Pandas** (batch CSV analysis), and **C++** (alternate implementation).

---

## Project Structure

```
password-strength-checker/
│
├── python/
│   ├── checker.py       ← Core strength logic (functions)
│   ├── main.py          ← Interactive CLI (Python)
│   └── analyze.py       ← Batch CSV analysis using Pandas
│
├── cpp/
│   └── checker.cpp      ← Full C++ implementation
│
├── tests/
│   └── test_checker.py  ← Unit tests (21 test cases)
│
├── data/
│   └── sample_passwords.csv  ← Sample input for batch analysis
│
├── reports/             ← Auto-generated after running analyze.py
│   └── (output CSVs go here)
│
├── requirements.txt
└── README.md
```

---

## How to Run

### Python — Interactive CLI
```bash
cd python
python main.py
```
Type a password when prompted (input is hidden via `getpass`).

### Python — Single Password Check
```bash
python main.py MyPassword123!
```

### Pandas — Batch Analysis
```bash
cd python
python analyze.py ../data/sample_passwords.csv
```
Generates a detailed + summary CSV in `/reports/`.

### C++ — Compile & Run
```bash
cd cpp
g++ -std=c++17 -o checker checker.cpp
./checker
```

### Run Tests
```bash
cd tests
python test_checker.py
# or with pytest:
python -m pytest test_checker.py -v
```

---

## Strength Classification Logic

| Score | Result |
|-------|--------|
| 0–3   | WEAK   |
| 4–5   | MEDIUM |
| 6–7   | STRONG |

**Scoring breakdown:**
- Length ≥ 8:  +1 point
- Length ≥ 12: +2 points
- Length ≥ 16: +3 points
- Uppercase letter present: +1
- Lowercase letter present: +1
- Digit present: +1
- Symbol present: +1
- Common/leaked password: score reset to 0
- Repeated characters (3+ same in a row): −1

---

## Key Concepts Used

- **String handling** — Python's `.isupper()`, `.isdigit()`, `string.punctuation`
- **Pythonic `any()`** — short-circuit evaluation instead of verbose loops
- **`hmac.compare_digest()`** — constant-time comparison to prevent timing attacks
- **Pandas** — batch processing, `.apply()`, groupby aggregations, CSV I/O
- **C++ STL** — `std::set`, `std::transform`, character classification with `<cctype>`
- **O(n) linear scan** — validation time grows linearly, not exponentially

---

## Sample Output

```
=======================================================
   🔐  PASSWORD STRENGTH CHECKER
=======================================================

Enter password: ********

—————————————————————————————————————————
  Password   : ************
  Length     : 12 characters
  Score      : 6 / 7

  ✅  STRONG PASSWORD — Good to go
—————————————————————————————————————————

  Character Mix:
    Uppercase : ✓
    Lowercase : ✓
    Numbers   : ✓
    Symbols   : ✓

  Suggestions:
    → Password looks solid. Good work!
```

---

## Requirements

```
pandas>=1.5.0
```

Python 3.8+ required. C++17 for the C++ version.

---

## Why This Matters

> 81% of hacking-related breaches leverage weak or stolen passwords.
> Average breach cost: $4.24M. (Source: Verizon DBIR)

Password validation is the **gatekeeper before encryption**. A weak password, no matter how well it's hashed, is a security liability.

---
