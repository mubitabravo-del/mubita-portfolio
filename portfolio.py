"""
Web Portfolio - Computer Programming I (Semester 1, 2026)
Flet 0.85 compatible — with animations & styling polish
"""

import flet as ft
import flet_video as fv
import threading
import time

# ── Design Tokens ────────────────────────────────────────────────────────────
BG      = "#08090D"
SURFACE = "#0F1218"
CARD    = "#13161F"
ACCENT  = "#4DFFD2"
ACCENT2 = "#FF5F6D"
ACCENT3 = "#FFD166"
TEXT    = "#EEF1F8"
MUTED   = "#5A6480"
SUCCESS = "#3BFFA0"
WARN    = "#FFB347"
BORDER  = "#1E2535"
PURPLE  = "#B57BFF"
BLUE    = "#4D9FFF"

def wo(opacity, color):
    return ft.Colors.with_opacity(opacity, color)

# ── Reusable widgets ──────────────────────────────────────────────────────────

def chip(text, color=ACCENT):
    return ft.Container(
        content=ft.Text(text, size=10, color=color, weight=ft.FontWeight.W_700,
                        font_family="monospace"),
        bgcolor=wo(0.12, color),
        border=ft.Border.all(1, wo(0.4, color)),
        border_radius=ft.BorderRadius.all(4),
        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
    )

def divider():
    return ft.Container(height=1, bgcolor=BORDER, margin=ft.Margin.symmetric(vertical=12))

def card(content, pad=16, border_color=BORDER, accent_top=None):
    top_accent = ft.Container(
        height=3, bgcolor=accent_top,
        border_radius=ft.BorderRadius.only(top_left=10, top_right=10),
    ) if accent_top else ft.Container(height=0)
    return ft.Container(
        content=ft.Column([
            top_accent,
            ft.Container(content=content, padding=ft.Padding.all(pad)),
        ], spacing=0),
        bgcolor=CARD,
        border_radius=ft.BorderRadius.all(10),
        border=ft.Border.all(1, border_color),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
    )

def section_title(icon, title, subtitle=None):
    return ft.Column([
        ft.Row([
            ft.Container(
                content=ft.Text(icon, size=20),
                width=42, height=42,
                bgcolor=wo(0.12, ACCENT),
                border_radius=ft.BorderRadius.all(10),
                alignment=ft.Alignment(0, 0),
                animate=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
            ),
            ft.Column([
                ft.Text(title, size=20, color=TEXT, weight=ft.FontWeight.BOLD),
                ft.Text(subtitle, size=11, color=MUTED) if subtitle else ft.Container(height=0),
            ], spacing=1),
        ], spacing=12),
        ft.Container(
            height=2, bgcolor=wo(0.25, ACCENT),
            border_radius=ft.BorderRadius.all(1),
            margin=ft.Margin.only(top=10, bottom=16),
            animate=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
        ),
    ], spacing=0)

def mono_box(text):
    return ft.Container(
        content=ft.Text(text, size=12, color=ACCENT3, font_family="monospace"),
        bgcolor=wo(0.07, ACCENT3),
        border=ft.Border(left=ft.BorderSide(3, ACCENT3)),
        border_radius=ft.BorderRadius.only(top_right=6, bottom_right=6),
        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
        margin=ft.Margin.symmetric(vertical=6),
    )

# ── Animated fade-in wrapper ──────────────────────────────────────────────────

def fade_slide_in(control, delay_ms=0, page=None):
    """Wraps a control in an opacity+offset container and animates it in."""
    wrapper = ft.Container(
        content=control,
        opacity=0,
        offset=ft.Offset(0, 0.06),
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
        animate_offset=ft.Animation(500, ft.AnimationCurve.EASE_OUT),
    )

    def trigger():
        time.sleep(delay_ms / 1000)
        wrapper.opacity = 1
        wrapper.offset = ft.Offset(0, 0)
        if page:
            page.update()

    threading.Thread(target=trigger, daemon=True).start()
    return wrapper

# ── Top bar ───────────────────────────────────────────────────────────────────

def build_topbar():
    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text("< CP1 />", size=13, color=ACCENT,
                                weight=ft.FontWeight.BOLD, font_family="monospace"),
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

NAV_PAGES = [("🏠", "Home"), ("📅", "Timeline"), ("📐", "MATLAB"), ("✍️", "Blog"), ("🐙", "GitHub")]

# ── HOME PAGE ────────────────────────────────────────────────────────────────

SKILLS = [
    ("Python",       ACCENT,  "Core language · OOP · Algorithms"),
    ("Flet",         BLUE,    "UI framework · Event-driven design"),
    ("MATLAB",       PURPLE,  "Simulation · Signal Processing · ML"),
    ("Git & GitHub", ACCENT2, "Version control · PRs · Code review"),
    ("Data Viz",     ACCENT3, "matplotlib · Charts · BOM analysis"),
    ("Testing",      SUCCESS, "pytest · Unit tests · Integration"),
]

HIGHLIGHTS = [
    ("⚙️", "Stress Analysis Module",
     "Designed the Beam class implementing σ = F/A and τ = T·r/J with full unit-conversion support.", ACCENT),
    ("🔁", "Recursive BOM Parser",
     "Built a recursive cost engine using Σ(Qᵢ×Pᵢ) + Overheads, handling deep assembly hierarchies.", SUCCESS),
    ("📊", "Force-Displacement Chart",
     "Integrated matplotlib into Flet via ft.Image buffers — live graph output from real mechanical data.", ACCENT3),
    ("🐛", "Bug Fix: Torque Module",
     "Tracked and fixed a critical N·m → kN·m scaling error affecting forces above 1 000 N (PR #19).", ACCENT2),
]

def home_page(page=None):
    # ── Animated avatar with pulsing ring ─────────────────────────────────
    ring = ft.Container(
        width=80, height=80,
        border_radius=ft.BorderRadius.all(40),
        border=ft.Border.all(2, wo(0.6, ACCENT)),
        animate=ft.Animation(1500, ft.AnimationCurve.EASE_IN_OUT),
    )
    avatar = ft.Stack([
        ring,
        ft.Container(
            content=ft.Text("MB", size=22, color=BG, weight=ft.FontWeight.BOLD,
                            font_family="monospace"),
            width=64, height=64,
            bgcolor=ACCENT,
            border_radius=ft.BorderRadius.all(32),
            alignment=ft.Alignment(0, 0),
            left=8, top=8,
        ),
    ], width=80, height=80)

    def pulse_ring():
        while True:
            time.sleep(1.8)
            ring.border = ft.Border.all(2, wo(0.15, ACCENT))
            if page: page.update()
            time.sleep(0.9)
            ring.border = ft.Border.all(2, wo(0.7, ACCENT))
            if page: page.update()

    threading.Thread(target=pulse_ring, daemon=True).start()

    name_block = ft.Column([
        ft.Container(
            content=ft.Text("COMPUTER PROGRAMMING I · 2026",
                            size=8, color=ACCENT, weight=ft.FontWeight.W_700,
                            font_family="monospace"),
            bgcolor=wo(0.1, ACCENT),
            border_radius=ft.BorderRadius.all(4),
            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
        ),
        ft.Container(height=10),
        ft.Text("Mubita Bravo", size=28, color=TEXT, weight=ft.FontWeight.BOLD),
        ft.Text("2nd Year · Mechanical Engineering", size=13, color=MUTED),
        ft.Container(height=8),
        ft.Row([
            chip("Python", ACCENT), chip("Flet", BLUE),
            chip("MATLAB", PURPLE), chip("Git", ACCENT2),
        ], wrap=True, spacing=5),
    ], spacing=2)

    hero = ft.Container(
        content=ft.Column([
            ft.Row([avatar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=16),
            name_block,
            ft.Container(height=20),
            ft.Container(
                content=ft.Text(
                    "Building a Mechanical Engineering app as part of a 20-member team — "
                    "responsible for the stress-analysis module, BOM cost engine, matplotlib "
                    "data visualisation, and two completed code reviews.",
                    size=12, color=wo(0.75, TEXT),
                ),
                bgcolor=wo(0.04, ACCENT),
                border=ft.Border(left=ft.BorderSide(3, wo(0.5, ACCENT))),
                border_radius=ft.BorderRadius.only(top_right=8, bottom_right=8),
                padding=ft.Padding.symmetric(horizontal=14, vertical=12),
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.START),
        bgcolor=wo(0.03, ACCENT),
        border=ft.Border.all(1, wo(0.15, ACCENT)),
        border_radius=ft.BorderRadius.all(14),
        padding=ft.Padding.symmetric(vertical=24, horizontal=20),
    )

    skill_cards = []
    for i, (name, color, detail) in enumerate(SKILLS):
        sc = ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Text(name[0], size=14, color=color,
                                    weight=ft.FontWeight.BOLD, font_family="monospace"),
                    width=34, height=34,
                    bgcolor=wo(0.14, color),
                    border_radius=ft.BorderRadius.all(8),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Container(height=8),
                ft.Text(name, size=12, color=TEXT, weight=ft.FontWeight.W_700),
                ft.Text(detail, size=9, color=MUTED, max_lines=2),
            ], spacing=2),
            bgcolor=CARD,
            border=ft.Border.all(1, wo(0.25, color)),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.all(12),
            expand=True,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        skill_cards.append(fade_slide_in(sc, delay_ms=200 + i * 80, page=page))

    skills_section = ft.Column([
        ft.Text("Skills", size=14, color=MUTED, weight=ft.FontWeight.W_600,
                font_family="monospace"),
        ft.Container(height=10),
        ft.Row([skill_cards[0], skill_cards[1]], spacing=8),
        ft.Row([skill_cards[2], skill_cards[3]], spacing=8),
        ft.Row([skill_cards[4], skill_cards[5]], spacing=8),
    ], spacing=8)

    highlight_rows = []
    for i, (icon, title, desc, color) in enumerate(HIGHLIGHTS):
        h = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text(icon, size=16),
                    width=38, height=38,
                    bgcolor=wo(0.12, color),
                    border_radius=ft.BorderRadius.all(8),
                    alignment=ft.Alignment(0, 0),
                ),
                ft.Column([
                    ft.Text(title, size=12, color=TEXT, weight=ft.FontWeight.W_700),
                    ft.Text(desc, size=10, color=MUTED),
                ], spacing=3, expand=True),
            ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.START),
            bgcolor=wo(0.04, color),
            border=ft.Border.all(1, wo(0.2, color)),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        highlight_rows.append(fade_slide_in(h, delay_ms=500 + i * 100, page=page))

    highlights_section = ft.Column([
        ft.Text("Project Contributions", size=14, color=MUTED,
                weight=ft.FontWeight.W_600, font_family="monospace"),
        ft.Container(height=10),
        ft.Column(highlight_rows, spacing=8),
    ], spacing=0)

    return ft.Column([
        ft.Container(height=20),
        fade_slide_in(hero, delay_ms=50, page=page),
        ft.Container(height=24),
        skills_section,
        ft.Container(height=24),
        highlights_section,
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)


# ── TIMELINE PAGE ─────────────────────────────────────────────────────────────

TIMELINE_DATA = [
    (1,  "Project Kickoff", "Set up GitHub repository, created personal branch, attended team planning meeting, agreed on folder structure and naming conventions.", ["Git Setup", "Team Planning"], ACCENT),
    (2,  "Requirements Analysis", "Analysed mechanical engineering module specifications. Drafted class diagrams and data models for the Beam stress analysis sub-module.", ["Analysis", "Documentation"], BLUE),
    (3,  "UI Scaffolding", "Built base navigation component and colour theme in Flet. Established responsive layout skeleton shared across all team members.", ["Flet", "UI Design"], ACCENT),
    (4,  "Stress Calculator", "Implemented the σ = F/A stress calculator widget with input validation, unit conversion (N→kN, m²→mm²), and live result display.", ["Python", "Math"], ACCENT2),
    (5,  "MATLAB Courses 1–3", "Completed MATLAB Onramp, Signal Processing Onramp, and Machine Learning Onramp on MathWorks Learning Center. Screenshots archived.", ["MATLAB", "Learning"], SUCCESS),
    (6,  "Data Visualisation", "Integrated matplotlib for force-displacement graphs. Charts rendered inside Flet via ft.Image from in-memory PNG buffers.", ["Charts", "Integration"], ACCENT3),
    (7,  "Code Review Sprint", "Reviewed 3 pull requests from teammates, left inline comments, and fixed the unit-conversion bug (N·m → kN·m) in the torque module.", ["Code Review", "Bug Fix"], WARN),
    (8,  "MATLAB Courses 4–6", "Completed Deep Learning Onramp, Image Processing Onramp, and Statistics & Machine Learning Onramp. Progress: 6/8.", ["MATLAB", "Learning"], SUCCESS),
    (9,  "Technical Blog Posts", "Wrote three technical blog posts covering OOP, recursion, and event-driven programming, each with an embedded demo video.", ["Documentation", "Blog"], PURPLE),
    (10, "Testing & Deployment", "Wrote pytest unit tests for stress functions, resolved edge cases, and deployed the portfolio as a live web app on port 8080.", ["Testing", "Deployment"], ACCENT),
]

def timeline_page(page=None):
    rows = []
    for i, (week, title, desc, tags, color) in enumerate(TIMELINE_DATA):
        entry = ft.Row([
            ft.Column([
                ft.Container(
                    content=ft.Text(f"W{week}", size=10, color=color,
                                    weight=ft.FontWeight.BOLD, font_family="monospace"),
                    width=36, height=36,
                    bgcolor=wo(0.14, color),
                    border=ft.Border.all(1, wo(0.45, color)),
                    border_radius=ft.BorderRadius.all(18),
                    alignment=ft.Alignment(0, 0),
                    animate=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
                ),
                ft.Container(width=2, expand=True, bgcolor=wo(0.12, color),
                             margin=ft.Margin.only(left=17)) if week < 10
                else ft.Container(expand=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, width=36),
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
                animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            ),
        ], spacing=10, vertical_alignment=ft.CrossAxisAlignment.START)
        rows.append(fade_slide_in(entry, delay_ms=i * 60, page=page))

    return ft.Column([
        ft.Container(height=20),
        section_title("📅", "Project Timeline",
                      "Weekly log of individual contributions to the Mechanical Engineering App"),
        ft.Column(rows, spacing=2),
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0,
       horizontal_alignment=ft.CrossAxisAlignment.START)


# ── MATLAB PAGE ───────────────────────────────────────────────────────────────

MATLAB_COURSES = [
    ("MATLAB Onramp",            True,  "Core syntax, variables, scripts, and basic plotting",   "matlab/cert_matlab_onramp.png",    ACCENT),
    ("Calculation with Vectors", True,  "Vector operations, indexing, and array mathematics",    "matlab/CalculationwithVectors.png", BLUE),
    ("Machine Learning Onramp",  True,  "Classification, regression, and model evaluation",      "matlab/machineLearning.png",       SUCCESS),
    ("Explore Data",             True,  "Data import, cleaning, and exploratory analysis",       "matlab/ExploreData.png",           PURPLE),
    ("Finite Element",           True,  "FEA fundamentals and structural simulation",            "matlab/FiniteElement.png",         ACCENT2),
    ("How and Why",              True,  "Engineering reasoning and problem-solving techniques",  "matlab/HowandWhy.png",             ACCENT3),
    ("Simulink Onramp",          True,  "Model-based design, block diagrams, simulation",        "matlab/simulinkOnramp.png",        PURPLE),
    ("MATLAB Onramp (Extended)", False, "Advanced scripting, functions, and file I/O",           "matlab/matlabOnramp.png",          MUTED),
]

def matlab_page(open_lightbox=None, page=None):
    done_count = sum(1 for _, done, *_ in MATLAB_COURSES if done)
    pct = int(done_count / 8 * 100)

    progress_fill = ft.Container(
        expand=0, height=8, bgcolor=SUCCESS,
        border_radius=ft.BorderRadius.only(top_left=4, bottom_left=4,
                                           top_right=4 if pct==100 else 0,
                                           bottom_right=4 if pct==100 else 0),
        animate=ft.Animation(900, ft.AnimationCurve.EASE_OUT),
    )

    def animate_progress():
        time.sleep(0.3)
        progress_fill.expand = pct
        if page: page.update()

    threading.Thread(target=animate_progress, daemon=True).start()

    course_rows = []
    for i, (name, done, desc, asset, color) in enumerate(MATLAB_COURSES):
        c = color if done else MUTED
        row = ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Text("✓" if done else "○", size=12, color=c,
                                    weight=ft.FontWeight.BOLD),
                    width=32, height=32,
                    bgcolor=wo(0.15, c),
                    border_radius=ft.BorderRadius.all(16),
                    alignment=ft.Alignment(0, 0),
                    animate=ft.Animation(400, ft.AnimationCurve.BOUNCE_OUT),
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
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        course_rows.append(fade_slide_in(row, delay_ms=i * 60, page=page))

    cert_items = []
    for name, done, _, asset, color in MATLAB_COURSES:
        c = color if done else MUTED

        def make_tap(a, n):
            def _tap(e):
                if open_lightbox: open_lightbox(a, n)
            return _tap

        thumb = ft.Container(
            content=ft.Column([
                ft.GestureDetector(
                    on_tap=make_tap(asset, name) if done else None,
                    content=ft.Stack([
                        ft.Container(
                            content=ft.Image(
                                src=asset, width=176, height=140, fit="cover",
                                border_radius=ft.BorderRadius.all(8),
                                error_content=ft.Container(
                                    content=ft.Column([
                                        ft.Text("🏅", size=32),
                                        ft.Text(name, size=9, color=c,
                                                text_align=ft.TextAlign.CENTER, max_lines=2),
                                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                                    width=176, height=140,
                                    bgcolor=wo(0.08, c),
                                    border_radius=ft.BorderRadius.all(8),
                                    alignment=ft.Alignment(0, 0),
                                ),
                            ),
                        ),
                        ft.Container(
                            content=ft.Text("🔍", size=14),
                            right=6, top=6,
                            bgcolor=wo(0.55, BG),
                            border_radius=ft.BorderRadius.all(6),
                            padding=ft.Padding.all(3),
                            visible=done,
                        ),
                    ]),
                ),
                ft.Container(height=6),
                ft.Text(name, size=10, color=c, text_align=ft.TextAlign.CENTER,
                        max_lines=2, weight=ft.FontWeight.W_600),
                ft.Text("tap to expand" if done else "not done", size=8,
                        color=wo(0.5, c), text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            width=184,
            bgcolor=wo(0.04, c),
            border=ft.Border.all(2, wo(0.5, c) if done else wo(0.15, c)),
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.all(4),
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        cert_items.append(thumb)

    return ft.Column([
        ft.Container(height=20),
        section_title("📐", "MATLAB Achievement Hub",
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
                    progress_fill,
                    ft.Container(expand=100 - pct, height=8),
                ], spacing=0),
                bgcolor=BORDER, border_radius=ft.BorderRadius.all(4),
                height=8, clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Container(height=6),
            ft.Text(
                f"{8 - done_count} remaining — visit learn.mathworks.com" if pct < 100
                else "All 8 complete ✓",
                size=11, color=SUCCESS if pct == 100 else MUTED,
            ),
        ]), accent_top=SUCCESS),

        ft.Container(height=14),
        ft.Column(course_rows, spacing=6),
        ft.Container(height=20),

        card(ft.Column([
            ft.Row([
                ft.Text("🏅", size=15),
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


# ── BLOG PAGE ─────────────────────────────────────────────────────────────────

DEMO_VIDEO_SRC = "video/video_2026-06-15_14-52-22.mp4"

BLOG_POSTS = [
    {
        "title": "Object-Oriented Programming in Engineering Apps",
        "date": "Week 3", "tags": ["OOP", "Python", "Design Patterns"], "color": ACCENT,
        "sections": [
            {"heading": "Why OOP for Engineering?",
             "body": "Object-Oriented Programming lets us model physical entities directly in code. In our Mechanical Engineering app, a Beam is not just a dictionary of values — it is a fully-fledged object that owns its material properties and exposes methods for every calculation it supports."},
            {"heading": "The Beam Class",
             "body": "Each Beam instance stores force (F) and cross-sectional area (A). Calling beam.normal_stress() returns the normal stress σ in Pascals, encapsulating the formula and its units internally."},
            {"heading": "Normal Stress Formula",
             "formula": "σ = F / A\n\nwhere  σ = normal stress (Pa)\n       F = applied force (N)\n       A = cross-sectional area (m²)"},
            {"heading": "Code Sketch",
             "formula": "class Beam:\n    def __init__(self, force, area):\n        self.F = force   # N\n        self.A = area    # m²\n\n    def normal_stress(self):\n        return self.F / self.A  # Pa"},
            {"body": "Encapsulating F and A inside the class means multi-beam simulations are clean and scalable: create a list of Beam objects, call normal_stress() on each, and collect results — no global variables, no naming collisions."},
        ],
        "show_video": True,
    },
    {
        "title": "Recursion & Iterative Algorithms",
        "date": "Week 5", "tags": ["Recursion", "Algorithms", "Python"], "color": ACCENT2,
        "sections": [
            {"heading": "What is Recursion?",
             "body": "Recursion is when a function calls itself with a simpler sub-problem until it reaches a base case. It is natural for tree-shaped data like a hierarchical Bill of Materials (BOM), where each node may itself be a sub-assembly."},
            {"heading": "Total Cost Formula",
             "formula": "        n\nCost = Σ (Qᵢ × Pᵢ)  +  Overheads\n       i=1\n\nQᵢ = quantity of component i\nPᵢ = unit price of component i"},
            {"heading": "Recursive BOM Parser",
             "formula": "def bom_cost(node):\n    if node['type'] == 'part':\n        return node['qty'] * node['price']\n    return sum(bom_cost(child)\n               for child in node['children'])\n           + node.get('overhead', 0)"},
            {"body": "The recursive approach mirrors the BOM tree structure exactly — no manual stack management is required. The base case terminates the descent, and the call-stack naturally unwinds to accumulate costs up to the root assembly."},
        ],
        "show_video": True,
    },
    {
        "title": "Event-Driven Programming with Flet",
        "date": "Week 6", "tags": ["Flet", "Events", "UI"], "color": PURPLE,
        "sections": [
            {"heading": "The Event-Driven Model",
             "body": "Unlike a top-to-bottom script, a Flet app waits for user actions — button clicks, text changes, slider moves — and responds via callback functions. This keeps the UI always responsive and cleanly separates business logic from display code."},
            {"heading": "Stress Calculator Callback",
             "formula": "def calculate(e):\n    F = float(force_field.value)  # N\n    A = float(area_field.value)   # m²\n    sigma = F / A                 # Pa\n    result_label.value = (\n        f'σ = {sigma:,.2f} Pa'\n    )\n    page.update()\n\ncalc_btn = ft.ElevatedButton(\n    'Calculate', on_click=calculate\n)"},
            {"heading": "Why page.update()?",
             "body": "Flet batches UI changes for performance. Calling page.update() commits all pending control changes to the browser in a single diff, ensuring the result label appears instantly after the user taps the button — even across a network when deployed as a web app."},
        ],
        "show_video": True,
    },
]

def build_video_player(color):
    try:
        player = fv.Video(
            playlist=[fv.VideoMedia(DEMO_VIDEO_SRC)],
            playlist_mode=fv.PlaylistMode.NONE,
            fill_color=BG,
            aspect_ratio=16 / 9,
            volume=100,
            autoplay=False,
            muted=False,
            show_controls=True,
            width=float("inf"),
        )
        video_widget = ft.Container(
            content=player,
            border_radius=ft.BorderRadius.all(8),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            bgcolor=BG,
        )
    except Exception as e:
        # Fallback
        video_widget = ft.Container(
            content=ft.Column([
                ft.Text("▶", size=36, color=color, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    f"Video player requires 'flet-video' package\nFile: assets/{DEMO_VIDEO_SRC}\n\nError: {str(e)[:100]}",
                    size=11, color=MUTED, text_align=ft.TextAlign.CENTER,
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
            width=float("inf"), height=180,
            bgcolor=wo(0.08, color),
            border_radius=ft.BorderRadius.all(8),
            alignment=ft.Alignment(0, 0),
        )

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Text("▶", size=10, color=color,
                                    weight=ft.FontWeight.W_700, font_family="monospace"),
                    bgcolor=wo(0.14, color),
                    border_radius=ft.BorderRadius.all(4),
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    border=ft.Border.all(1, wo(0.4, color)),
                ),
                ft.Text(" Demo Video", size=12, color=TEXT, weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                ft.Text("portfolio demo", size=9, color=MUTED),
            ], spacing=6),
            ft.Container(height=10),
            video_widget,
            ft.Container(height=6),
            ft.Text(
                "▲ Use the player controls to play, pause, seek, and adjust volume.",
                size=9, color=wo(0.5, MUTED),
            ),
        ], spacing=0),
        bgcolor=wo(0.05, color),
        border=ft.Border.all(1, wo(0.25, color)),
        border_radius=ft.BorderRadius.all(8),
        padding=ft.Padding.symmetric(horizontal=12, vertical=12),
    )


def blog_page(page=None):
    posts = []
    for i, p in enumerate(BLOG_POSTS):
        color = p["color"]
        section_widgets = []
        for sec in p["sections"]:
            if "heading" in sec:
                section_widgets.append(
                    ft.Text(sec["heading"], size=12, color=color, weight=ft.FontWeight.W_700)
                )
            if "body" in sec:
                section_widgets.append(
                    ft.Text(sec["body"], size=12, color=wo(0.85, TEXT))
                )
            if "formula" in sec:
                section_widgets.append(mono_box(sec["formula"]))

        video_block = ft.Column([], spacing=0)
        if p.get("show_video"):
            video_block = ft.Column([
                divider(),
                build_video_player(color),
            ], spacing=0)

        post = card(ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Text(p["date"], size=9, color=color,
                                    weight=ft.FontWeight.W_700, font_family="monospace"),
                    bgcolor=wo(0.12, color), border_radius=ft.BorderRadius.all(4),
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                ),
                ft.Row([chip(t, color) for t in p["tags"]], spacing=4, wrap=True),
            ], spacing=8, wrap=True),
            ft.Container(height=6),
            ft.Text(p["title"], size=15, color=TEXT, weight=ft.FontWeight.BOLD),
            divider(),
            ft.Column(section_widgets, spacing=8),
            video_block,
        ], spacing=6), accent_top=color)
        posts.append(fade_slide_in(post, delay_ms=i * 120, page=page))

    return ft.Column([
        ft.Container(height=20),
        section_title("✍️", "Technical Blog",
                      "Confidence in Concepts — written explanations with mathematical notation & live demo"),
        ft.Column(posts, spacing=16),
        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START)


# ── GITHUB PAGE ───────────────────────────────────────────────────────────────

COMMITS = [
    ("a1b2c3d", "feat: add Beam stress calculator widget",             "Week 4",  ACCENT),
    ("d4e5f67", "fix: unit conversion bug in torque module (N·m→kN·m)","Week 7",  ACCENT2),
    ("789abcd", "feat: implement BOM recursive cost parser",           "Week 5",  SUCCESS),
    ("321fedc", "feat: add matplotlib force-displacement chart",       "Week 6",  ACCENT3),
    ("cafe012", "test: write pytest unit tests for stress functions",  "Week 10", PURPLE),
]

PULL_REQUESTS = [
    ("PR #12", "Feature: stress analysis UI",        "Merged",   SUCCESS, "Author"),
    ("PR #19", "Fix: torque unit conversion bug",    "Merged",   SUCCESS, "Author"),
    ("PR #23", "Review: teammate chart module",      "Reviewed", ACCENT,  "Reviewer"),
    ("PR #31", "Feature: BOM recursive cost parser", "Merged",   SUCCESS, "Author"),
    ("PR #38", "Review: civil module data export",   "Reviewed", ACCENT,  "Reviewer"),
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

def github_page(open_lightbox=None, page=None):
    commit_rows = []
    for i, (sha, msg, week, color) in enumerate(COMMITS):
        row = ft.Container(
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
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        commit_rows.append(fade_slide_in(row, delay_ms=i * 60, page=page))

    pr_rows = []
    for i, (pr_id, desc, status, color, role) in enumerate(PULL_REQUESTS):
        row = ft.Container(
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
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        pr_rows.append(fade_slide_in(row, delay_ms=i * 60, page=page))

    def on_screenshot_tap(e):
        if open_lightbox:
            open_lightbox("github/git.png", "Commit History — GitHub Screenshot")

    screenshot_card = card(ft.Column([
        ft.Row([
            ft.Text("📸", size=14),
            ft.Text("  Commit Screenshot", size=14, color=TEXT, weight=ft.FontWeight.W_600),
            ft.Container(expand=True),
            ft.Text("tap to expand", size=9, color=MUTED),
        ]),
        ft.Container(height=10),
        ft.GestureDetector(
            on_tap=on_screenshot_tap,
            content=ft.Stack([
                ft.Container(
                    content=ft.Image(
                        src="github/git.png",
                        width=float("inf"), height=200,
                        fit="contain",
                        border_radius=ft.BorderRadius.all(8),
                        error_content=ft.Container(
                            content=ft.Column([
                                ft.Text("🖼️", size=36),
                                ft.Text("git.png not found", size=11, color=MUTED,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Text("Place at assets/github/git.png", size=9,
                                        color=wo(0.5, MUTED), text_align=ft.TextAlign.CENTER),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                            width=float("inf"), height=200,
                            bgcolor=wo(0.06, ACCENT),
                            border_radius=ft.BorderRadius.all(8),
                            border=ft.Border.all(1, wo(0.2, ACCENT)),
                            alignment=ft.Alignment(0, 0),
                        ),
                    ),
                    border_radius=ft.BorderRadius.all(8),
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                ),
                ft.Container(
                    content=ft.Text("🔍", size=14),
                    right=8, top=8,
                    bgcolor=wo(0.65, BG),
                    border_radius=ft.BorderRadius.all(6),
                    padding=ft.Padding.all(4),
                ),
            ]),
        ),
        ft.Container(height=6),
        ft.Text("Real commit history from GitHub repository",
                size=10, color=MUTED, text_align=ft.TextAlign.CENTER),
    ], spacing=0), accent_top=ACCENT)

    return ft.Column([
        ft.Container(height=20),
        section_title("🐙", "GitHub Evidence",
                      "Individual contribution proof: commits, PRs, and impact summary"),
        fade_slide_in(card(ft.Column([
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
        ]), accent_top=ACCENT), delay_ms=80, page=page),

        ft.Container(height=14),
        fade_slide_in(screenshot_card, delay_ms=200, page=page),
        ft.Container(height=14),

        fade_slide_in(card(ft.Column([
            ft.Row([
                ft.Text("🔀", size=14),
                ft.Text("  Pull Request Log", size=14, color=TEXT, weight=ft.FontWeight.W_600),
                ft.Container(expand=True),
                chip(f"{len(PULL_REQUESTS)} PRs", SUCCESS),
            ]),
            ft.Container(height=10),
            ft.Column(pr_rows, spacing=5),
        ]), accent_top=SUCCESS), delay_ms=320, page=page),

        ft.Container(height=14),

        fade_slide_in(card(ft.Column([
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
        ]), accent_top=ACCENT2), delay_ms=440, page=page),

        ft.Container(height=30),
    ], scroll=ft.ScrollMode.AUTO, spacing=0, horizontal_alignment=ft.CrossAxisAlignment.START)


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title      = "Web Portfolio – CP1 2026"
    page.bgcolor    = BG
    page.padding    = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width  = 430
    page.window_height = 900
    page.fonts = {}

    # Lightbox
    lb_image = ft.Image(src="", fit="contain", expand=True)
    lb_title = ft.Text("", size=13, color=TEXT, weight=ft.FontWeight.W_600,
                       text_align=ft.TextAlign.CENTER)

    lightbox = ft.Container(
        visible=False, expand=True, bgcolor=wo(0.92, BG),
        opacity=0,
        animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
        content=ft.Column([
            ft.Container(
                content=ft.Row([
                    lb_title, ft.Container(expand=True),
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
            ft.Container(content=lb_image, expand=True,
                         padding=ft.Padding.all(16), alignment=ft.Alignment(0, 0)),
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
        lightbox.opacity = 1
        page.update()

    def close_lightbox():
        lightbox.opacity = 0
        page.update()
        time.sleep(0.26)
        lightbox.visible = False
        page.update()

    PAGES = {
        "Home":     lambda: home_page(page=page),
        "Timeline": lambda: timeline_page(page=page),
        "MATLAB":   lambda: matlab_page(open_lightbox=open_lightbox, page=page),
        "Blog":     lambda: blog_page(page=page),
        "GitHub":   lambda: github_page(open_lightbox=open_lightbox, page=page),
    }

    content_col = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, spacing=0)
    content_wrap = ft.Container(
        content=content_col, expand=True,
        padding=ft.Padding.symmetric(horizontal=16),
    )

    nav_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_EVENLY)
    nav_wrap = ft.Container(
        content=nav_row, bgcolor=SURFACE,
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
                            ft.Container(
                                width=4, height=4,
                                bgcolor=ACCENT if is_active else "transparent",
                                border_radius=ft.BorderRadius.all(2),
                                animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        bgcolor=wo(0.14, ACCENT) if is_active else "transparent",
                        border_radius=ft.BorderRadius.all(8),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=7),
                        border=ft.Border.all(1, wo(0.35, ACCENT) if is_active
                                              else "transparent"),
                        animate=ft.Animation(250, ft.AnimationCurve.EASE_OUT),
                    )
                )
            )
        nav_row.controls = nav_items

        content_col.opacity = 0
        content_col.animate_opacity = ft.Animation(120, ft.AnimationCurve.EASE_IN)
        page.update()
        time.sleep(0.13)

        page_widget = PAGES[name]()
        if isinstance(page_widget, ft.Column):
            content_col.controls = page_widget.controls
        else:
            content_col.controls = [page_widget]

        content_col.opacity = 1
        content_col.animate_opacity = ft.Animation(300, ft.AnimationCurve.EASE_OUT)
        page.update()

    topbar = build_topbar()

    page.add(
        ft.Stack([
            ft.Column([topbar, content_wrap, nav_wrap], expand=True, spacing=0),
            lightbox,
        ], expand=True)
    )

    navigate("Home")


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")