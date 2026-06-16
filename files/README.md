# Web Portfolio – Computer Programming I (Semester 1, 2026)
## Setup & Customisation Guide

---

## 1. Installation

```bash
# 1. Make sure Python 3.9+ is installed
python --version

# 2. Install Flet
pip install flet

# 3. Run locally (opens in browser at http://localhost:8080)
python portfolio.py
```

---

## 2. File Structure

```
portfolio/
├── portfolio.py          ← Main app (all sections)
├── README.md             ← This file
└── assets/
    ├── matlab/           ← Put your MathWorks certificate screenshots here
    │   ├── cert_matlab_onramp.png
    │   ├── cert_signal_processing.png
    │   └── ...
    └── github/           ← Put your commit/PR screenshots here
        ├── commit_history.png
        └── pr_log.png
```

---

## 3. What to Personalise (in portfolio.py)

### 🏠 Home Page
- Line ~96: Change `"Your Name"` → your actual name
- Line ~97: Update group project name if needed

### 📅 Timeline (TIMELINE_DATA, ~line 140)
```python
(week_number, "Title", "What you actually did that week", ["Tag1", "Tag2"]),
```
Fill in your real weekly contributions. Be specific — the marker checks this.

### 📐 MATLAB Hub (MATLAB_COURSES, ~line 188)
- Change `True` / `False` to reflect which courses you've actually completed
- Add certificate images using `ft.Image(src="assets/matlab/cert_name.png")`

### ✍️ Blog Posts (BLOG_POSTS, ~line 228)
- Update `"body"` with your own written explanation
- Replace `"video"` with real YouTube or Loom URLs
- Add more posts by copying the dict structure

### 🐙 GitHub Evidence (COMMITS & PRS, ~line 281)
- Replace SHA hashes (e.g. `"#a1b2c3"`) with your real commit IDs from GitHub
- Update commit messages and PR numbers to match your actual history
- Rewrite the Impact Summary paragraph with your specific contributions

---

## 4. Mathematical Notation

Since Flet doesn't render LaTeX, use Unicode characters directly in strings:

| Symbol | Unicode | Usage |
|--------|---------|-------|
| σ      | \u03c3  | Normal stress |
| τ      | \u03c4  | Shear stress |
| Σ      | \u03a3  | Summation |
| ×      | \u00d7  | Multiply |
| ᵢ      | \u1d62  | Subscript i |
| ²      | \u00b2  | Superscript 2 |
| ³      | \u00b3  | Superscript 3 |
| π      | \u03c0  | Pi |
| √      | \u221a  | Square root |
| ∫      | \u222b  | Integral |

**Example in a blog post body:**
```python
"body": "Normal stress: σ = F / A\nBending stress: σ = M·y / I",
```

---

## 5. Deploying as a Live Web App

### Option A – Flet Cloud (easiest)
```bash
pip install flet
flet publish portfolio.py
# Follow the prompts to get a live URL
```

### Option B – Run on a VPS / Replit
1. Upload portfolio.py to Replit or a server
2. Run: `python portfolio.py`
3. Expose port 8080 publicly
4. Share the URL with your lecturer

### Option C – GitHub Pages (static export)
```bash
flet build web
# Uploads the /build/web folder to GitHub Pages
```

---

## 6. Marks Checklist

| Category | Marks | What to check |
|----------|-------|---------------|
| Flet Implementation | 30 | App runs, all 4 sections navigate correctly |
| GitHub Evidence | 25 | Real commit SHAs, real PR numbers, specific impact summary |
| Blog & Video | 25 | 3+ posts, proper notation, working video links |
| MATLAB Certificates | 20 | 8 completed, certificates visible or linked |

---

## 7. Quick Tips

- **Don't leave placeholder text.** The marker will notice "Your Name" or fake commit SHAs.
- **Be specific in the Impact Summary.** Say *which bug* you fixed, *which formula* you implemented.
- **Blog videos** can be YouTube tutorials you watched — they show how you learned the concept.
- **Commit early and often** on GitHub so you have real evidence to screenshot.
- Run `python portfolio.py` after every change to check it looks correct before submitting.
