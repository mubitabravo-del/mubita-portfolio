"""
Web Portfolio - Computer Programming I (Semester 1, 2026)
Built with Flet Python Framework
Sections: Timeline | MATLAB Hub | Technical Blog | GitHub Evidence
"""

import flet as ft
from datetime import date

# ── Colour palette ──────────────────────────────────────────────────────────
BG        = "#0D0F14"
SURFACE   = "#161B25"
CARD      = "#1E2535"
ACCENT    = "#00C8FF"
ACCENT2   = "#FF6B35"
TEXT      = "#E8EDF5"
MUTED     = "#6B7A99"
SUCCESS   = "#00E5A0"
BORDER    = "#2A3348"

# ── Reusable helpers ─────────────────────────────────────────────────────────

def heading(text: str, size: int = 28, color: str = TEXT, weight=ft.FontWeight.BOLD):
    return ft.Text(text, size=size, color=color, weight=weight,
                   font_family="Courier New")

def label(text: str, size: int = 13, color: str = MUTED):
    return ft.Text(text, size=size, color=color)

def divider():
    return ft.Divider(height=1, color=BORDER)

def accent_bar():
    return ft.Container(width=40, height=3,
                        bgcolor=ACCENT,
                        border_radius=2,
                        margin=ft.margin.only(bottom=12))

def chip(text: str, color: str = ACCENT):
    return ft.Container(
        content=ft.Text(text, size=11, color=color, weight=ft.FontWeight.W_600),
        bgcolor=ft.colors.with_opacity(0.12, color),
        border=ft.border.all(1, ft.colors.with_opacity(0.35, color)),
        border_radius=20,
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
    )

def card(content, padding: int = 20):
    return ft.Container(
        content=content,
        bgcolor=CARD,
        border_radius=12,
        padding=padding,
        border=ft.border.all(1, BORDER),
    )

def section_title(icon: str, title: str):
    return ft.Column([
        ft.Row([
            ft.Text(icon, size=22),
            ft.Text("  " + title, size=22, color=TEXT,
                    weight=ft.FontWeight.BOLD, font_family="Courier New"),
        ]),
        ft.Container(
            width=60, height=3, bgcolor=ACCENT,
            border_radius=2, margin=ft.margin.only(top=6, bottom=18)
        )
    ])

# ── NAV BAR ──────────────────────────────────────────────────────────────────

def build_nav(active: str, on_nav):
    pages = [
        ("🏠", "Home"),
        ("📅", "Timeline"),
        ("📐", "MATLAB"),
        ("✍️", "Blog"),
        ("🐙", "GitHub"),
    ]
    items = []
    for icon, name in pages:
        is_active = name == active
        items.append(
            ft.GestureDetector(
                on_tap=lambda e, n=name: on_nav(n),
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(icon, size=18),
                        ft.Text(name, size=10,
                                color=ACCENT if is_active else MUTED,
                                weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.NORMAL),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                    bgcolor=ft.colors.with_opacity(0.15, ACCENT) if is_active else "transparent",
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=14, vertical=8),
                    border=ft.border.all(1, ft.colors.with_opacity(0.4, ACCENT)) if is_active else ft.border.all(1, "transparent"),
                )
            )
        )
    return ft.Container(
        content=ft.Row(items, alignment=ft.MainAxisAlignment.CENTER, spacing=4),
        bgcolor=ft.colors.with_opacity(0.85, SURFACE),
        border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
        padding=ft.padding.symmetric(vertical=10, horizontal=20),
    )

# ── HOME PAGE ────────────────────────────────────────────────────────────────

def home_page():
    stats = [
        ("15%", "CA Weight"),
        ("4",    "Sections"),
        ("30",   "Flet Marks"),
        ("8",    "MATLAB Certs"),
    ]
    stat_cards = [
        card(ft.Column([
            ft.Text(v, size=30, color=ACCENT, weight=ft.FontWeight.BOLD,
                    font_family="Courier New"),
            ft.Text(k, size=12, color=MUTED),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
             padding=16)
        for v, k in stats
    ]

    return ft.Column([
        ft.Container(height=30),

        # Hero
        ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("< WEB PORTFOLIO />", size=11, color=ACCENT,
                                    weight=ft.FontWeight.W_600, font_family="Courier New"),
                    bgcolor=ft.colors.with_opacity(0.12, ACCENT),
                    border=ft.border.all(1, ft.colors.with_opacity(0.3, ACCENT)),
                    border_radius=20,
                    padding=ft.padding.symmetric(horizontal=12, vertical=5),
                ),
                ft.Container(height=16),
                ft.Text("Your Name", size=42, color=TEXT,
                        weight=ft.FontWeight.BOLD, font_family="Courier New"),
                ft.Text("Computer Programming I  ·  Semester 1, 2026",
                        size=15, color=MUTED),
                ft.Container(height=8),
                ft.Text("Mechanical Engineering App  ·  Group Project Portfolio",
                        size=13, color=ft.colors.with_opacity(0.7, ACCENT)),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=30, horizontal=20),
            bgcolor=ft.colors.with_opacity(0.04, ACCENT),
            border_radius=16,
            border=ft.border.all(1, BORDER),
        ),

        ft.Container(height=24),

        # Stats row
        ft.Row(stat_cards, alignment=ft.MainAxisAlignment.CENTER,
               wrap=True, spacing=10, run_spacing=10),

        ft.Container(height=24),

        # Quick guide
        card(ft.Column([
            ft.Row([ft.Text("📋", size=16),
                    ft.Text("  Assessment Breakdown", size=15, color=TEXT,
                            weight=ft.FontWeight.BOLD)]),
            ft.Container(height=12),
            *[ft.Row([
                ft.Container(width=8, height=8, bgcolor=c, border_radius=4),
                ft.Text(f"  {sec}", size=13, color=TEXT, expand=True),
                ft.Text(f"{m} marks", size=13, color=c, weight=ft.FontWeight.W_600),
            ]) for sec, m, c in [
                ("Flet Implementation & Deployment",   30, ACCENT),
                ("GitHub Evidence & Documentation",    25, SUCCESS),
                ("Technical Blog & Video Content",     25, ACCENT2),
                ("MATLAB MathWorks Certificates (×8)", 20, "#C084FC"),
            ]],
        ], spacing=10)),

        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.CENTER)

# ── TIMELINE PAGE ────────────────────────────────────────────────────────────

TIMELINE_DATA = [
    (1,  "Project Kickoff",      "Set up GitHub repo, created branch structure, attended team planning meeting.",
     ["Team Planning", "Git Setup"]),
    (2,  "Requirements Analysis", "Analysed mechanical engineering module specs. Drafted data models for stress analysis inputs.",
     ["Analysis", "Documentation"]),
    (3,  "UI Scaffolding",        "Built base navigation and layout components in Flet. Established colour theme.",
     ["Flet", "UI Design"]),
    (4,  "Stress Calculator",     "Implemented σ = F/A formula widget with input validation and unit conversion.",
     ["Python", "Math"]),
    (5,  "MATLAB Courses 1–3",    "Completed MATLAB Onramp, Signal Processing Onramp, and Machine Learning Onramp.",
     ["MATLAB", "Learning"]),
    (6,  "Data Visualisation",    "Added matplotlib chart integration for force-displacement graphs.",
     ["Charts", "Integration"]),
    (7,  "Code Review Sprint",    "Reviewed 3 PRs from teammates. Fixed unit-conversion bug in torque module.",
     ["Code Review", "Bug Fix"]),
    (8,  "MATLAB Courses 4–6",    "Completed Deep Learning, Image Processing, and Statistics Onramps.",
     ["MATLAB", "Learning"]),
    (9,  "Blog Posts Draft",      "Wrote technical posts on OOP and recursion with LaTeX-style notation.",
     ["Documentation", "Blog"]),
    (10, "Testing & Deployment",  "Wrote unit tests, fixed edge cases, deployed portfolio as live web app.",
     ["Testing", "Deployment"]),
]

def timeline_page():
    rows = []
    for week, title, desc, tags in TIMELINE_DATA:
        rows.append(
            ft.Row([
                # Week bubble
                ft.Container(
                    content=ft.Text(f"W{week}", size=11, color=ACCENT,
                                    weight=ft.FontWeight.BOLD,
                                    font_family="Courier New"),
                    width=44, height=44,
                    bgcolor=ft.colors.with_opacity(0.12, ACCENT),
                    border=ft.border.all(1, ft.colors.with_opacity(0.4, ACCENT)),
                    border_radius=22,
                    alignment=ft.alignment.center,
                ),
                # Content
                ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=14, color=TEXT,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(desc, size=12, color=MUTED),
                        ft.Row([chip(t) for t in tags], wrap=True, spacing=6),
                    ], spacing=5),
                    expand=True,
                    bgcolor=CARD,
                    border_radius=10,
                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    border=ft.border.all(1, BORDER),
                ),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.START)
        )

    return ft.Column([
        ft.Container(height=20),
        section_title("📅", "Project Timeline"),
        ft.Text("Weekly log of individual contributions to the Mechanical Engineering App.",
                size=13, color=MUTED),
        ft.Container(height=16),
        ft.Column(rows, spacing=10),
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)

# ── MATLAB PAGE ──────────────────────────────────────────────────────────────

MATLAB_COURSES = [
    ("MATLAB Onramp",               True,  "Core syntax, variables, and scripts"),
    ("Signal Processing Onramp",    True,  "Filtering, FFT, and spectral analysis"),
    ("Machine Learning Onramp",     True,  "Classification and regression models"),
    ("Deep Learning Onramp",        True,  "Neural network fundamentals"),
    ("Image Processing Onramp",     True,  "Pixel operations and morphology"),
    ("Statistics and Machine Learning", True,  "Distributions and hypothesis testing"),
    ("Simulink Onramp",             False, "Model-based design and simulation"),
    ("Control Design Onramp",       False, "PID controllers and feedback systems"),
]

def matlab_page():
    total = sum(1 for _, done, _ in MATLAB_COURSES if done)
    pct   = int(total / 8 * 100)

    course_cards = []
    for name, done, desc in MATLAB_COURSES:
        course_cards.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text("✓" if done else "○", size=14,
                                        color=SUCCESS if done else MUTED,
                                        weight=ft.FontWeight.BOLD),
                        width=30, height=30,
                        bgcolor=ft.colors.with_opacity(0.15, SUCCESS if done else MUTED),
                        border_radius=15,
                        alignment=ft.alignment.center,
                    ),
                    ft.Column([
                        ft.Text(name, size=13, color=TEXT if done else MUTED,
                                weight=ft.FontWeight.W_600),
                        ft.Text(desc, size=11, color=MUTED),
                    ], spacing=2, expand=True),
                    chip("DONE" if done else "TODO",
                         color=SUCCESS if done else MUTED),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=CARD,
                border_radius=10,
                padding=ft.padding.symmetric(horizontal=14, vertical=12),
                border=ft.border.all(1, ft.colors.with_opacity(0.5, SUCCESS) if done else BORDER),
            )
        )

    return ft.Column([
        ft.Container(height=20),
        section_title("📐", "MATLAB Achievement Hub"),
        ft.Text("Verification of 8 MathWorks Learning Center short courses.",
                size=13, color=MUTED),
        ft.Container(height=16),

        # Progress card
        card(ft.Column([
            ft.Row([
                ft.Text(f"{total}/8 Courses Completed", size=15, color=TEXT,
                        weight=ft.FontWeight.W_600),
                ft.Text(f"{pct}%", size=15, color=SUCCESS,
                        weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            ft.Container(
                content=ft.Container(
                    width=0,  # set dynamically via ratio below
                    bgcolor=SUCCESS,
                    border_radius=4,
                    height=8,
                ),
                bgcolor=BORDER,
                border_radius=4,
                height=8,
            ),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        width=ft.PercentageWidth(pct / 100),
                        bgcolor=SUCCESS,
                        border_radius=4,
                        height=8,
                    )
                ]),
                bgcolor=BORDER,
                border_radius=4,
                height=8,
            ),
            ft.Container(height=6),
            ft.Text("Upload MathWorks certificate screenshots to the Evidence folder.",
                    size=11, color=MUTED),
        ])),

        ft.Container(height=16),
        ft.Column(course_cards, spacing=8),

        ft.Container(height=16),
        card(ft.Column([
            ft.Row([ft.Text("📎", size=14),
                    ft.Text("  How to add certificate proof", size=14, color=TEXT,
                            weight=ft.FontWeight.W_600)]),
            ft.Container(height=8),
            ft.Text(
                "1. Complete the course at learn.mathworks.com\n"
                "2. Download your certificate PDF\n"
                "3. Screenshot the badge/certificate\n"
                "4. Add the image file to your /assets/matlab/ folder\n"
                "5. Reference it in this section with ft.Image(src=...)",
                size=12, color=MUTED,
            ),
        ])),
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)

# ── BLOG PAGE ────────────────────────────────────────────────────────────────

BLOG_POSTS = [
    {
        "title": "Object-Oriented Programming in Engineering Apps",
        "date":  "Week 3",
        "tags":  ["OOP", "Python", "Design Patterns"],
        "body": (
            "Object-Oriented Programming (OOP) allows us to model real-world "
            "engineering entities as classes. In our Mechanical Engineering app, "
            "we created a Beam class that encapsulates material properties and "
            "exposes methods for stress and deflection calculations.\n\n"
            "Key formula used for normal stress:\n\n"
            "    σ = F / A\n\n"
            "where σ is normal stress (Pa), F is the applied force (N), and "
            "A is the cross-sectional area (m²). Using OOP, each Beam instance "
            "carries its own F and A, making multi-beam simulations clean and scalable."
        ),
        "video": "https://www.youtube.com/watch?v=JeznW_7DlB0",
    },
    {
        "title": "Recursion & Iterative Algorithms",
        "date":  "Week 5",
        "tags":  ["Recursion", "Algorithms", "Python"],
        "body": (
            "Recursion is a technique where a function calls itself with a "
            "simpler sub-problem. We used recursion in our app to traverse "
            "hierarchical engineering component trees.\n\n"
            "The total cost formula from the brief:\n\n"
            "    Total Cost = Σ (Qᵢ × Pᵢ) + Overheads\n\n"
            "We implemented this as a recursive sum over a Bill of Materials "
            "(BOM) tree, where each node can itself be a sub-assembly with its "
            "own components."
        ),
        "video": "https://www.youtube.com/watch?v=ngCos392W4w",
    },
    {
        "title": "Event-Driven Programming with Flet",
        "date":  "Week 6",
        "tags":  ["Flet", "Events", "UI"],
        "body": (
            "Flet uses an event-driven model — your code responds to user "
            "actions (button clicks, text input) rather than running top-to-bottom. "
            "Every interactive control accepts an on_click or on_change callback.\n\n"
            "In our stress calculator:\n\n"
            "    def calculate(e):\n"
            "        sigma = float(force.value) / float(area.value)\n"
            "        result.value = f'σ = {sigma:.2f} Pa'\n"
            "        page.update()\n\n"
            "This pattern keeps the UI responsive and separates logic from display."
        ),
        "video": "https://www.youtube.com/watch?v=qobTBTue9Ow",
    },
]

def blog_page():
    posts = []
    for p in BLOG_POSTS:
        posts.append(
            card(ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(p["title"], size=16, color=TEXT,
                                weight=ft.FontWeight.BOLD),
                        ft.Text(p["date"], size=11, color=MUTED),
                    ], expand=True),
                ]),
                ft.Container(height=8),
                ft.Row([chip(t, ACCENT2) for t in p["tags"]], wrap=True, spacing=6),
                ft.Container(height=10),
                ft.Text(p["body"], size=12, color=ft.colors.with_opacity(0.85, TEXT)),
                ft.Container(height=10),
                ft.Row([
                    ft.Text("🎬 Video: ", size=12, color=MUTED),
                    ft.Text(p["video"], size=12, color=ACCENT,
                            selectable=True),
                ]),
            ], spacing=4))
        )

    return ft.Column([
        ft.Container(height=20),
        section_title("✍️", "Technical Blog"),
        ft.Text("Confidence in Concepts — written explanations with mathematical notation.",
                size=13, color=MUTED),
        ft.Container(height=16),
        ft.Column(posts, spacing=14),
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)

# ── GITHUB PAGE ──────────────────────────────────────────────────────────────

COMMITS = [
    ("#a1b2c3", "Add Beam stress calculator widget",            "Week 4"),
    ("#d4e5f6", "Fix unit conversion bug in torque module",     "Week 7"),
    ("#789abc", "Implement Bill of Materials recursive parser", "Week 5"),
    ("#321fed", "Add matplotlib force-displacement chart",      "Week 6"),
    ("#cafe01", "Write unit tests for stress functions",        "Week 10"),
]

PRS = [
    ("PR #12", "Feature: stress analysis UI",   "Merged", SUCCESS),
    ("PR #19", "Fix: torque unit bug",           "Merged", SUCCESS),
    ("PR #23", "Review: teammate's chart code",  "Reviewed", ACCENT),
    ("PR #31", "Feature: BOM recursive parser",  "Merged", SUCCESS),
]

def github_page():
    commit_rows = [
        ft.Row([
            ft.Text(sha, size=11, color=ACCENT, font_family="Courier New"),
            ft.Text(msg, size=12, color=TEXT, expand=True),
            ft.Text(week, size=11, color=MUTED),
        ], spacing=12)
        for sha, msg, week in COMMITS
    ]

    pr_rows = [
        ft.Row([
            ft.Text(pr, size=12, color=ACCENT, font_family="Courier New", width=60),
            ft.Text(desc, size=12, color=TEXT, expand=True),
            chip(status, color),
        ], spacing=12)
        for pr, desc, status, color in PRS
    ]

    return ft.Column([
        ft.Container(height=20),
        section_title("🐙", "GitHub Evidence"),
        ft.Text("Individual contribution proof — commits, pull requests, and impact summary.",
                size=13, color=MUTED),
        ft.Container(height=16),

        # Commit history
        card(ft.Column([
            ft.Row([ft.Text("📝", size=14),
                    ft.Text("  Commit History", size=14, color=TEXT,
                            weight=ft.FontWeight.W_600)]),
            ft.Container(height=10),
            ft.Column(commit_rows, spacing=8),
            ft.Container(height=8),
            ft.Text("Replace SHA hashes above with your real commit IDs from GitHub.",
                    size=11, color=MUTED),
        ])),

        ft.Container(height=14),

        # PR logs
        card(ft.Column([
            ft.Row([ft.Text("🔀", size=14),
                    ft.Text("  Pull Request Log", size=14, color=TEXT,
                            weight=ft.FontWeight.W_600)]),
            ft.Container(height=10),
            ft.Column(pr_rows, spacing=8),
        ])),

        ft.Container(height=14),

        # Impact summary
        card(ft.Column([
            ft.Row([ft.Text("⚡", size=14),
                    ft.Text("  Impact Summary", size=14, color=TEXT,
                            weight=ft.FontWeight.W_600)]),
            ft.Container(height=10),
            ft.Text(
                "My primary contribution to the Mechanical Engineering app was the "
                "Stress Analysis module. I designed and implemented the Beam class "
                "(OOP), which uses σ = F/A and τ = T·r/J to compute normal and shear "
                "stress. I discovered and fixed a unit-conversion bug in the torque "
                "sub-module (PR #19) that caused incorrect N·m → kN·m scaling for "
                "inputs above 1000 N. I also built the recursive Bill of Materials "
                "parser that correctly aggregates nested sub-assembly costs using "
                "Σ(Qᵢ × Pᵢ) + Overheads. These contributions directly enabled the "
                "mechanical module to pass all integration tests in Week 10.",
                size=12,
                color=ft.colors.with_opacity(0.85, TEXT),
            ),
        ])),

        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)

# ── MAIN APP ─────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title       = "Web Portfolio – CP1 2026"
    page.bgcolor     = BG
    page.padding     = 0
    page.theme_mode  = ft.ThemeMode.DARK
    page.fonts       = {"Courier New": "https://fonts.gstatic.com/s/cousine/v27/d6lIkaiiRdih4SpP9Z8K6T4.woff2"}
    page.window_width  = 420
    page.window_height = 820

    state = {"page": "Home"}

    content_area = ft.Container(
        expand=True,
        padding=ft.padding.symmetric(horizontal=16),
    )

    def render(name: str):
        state["page"] = name
        pages = {
            "Home":     home_page,
            "Timeline": timeline_page,
            "MATLAB":   matlab_page,
            "Blog":     blog_page,
            "GitHub":   github_page,
        }
        content_area.content = pages[name]()
        nav_container.content = build_nav(name, render).content
        page.update()

    nav_container = ft.Container(
        content=build_nav("Home", render).content,
        bgcolor=ft.colors.with_opacity(0.85, SURFACE),
        border=ft.border.only(bottom=ft.BorderSide(1, BORDER)),
        padding=ft.padding.symmetric(vertical=10, horizontal=20),
    )

    content_area.content = home_page()

    page.add(
        ft.Column([
            nav_container,
            content_area,
        ], expand=True, spacing=0)
    )

ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8080)
