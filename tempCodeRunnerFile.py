"""
Web Portfolio - Computer Programming I (Semester 1, 2026)
Flet 0.84 compatible

HOW TO RUN:
    pip install flet
    python portfolio.py

FOLDER STRUCTURE:
    portfolio/
    ├── portfolio.py
    └── assets/
        └── matlab/
            ├── cert_matlab_onramp.png
            ├── cert_signal_processing.png
            ├── cert_machine_learning.png
            ├── cert_deep_learning.png
            ├── cert_image_processing.png
            ├── cert_statistics.png
            ├── cert_simulink.png
            └── cert_control_design.png

FIXES APPLIED (vs original):
    1. ft.Image fit= changed from ft.ImageFit.CONTAIN  →  "contain"  (string literal)
       ft.ImageFit enum does not exist in Flet ≤ 0.84; use plain strings instead.
    2. ft.app()  →  ft.run()
       ft.app() was deprecated in Flet 0.80.0; ft.run() is the correct call.
"""

import flet as ft

# ─────────────────────────────────────────────────────────────────────────────
# DESIGN TOKENS
# ─────────────────────────────────────────────────────────────────────────────
BG       = "#08090D"
SURFACE  = "#0F1218"
CARD     = "#13161F"
CARD2    = "#191E2B"
ACCENT   = "#4DFFD2"
ACCENT2  = "#FF5F6D"
ACCENT3  = "#FFD166"
TEXT     = "#EEF1F8"
MUTED    = "#5A6480"
SUCCESS  = "#3BFFA0"
WARN     = "#FFB347"
BORDER   = "#1E2535"
PURPLE   = "#B57BFF"
BLUE     = "#4D9FFF"

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def wo(opacity, color):
    return ft.Colors.with_opacity(opacity, color)

def chip(text, color=ACCENT):
    return ft.Container(
        content=ft.Text(text, size=10, color=color, weight=ft.FontWeight.W_700,
                        font_family="monospace"),
        bgcolor=wo(0.12, color),
        border=ft.Border.all(1, wo(0.4, color)),
        border_radius=ft.BorderRadius.all(4),
        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
    )

def divider():
    return ft.Container(height=1, bgcolor=BORDER, margin=ft.Margin.symmetric(vertical=12))

def card(content, pad=16, border_color=BORDER, accent_top=None):
    top_accent = ft.Container(
        height=3,
        bgcolor=accent_top,
        border_radius=ft.BorderRadius.only(top_left=10, top_right=10),
    ) if accent_top else ft.Container(height=0)
    return ft.Container(
        content=ft.Column([top_accent, ft.Container(content=content, padding=ft.Padding.all(pad))], spacing=0),
        bgcolor=CARD,
        border_radius=ft.BorderRadius.all(10),
        border=ft.Border.all(1, border_color),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
    )

def section_title(icon, title, subtitle=None):
    children = [
        ft.Row([
            ft.Container(
                content=ft.Text(icon, size=20),
                width=42, height=42,
                bgcolor=wo(0.12, ACCENT),
                border_radius=ft.BorderRadius.all(10),
                alignment=ft.Alignment(0, 0),
            ),
            ft.Column([
                ft.Text(title, size=20, color=TEXT, weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=11, color=MUTED) if subtitle else ft.Container(height=0),
            ], spacing=1),
        ], spacing=12),
        ft.Container(height=2, bgcolor=wo(0.25, ACCENT),
                     border_radius=ft.BorderRadius.all(1),
                     margin=ft.Margin.only(top=10, bottom=16)),
    ]
    return ft.Column(children, spacing=0)

def mono_box(text):
    return ft.Container(
        content=ft.Text(text, size=12, color=ACCENT3, font_family="monospace"),
        bgcolor=wo(0.07, ACCENT3),
        border=ft.Border(left=ft.BorderSide(3, ACCENT3)),
        border_radius=ft.BorderRadius.only(top_right=6, bottom_right=6),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        margin=ft.Margin.symmetric(vertical=6),
    )

def stat_card(value, label, color):
    return ft.Container(
        content=ft.Column([
            ft.Text(value, size=26, color=color, weight=ft.FontWeight.BOLD),
            ft.Text(label, size=10, color=MUTED, text_align=ft.TextAlign.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
        bgcolor=CARD,
        border=ft.Border.all(1, wo(0.3, color)),
        border_radius=ft.BorderRadius.all(10),
        padding=ft.Padding.symmetric(horizontal=18, vertical=14),
        width=90,
    )

def info_row(label, value, color=TEXT):
    return ft.Row([
        ft.Text(label, size=11, color=MUTED, width=100),
        ft.Text(value, size=11, color=color, weight=ft.FontWeight.W_600),
    ], spacing=8)

# ─────────────────────────────────────────────────────────────────────────────
# TOP BAR
# ─────────────────────────────────────────────────────────────────────────────

def build_topbar():
    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text("< CP1 />", size=13, color=ACCENT, weight=ft.FontWeight.BOLD,
                                font_family="monospace"),
                bgcolor=wo(0.1, ACCENT),
                border_radius=ft.BorderRadius.all(6),
                padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                border=ft.Border.all(1, wo(0.3, ACCENT)),
            ),
            ft.Text("Web Portfolio  ·  2026", size=11, color=MUTED),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor=SURFACE,
        padding=ft.Padding.symmetric(horizontal=16, vertical=10),
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
    )

# ─────────────────────────────────────────────────────────────────────────────
# NAV BAR
# ─────────────────────────────────────────────────────────────────────────────

NAV_PAGES = [("🏠", "Home"), ("📅", "Timeline"), ("📐", "MATLAB"), ("✍️", "Blog"), ("🐙", "GitHub")]

# ─────────────────────────────────────────────────────────────────────────────
# HOME PAGE
# ─────────────────────────────────────────────────────────────────────────────

def home_page():
    breakdown = [
        ("Flet Implementation & Deployment",    30, ACCENT),
        ("GitHub Evidence & Documentation",     25, SUCCESS),
        ("Technical Blog & Video Content",      25, ACCENT2),
        ("MATLAB MathWorks Certificates (×8)",  20, PURPLE),
    ]

    bar_rows = []
    for label, marks, color in breakdown:
        bar_rows.append(ft.Column([
            ft.Row([
                ft.Text(label, size=11, color=TEXT, expand=True),
                ft.Text(f"{marks}", size=11, color=color, weight=ft.FontWeight.BOLD),
            ]),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        expand=marks, height=5, bgcolor=color,
                        border_radius=ft.BorderRadius.all(3),
                    ),
                    ft.Container(expand=100 - marks, height=5),
                ], spacing=0),
                bgcolor=BORDER,
                border_radius=ft.BorderRadius.all(3),
                height=5,
                clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
        ], spacing=5))

    return ft.Column([
        ft.Container(height=20),

        ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text("COMPUTER PROGRAMMING I  ·  2026",
                                    size=9, color=ACCENT, weight=ft.FontWeight.W_700,
                                    font_family="monospace"),
                    bgcolor=wo(0.1, ACCENT),
                    border_radius=ft.BorderRadius.all(4),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                ),
                ft.Container(height=16),
                ft.Text("Mubita Bravo", size=32, color=TEXT, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                ft.Text("Mechanical Engineering App", size=13, color=wo(0.8, ACCENT)),
                ft.Text("Individual Web Portfolio  ·  Group Project", size=11, color=MUTED),
                ft.Container(height=20),
                ft.Row([
                    stat_card("15%", "CA Weight", ACCENT),
                    stat_card("100", "Total Marks", SUCCESS),
                    stat_card("8", "MATLAB Certs", PURPLE),
                    stat_card("10", "Weeks", ACCENT2),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=wo(0.04, ACCENT),
            border=ft.Border.all(1, wo(0.18, ACCENT)),
            border_radius=ft.BorderRadius.all(14),
            padding=ft.Padding.symmetric(vertical=28, horizontal=20),
        ),

        ft.Container(height=20),

        card(ft.Column([
            ft.Row([
                ft.Text("📋", size=14),
                ft.Text("  Assessment Breakdown", size=14, color=TEXT, weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                chip("100 marks", ACCENT3),
            ]),
            ft.Container(height=14),
            ft.Column(bar_rows, spacing=12),
        ])),

        ft.Container(height=20),

        card(ft.Column([
            ft.Row([ft.Text("ℹ️", size=14),
                    ft.Text("  Portfolio Info", size=13, color=TEXT, weight=ft.FontWeight.W_600)]),
            divider(),
            info_row("Framework", "Flet (Python)", ACCENT),
            info_row("Deployment", "Live Web App", SUCCESS),
            info_row("Semester", "1, 2026", TEXT),
            info_row("Module", "CP1 Group Project", TEXT),
            info_row("Team Size", "20 Members", WARN),
        ], spacing=8)),

        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.CENTER)

# ─────────────────────────────────────────────────────────────────────────────
# TIMELINE PAGE
# ─────────────────────────────────────────────────────────────────────────────

TIMELINE_DATA = [
    (1,  "Project Kickoff",
     "Set up GitHub repository, created personal branch, attended team planning meeting, agreed on folder structure and naming conventions.",
     ["Git Setup", "Team Planning"], ACCENT),
    (2,  "Requirements Analysis",
     "Analysed mechanical engineering module specifications. Drafted class diagrams and data models for the Beam stress analysis sub-module.",
     ["Analysis", "Documentation"], BLUE),
    (3,  "UI Scaffolding",
     "Built base navigation component and colour theme in Flet. Established responsive layout skeleton shared across all team members.",
     ["Flet", "UI Design"], ACCENT),
    (4,  "Stress Calculator",
     "Implemented the σ = F/A stress calculator widget with input validation, unit conversion (N→kN, m²→mm²), and live result display.",
     ["Python", "Math"], ACCENT2),
    (5,  "MATLAB Courses 1–3",
     "Completed MATLAB Onramp, Signal Processing Onramp, and Machine Learning Onramp on MathWorks Learning Center. Screenshots archived.",
     ["MATLAB", "Learning"], SUCCESS),
    (6,  "Data Visualisation",
     "Integrated matplotlib for force-displacement graphs. Charts rendered inside Flet via ft.Image from in-memory PNG buffers.",
     ["Charts", "Integration"], ACCENT3),
    (7,  "Code Review Sprint",
     "Reviewed 3 pull requests from teammates, left inline comments, and fixed the unit-conversion bug (N·m → kN·m) in the torque module.",
     ["Code Review", "Bug Fix"], WARN),
    (8,  "MATLAB Courses 4–6",
     "Completed Deep Learning Onramp, Image Processing Onramp, and Statistics & Machine Learning Onramp. Progress: 6/8.",
     ["MATLAB", "Learning"], SUCCESS),
    (9,  "Technical Blog Posts",
     "Wrote three technical blog posts covering OOP, recursion, and event-driven programming, each with embedded YouTube video references.",
     ["Documentation", "Blog"], PURPLE),
    (10, "Testing & Deployment",
     "Wrote pytest unit tests for stress functions, resolved edge cases, and deployed the portfolio as a live web app on port 8080.",
     ["Testing", "Deployment"], ACCENT),
]

def timeline_page():
    rows = []
    for week, title, desc, tags, color in TIMELINE_DATA:
        rows.append(
            ft.Row([
                ft.Column([
                    ft.Container(
                        content=ft.Text(f"W{week}", size=10, color=color,
                                        weight=ft.FontWeight.BOLD, font_family="monospace"),
                        width=36, height=36,
                        bgcolor=wo(0.14, color),
                        border=ft.Border.all(1, wo(0.45, color)),
                        border_radius=ft.BorderRadius.all(18),
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Container(width=2, expand=True, bgcolor=wo(0.12, color),
                                 margin=ft.Margin.only(left=17)) if week < 10
                    else ft.Container(expand=True),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0,
                   width=36),
                ft.Container(
                    content=ft.Column([
                        ft.Text(title, size=13, color=TEXT, weight=ft.FontWeight.BOLD),
                        ft.Container(height=4),
                        ft.Text(desc, size=11, color=MUTED),
                        ft.Container(height=6),
                        ft.Row([chip(t, color) for t in tags], wrap=True, spacing=5),
                    ], spacing=0),
                    expand=True,
                    bgcolor=wo(0.05, color),
                    border_radius=ft.BorderRadius.all(10),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=12),
                    border=ft.Border.all(1, wo(0.2, color)),
                    margin=ft.Margin.only(bottom=4),
                ),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START)
        )

    return ft.Column([
        ft.Container(height=20),
        section_title("📅", "Project Timeline",
                      "Weekly log of individual contributions to the Mechanical Engineering App"),
        ft.Column(rows, spacing=2),
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)

# ─────────────────────────────────────────────────────────────────────────────
# MATLAB PAGE
# ─────────────────────────────────────────────────────────────────────────────

MATLAB_COURSES = [
    ("MATLAB Onramp",                    True,  "Core syntax, variables, scripts, and basic plotting",   "matlab/cert_matlab_onramp.png",           ACCENT),
    ("Calculation with Vectors",         True,  "Vector operations, indexing, and array mathematics",    "matlab/CalculationwithVectors.png",        BLUE),
    ("Machine Learning Onramp",          True,  "Classification, regression, and model evaluation",      "matlab/machineLearning.png",               SUCCESS),
    ("Explore Data",                     True,  "Data import, cleaning, and exploratory analysis",       "matlab/ExploreData.png",                   PURPLE),
    ("Finite Element",                   True,  "FEA fundamentals and structural simulation",            "matlab/FiniteElement.png",                 ACCENT2),
    ("How and Why",                      True,  "Engineering reasoning and problem-solving techniques",  "matlab/HowandWhy.png",                     ACCENT3),
    ("Simulink Onramp",                  True,  "Model-based design, block diagrams, simulation",        "matlab/simulinkOnramp.png",                PURPLE),
    ("MATLAB Onramp (Extended)",         False, "Advanced scripting, functions, and file I/O",           "matlab/matlabOnramp.png",                  MUTED),
]

def matlab_page(open_lightbox=None):
    done_count = sum(1 for _, done, *_ in MATLAB_COURSES if done)
    pct = int(done_count / 8 * 100)

    course_rows = []
    for name, done, desc, asset, color in MATLAB_COURSES:
        c = color if done else MUTED
        course_rows.append(ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text("\u2713" if done else "\u25cb", size=12, color=c,
                                    weight=ft.FontWeight.BOLD),
                    width=32, height=32,
                    bgcolor=wo(0.15, c),
                    border_radius=ft.BorderRadius.all(16),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Column([
                    ft.Text(name, size=12, color=TEXT if done else MUTED,
                            weight=ft.FontWeight.W_600),
                    ft.Text(desc, size=10, color=MUTED),
                ], spacing=2, expand=True),
                chip("DONE" if done else "TODO", c),
            ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=wo(0.05, c),
            border_radius=ft.BorderRadius.all(8),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            border=ft.Border.all(1, wo(0.25, c)),
        ))

    cert_items = []
    for name, done, _, asset, color in MATLAB_COURSES:
        c = color if done else MUTED

        def make_tap(a, n):
            def _tap(e):
                if open_lightbox:
                    open_lightbox(a, n)
            return _tap

        thumb = ft.Container(
            content=ft.Column([
                ft.GestureDetector(
                    on_tap=make_tap(asset, name) if done else None,
                    content=ft.Stack([
                        ft.Container(
                            content=ft.Image(
                                src=asset,
                                width=176, height=140,
                                fit="cover",
                                border_radius=ft.BorderRadius.all(8),
                                error_content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("\U0001f3c5", size=32),
                                        ft.Text(name, size=9, color=c,
                                                text_align=ft.TextAlign.CENTER,
                                                max_lines=2),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                       spacing=6),
                                    width=176, height=140,
                                    bgcolor=wo(0.08, c),
                                    border_radius=ft.BorderRadius.all(8),
                                    alignment=ft.Alignment(0, 0),
                                ),
                            ),
                        ),
                        # zoom hint badge top-right
                        ft.Container(
                            content=ft.Text("\U0001f50d", size=14),
                            right=6, top=6,
                            bgcolor=wo(0.55, BG),
                            border_radius=ft.BorderRadius.all(6),
                            padding=ft.Padding.all(3),
                            visible=done,
                        ),
                    ]),
                ),
                ft.Container(height=6),
                ft.Text(name, size=10, color=c,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=2, weight=ft.FontWeight.W_600),
                ft.Text("tap to expand" if done else "not done",
                        size=8, color=wo(0.5, c),
                        text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            width=184,
            bgcolor=wo(0.04, c),
            border=ft.Border.all(2, wo(0.5, c) if done else wo(0.15, c)),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.all(4),
        )
        cert_items.append(thumb)

    return ft.Column([
        ft.Container(height=20),
        section_title("\U0001f4d0", "MATLAB Achievement Hub",
                      "Verification of 8 MathWorks Learning Center short courses"),

        card(ft.Column([
            ft.Row([
                ft.Text(f"{done_count}/8 Completed", size=13, color=TEXT,
                        weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                ft.Text(f"{pct}%", size=18, color=SUCCESS, weight=ft.FontWeight.BOLD),
            ]),
            ft.Container(height=10),
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        expand=pct, height=8, bgcolor=SUCCESS,
                        border_radius=ft.BorderRadius.only(
                            top_left=4, bottom_left=4,
                            top_right=4 if pct == 100 else 0,
                            bottom_right=4 if pct == 100 else 0,
                        ),
                    ),
                    ft.Container(expand=100 - pct, height=8),
                ], spacing=0),
                bgcolor=BORDER, border_radius=ft.BorderRadius.all(4),
                height=8, clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Container(height=6),
            ft.Text(
                "All 8 complete \u2014 20 marks secured \u2713" if pct == 100
                else f"{8 - done_count} remaining \u2014 visit learn.mathworks.com",
                size=11, color=SUCCESS if pct == 100 else MUTED,
            ),
        ]), accent_top=SUCCESS),

        ft.Container(height=14),
        ft.Column(course_rows, spacing=6),
        ft.Container(height=20),

        card(ft.Column([
            ft.Row([
                ft.Text("\U0001f3c5", size=15),
                ft.Text("  Certificate Evidence", size=14, color=TEXT,
                        weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                ft.Text("tap any cert to expand", size=9, color=MUTED),
            ]),
            ft.Container(height=14),
            ft.Row(cert_items, wrap=True, spacing=10, run_spacing=12),
        ])),

        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=8,
       horizontal_alignment=ft.CrossAxisAlignment.START)


# ─────────────────────────────────────────────────────────────────────────────
# BLOG PAGE
# ─────────────────────────────────────────────────────────────────────────────

BLOG_POSTS = [
    {
        "title": "Object-Oriented Programming in Engineering Apps",
        "date":  "Week 3",
        "tags":  ["OOP", "Python", "Design Patterns"],
        "color": ACCENT,
        "sections": [
            {
                "heading": "Why OOP for Engineering?",
                "body": (
                    "Object-Oriented Programming lets us model physical entities directly in code. "
                    "In our Mechanical Engineering app, a Beam is not just a dictionary of values — "
                    "it is a fully-fledged object that owns its material properties and exposes "
                    "methods for every calculation it supports."
                ),
            },
            {
                "heading": "The Beam Class",
                "body": (
                    "Each Beam instance stores force (F) and cross-sectional area (A). "
                    "Calling beam.normal_stress() returns the normal stress σ in Pascals, "
                    "encapsulating the formula and its units internally."
                ),
            },
            {
                "heading": "Normal Stress Formula",
                "formula": "σ = F / A\n\nwhere  σ = normal stress (Pa)\n       F = applied force (N)\n       A = cross-sectional area (m²)",
            },
            {
                "heading": "Code Sketch",
                "formula": (
                    "class Beam:\n"
                    "    def __init__(self, force, area):\n"
                    "        self.F = force   # N\n"
                    "        self.A = area    # m²\n\n"
                    "    def normal_stress(self):\n"
                    "        return self.F / self.A  # Pa"
                ),
            },
            {
                "body": (
                    "Encapsulating F and A inside the class means multi-beam simulations are "
                    "clean and scalable: create a list of Beam objects, call normal_stress() on "
                    "each, and collect results — no global variables, no naming collisions."
                ),
            },
        ],
        "video": "⚠️  REPLACE THIS — paste your own YouTube/video link here (screen recording of you explaining OOP)",
    },
    {
        "title": "Recursion & Iterative Algorithms",
        "date":  "Week 5",
        "tags":  ["Recursion", "Algorithms", "Python"],
        "color": ACCENT2,
        "sections": [
            {
                "heading": "What is Recursion?",
                "body": (
                    "Recursion is when a function calls itself with a simpler sub-problem until "
                    "it reaches a base case. It is natural for tree-shaped data like a hierarchical "
                    "Bill of Materials (BOM), where each node may itself be a sub-assembly."
                ),
            },
            {
                "heading": "Total Cost Formula",
                "formula": (
                    "        n\n"
                    "Cost = Σ (Qᵢ × Pᵢ)  +  Overheads\n"
                    "       i=1\n\n"
                    "Qᵢ = quantity of component i\n"
                    "Pᵢ = unit price of component i"
                ),
            },
            {
                "heading": "Recursive BOM Parser",
                "formula": (
                    "def bom_cost(node):\n"
                    "    if node['type'] == 'part':\n"
                    "        return node['qty'] * node['price']\n"
                    "    return sum(bom_cost(child)\n"
                    "               for child in node['children'])\n"
                    "           + node.get('overhead', 0)"
                ),
            },
            {
                "body": (
                    "The recursive approach mirrors the BOM tree structure exactly — no "
                    "manual stack management is required. The base case (a leaf 'part' node) "
                    "terminates the descent, and the call-stack naturally unwinds to accumulate "
                    "costs up to the root assembly."
                ),
            },
        ],
        "video": "⚠️  REPLACE THIS — paste your own YouTube/video link here (screen recording of you explaining Recursion)",
    },
    {
        "title": "Event-Driven Programming with Flet",
        "date":  "Week 6",
        "tags":  ["Flet", "Events", "UI"],
        "color": PURPLE,
        "sections": [
            {
                "heading": "The Event-Driven Model",
                "body": (
                    "Unlike a top-to-bottom script, a Flet app waits for user actions — "
                    "button clicks, text changes, slider moves — and responds via callback "
                    "functions. This keeps the UI always responsive and cleanly separates "
                    "business logic from display code."
                ),
            },
            {
                "heading": "Stress Calculator Callback",
                "formula": (
                    "def calculate(e):\n"
                    "    F = float(force_field.value)  # N\n"
                    "    A = float(area_field.value)   # m²\n"
                    "    sigma = F / A                 # Pa\n"
                    "    result_label.value = (\n"
                    "        f'σ = {sigma:,.2f} Pa'\n"
                    "    )\n"
                    "    page.update()\n\n"
                    "calc_btn = ft.ElevatedButton(\n"
                    "    'Calculate', on_click=calculate\n"
                    ")"
                ),
            },
            {
                "heading": "Why page.update()?",
                "body": (
                    "Flet batches UI changes for performance. Calling page.update() commits "
                    "all pending control changes to the browser in a single diff, ensuring "
                    "the result label appears instantly after the user taps the button — "
                    "even across a network when deployed as a web app."
                ),
            },
        ],
        "video": "⚠️  REPLACE THIS — paste your own YouTube/video link here (screen recording of you explaining Flet events)",
    },
]

def blog_page():
    posts = []
    for p in BLOG_POSTS:
        color = p["color"]
        section_widgets = []
        for sec in p["sections"]:
            if "heading" in sec:
                section_widgets.append(
                    ft.Text(sec["heading"], size=12, color=color,
                            weight=ft.FontWeight.W_700)
                )
            if "body" in sec:
                section_widgets.append(
                    ft.Text(sec["body"], size=12, color=wo(0.85, TEXT))
                )
            if "formula" in sec:
                section_widgets.append(mono_box(sec["formula"]))

        posts.append(card(ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Text(p["date"], size=9, color=color,
                                    weight=ft.FontWeight.W_700, font_family="monospace"),
                    bgcolor=wo(0.12, color),
                    border_radius=ft.BorderRadius.all(4),
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                ),
                ft.Row([chip(t, color) for t in p["tags"]], spacing=4, wrap=True),
            ], spacing=8, wrap=True),
            ft.Container(height=6),
            ft.Text(p["title"], size=15, color=TEXT, weight=ft.FontWeight.BOLD),
            divider(),
            ft.Column(section_widgets, spacing=8),
            divider(),
            ft.Container(
                content=ft.Row([
                    ft.Text("▶ ", size=12, color=color),
                    ft.Text("Video Reference: ", size=11, color=MUTED),
                    ft.Text(p["video"], size=10, color=ACCENT, selectable=True,
                            expand=True),
                ]),
                bgcolor=wo(0.06, color),
                border_radius=ft.BorderRadius.all(6),
                padding=ft.Padding.symmetric(horizontal=10, vertical=8),
                border=ft.Border.all(1, wo(0.2, color)),
            ),
        ], spacing=6), accent_top=color))

    return ft.Column([
        ft.Container(height=20),
        section_title("✍️", "Technical Blog",
                      "Confidence in Concepts — written explanations with mathematical notation"),
        ft.Column(posts, spacing=16),
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)

# ─────────────────────────────────────────────────────────────────────────────
# GITHUB PAGE
# ─────────────────────────────────────────────────────────────────────────────

COMMITS = [
    ("a1b2c3d", "feat: add Beam stress calculator widget",             "Week 4",  ACCENT),
    ("d4e5f67", "fix: unit conversion bug in torque module (N·m→kN·m)","Week 7",  ACCENT2),
    ("789abcd", "feat: implement BOM recursive cost parser",           "Week 5",  SUCCESS),
    ("321fedc", "feat: add matplotlib force-displacement chart",       "Week 6",  ACCENT3),
    ("cafe012", "test: write pytest unit tests for stress functions",  "Week 10", PURPLE),
]

PULL_REQUESTS = [
    ("PR #12", "Feature: stress analysis UI",          "Merged",   SUCCESS,  "Author"),
    ("PR #19", "Fix: torque unit conversion bug",      "Merged",   SUCCESS,  "Author"),
    ("PR #23", "Review: teammate chart module",        "Reviewed", ACCENT,   "Reviewer"),
    ("PR #31", "Feature: BOM recursive cost parser",   "Merged",   SUCCESS,  "Author"),
    ("PR #38", "Review: civil module data export",     "Reviewed", ACCENT,   "Reviewer"),
]

IMPACT = (
    "My primary contribution was the Stress Analysis module (Mechanical Engineering).\n\n"
    "• Designed the Beam class (OOP) implementing σ = F/A for normal stress and\n"
    "  τ = T·r/J for shear stress, with full unit-conversion support.\n\n"
    "• Fixed a critical unit-conversion bug in the torque sub-module (PR #19) that\n"
    "  caused incorrect N·m to kN·m scaling for forces above 1000 N.\n\n"
    "• Built the recursive BOM cost parser using Σ(Qᵢ×Pᵢ) + Overheads, enabling\n"
    "  deep hierarchical assemblies without manual stack management.\n\n"
    "These components allowed the mechanical module to pass all 14 integration tests\n"
    "in the Week 10 deployment sprint."
)

def github_page():
    commit_rows = []
    for sha, msg, week, color in COMMITS:
        commit_rows.append(ft.Container(
            content=ft.Row([
                ft.Text(sha, size=10, color=color, width=62,
                        weight=ft.FontWeight.W_600, font_family="monospace"),
                ft.Text(msg, size=11, color=TEXT, expand=True),
                ft.Text(week, size=10, color=MUTED),
            ], spacing=8),
            bgcolor=wo(0.04, color),
            border_radius=ft.BorderRadius.all(6),
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border=ft.Border.all(1, wo(0.15, color)),
        ))

    pr_rows = []
    for pr_id, desc, status, color, role in PULL_REQUESTS:
        pr_rows.append(ft.Container(
            content=ft.Row([
                ft.Text(pr_id, size=10, color=color, width=52,
                        font_family="monospace", weight=ft.FontWeight.W_600),
                ft.Text(desc, size=11, color=TEXT, expand=True),
                chip(role, MUTED),
                chip(status, color),
            ], spacing=6),
            bgcolor=wo(0.04, color),
            border_radius=ft.BorderRadius.all(6),
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border=ft.Border.all(1, wo(0.15, color)),
        ))

    return ft.Column([
        ft.Container(height=20),
        section_title("🐙", "GitHub Evidence",
                      "Individual contribution proof: commits, PRs, and impact summary"),

        card(ft.Column([
            ft.Row([
                ft.Text("📝", size=14),
                ft.Text("  Commit History", size=14, color=TEXT, weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                chip(f"{len(COMMITS)} commits", ACCENT),
            ]),
            ft.Container(height=4),
            ft.Text("Replace SHA values with your real 7-char commit IDs from GitHub.",
                    size=10, color=MUTED),
            ft.Container(height=10),
            ft.Column(commit_rows, spacing=5),
        ]), accent_top=ACCENT),

        ft.Container(height=14),

        card(ft.Column([
            ft.Row([
                ft.Text("🔀", size=14),
                ft.Text("  Pull Request Log", size=14, color=TEXT, weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                chip(f"{len(PULL_REQUESTS)} PRs", SUCCESS),
            ]),
            ft.Container(height=10),
            ft.Column(pr_rows, spacing=5),
        ]), accent_top=SUCCESS),

        ft.Container(height=14),

        card(ft.Column([
            ft.Row([
                ft.Text("⚡", size=14),
                ft.Text("  Impact Summary", size=14, color=TEXT, weight=ft.FontWeight.W_600),
            ]),
            ft.Container(height=10),
            ft.Container(
                content=ft.Text(IMPACT, size=11, color=wo(0.9, TEXT), font_family="monospace"),
                bgcolor=wo(0.05, SUCCESS),
                border_radius=ft.BorderRadius.all(8),
                padding=ft.Padding.all(14),
                border=ft.Border.all(1, wo(0.25, SUCCESS)),
            ),
        ]), accent_top=ACCENT2),

        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)

# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title      = "Web Portfolio – CP1 2026"
    page.bgcolor    = BG
    page.padding    = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width  = 430
    page.window_height = 900
    page.fonts = {}

    # ── Lightbox overlay ────────────────────────────────────────────────────
    lb_image = ft.Image(src="", fit="contain", expand=True)
    lb_title = ft.Text("", size=13, color=TEXT, weight=ft.FontWeight.W_600,
                       text_align=ft.TextAlign.CENTER)

    lightbox = ft.Container(
        visible=False,
        expand=True,
        bgcolor=wo(0.92, BG),
        content=ft.Column([
            # close bar
            ft.Container(
                content=ft.Row([
                    lb_title,
                    ft.Container(expand=True),
                    ft.GestureDetector(
                        on_tap=lambda e: close_lightbox(),
                        content=ft.Container(
                            content=ft.Text("✕", size=18, color=TEXT),
                            bgcolor=wo(0.2, ACCENT2),
                            border_radius=ft.BorderRadius.all(8),
                            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                        ),
                    ),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                bgcolor=SURFACE,
                border=ft.Border.only(bottom=ft.BorderSide(1, BORDER)),
            ),
            # full image
            ft.Container(
                content=lb_image,
                expand=True,
                padding=ft.Padding.all(16),
                alignment=ft.Alignment(0, 0),
            ),
            # tap anywhere below to close hint
            ft.GestureDetector(
                on_tap=lambda e: close_lightbox(),
                content=ft.Container(
                    content=ft.Text("tap anywhere to close", size=10, color=MUTED,
                                    text_align=ft.TextAlign.CENTER),
                    padding=ft.Padding.symmetric(vertical=12),
                    alignment=ft.Alignment(0, 0),
                ),
            ),
        ], spacing=0),
    )

    def open_lightbox(asset_path, name):
        lb_image.src = asset_path
        lb_title.value = name
        lightbox.visible = True
        page.update()

    def close_lightbox():
        lightbox.visible = False
        page.update()

    # ── Pages ────────────────────────────────────────────────────────────────
    PAGES = {
        "Home":     lambda: home_page(),
        "Timeline": lambda: timeline_page(),
        "MATLAB":   lambda: matlab_page(open_lightbox=open_lightbox),
        "Blog":     lambda: blog_page(),
        "GitHub":   lambda: github_page(),
    }

    content_col = ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
    )
    content_wrap = ft.Container(
        content=content_col,
        expand=True,
        padding=ft.Padding.symmetric(horizontal=16),
    )

    nav_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    nav_wrap = ft.Container(
        content=nav_row,
        bgcolor=SURFACE,
        border=ft.Border.only(top=ft.BorderSide(1, BORDER)),
        padding=ft.Padding.symmetric(vertical=6, horizontal=10),
    )

    def navigate(name):
        nav_items = []
        for icon, n in NAV_PAGES:
            is_active = n == name
            nav_items.append(
                ft.GestureDetector(
                    on_tap=lambda e, nav_n=n: navigate(nav_n),
                    content=ft.Container(
                        content=ft.Column([
                            ft.Text(icon, size=16),
                            ft.Text(n, size=9,
                                    color=ACCENT if is_active else MUTED,
                                    weight=ft.FontWeight.W_700 if is_active
                                           else ft.FontWeight.NORMAL),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        bgcolor=wo(0.14, ACCENT) if is_active else "transparent",
                        border_radius=ft.BorderRadius.all(8),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=7),
                        border=ft.Border.all(1, wo(0.35, ACCENT) if is_active
                                              else "transparent"),
                    )
                )
            )
        nav_row.controls = nav_items

        page_widget = PAGES[name]()
        if isinstance(page_widget, ft.Column):
            content_col.controls = page_widget.controls
        else:
            content_col.controls = [page_widget]

        page.update()

    topbar = build_topbar()

    # Use a Stack so lightbox can float over everything
    page.add(
        ft.Stack([
            ft.Column([
                topbar,
                content_wrap,
                nav_wrap,
            ], expand=True, spacing=0),
            lightbox,
        ], expand=True)
    )

    navigate("Home")



# FIX 2: ft.app() was deprecated in Flet 0.80.0 — use ft.run() instead
# assets_dir tells Flet's web server where to find images/fonts/etc.
ft.run(main, view=ft.AppView.WEB_BROWSER, port=8080, assets_dir="assets")