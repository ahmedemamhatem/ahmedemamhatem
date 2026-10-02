#!/usr/bin/env python3
"""Generates the animated 3D SVG assets used by README.md.
Edit the data blocks below, then run:  python3 build_assets.py
"""
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
C, S = 0.866, 0.5

# ---------- palette (SyncoreHQ brand tokens, from syncorehq.com) ----------
BG0, BG1, LINE = "#0C1118", "#1A212B", "#313D4D"
BLUE, CYAN, AMBER = "#5B9DD9", "#3FB6A8", "#F2A35E"   # primary, accent teal, logo orange
TEXT, MUTED = "#E6EDF3", "#9FB0C3"
SHADES = {  # (top, left, right)
    "blue":  ("#79B4E6", "#4F8FD0", "#3A6FA6"),
    "cyan":  ("#7FD6CB", "#3FB6A8", "#2A8279"),
    "amber": ("#FFD9A8", "#E8843F", "#B85F2A"),
    "ink":   ("#2B3643", "#222B37", "#171E28"),
    "slate": ("#465568", "#313D4D", "#232C38"),
}

STYLE = f"""
.sans{{font-family:Inter,'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif}}
.mono{{font-family:ui-monospace,'SF Mono','Cascadia Code',Menlo,Consolas,'DejaVu Sans Mono',monospace}}
.pre{{white-space:pre}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
@keyframes bobs{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-4px)}}}}
@keyframes flow{{to{{stroke-dashoffset:-48}}}}
@keyframes blink{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
@keyframes rise{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadein{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes floor{{from{{transform:translateY(0);opacity:0}}15%{{opacity:1}}to{{transform:translateY(var(--d));opacity:1}}}}
@keyframes shadow{{0%,100%{{transform:scale(1);opacity:.5}}50%{{transform:scale(.8);opacity:.28}}}}
.bob{{animation:bob 5s ease-in-out infinite}}
.bobs{{animation:bobs 4s ease-in-out infinite}}
.flow{{stroke-dasharray:6 10;animation:flow 1.6s linear infinite}}
.blink{{animation:blink 2.4s ease-in-out infinite}}
.rise{{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}}
.fadein{{animation:fadein .5s ease-out both}}
.shadow{{transform-box:fill-box;transform-origin:center;animation:shadow 5s ease-in-out infinite}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""

def svg(w, h, body, extra_style="", label=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">'
            f'<title>{esc(label)}</title><style>{STYLE}{extra_style}</style>'
            f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>'
            f'<linearGradient id="name" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#CFE3F5"/></linearGradient>'
            f'<linearGradient id="brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5B9DD9"/><stop offset=".55" stop-color="#4F8FD0"/><stop offset="1" stop-color="#3FB6A8"/></linearGradient>'
            f'<linearGradient id="scRing" gradientUnits="userSpaceOnUse" x1="-36" y1="-36" x2="36" y2="36"><stop offset="0" stop-color="#f2a35e"/><stop offset=".5" stop-color="#e8843f"/><stop offset="1" stop-color="#2bb6a8"/></linearGradient>'
            f'<radialGradient id="scCore" cx=".5" cy=".42" r=".62"><stop offset="0" stop-color="#ffd9a8"/><stop offset=".45" stop-color="#f2a35e"/><stop offset="1" stop-color="#d9743a"/></radialGradient>'
            f'<radialGradient id="scGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e8843f" stop-opacity=".4"/><stop offset="1" stop-color="#e8843f" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".55" stop-color="#fff" stop-opacity="1"/></linearGradient>'
            f'<clipPath id="clip"><rect width="{w}" height="{h}" rx="28"/></clipPath></defs>'
            f'<g clip-path="url(#clip)"><rect width="{w}" height="{h}" fill="url(#bg)"/>{body}</g>'
            f'<rect x=".75" y=".75" width="{w-1.5}" height="{h-1.5}" rx="27.25" fill="none" stroke="{LINE}" stroke-width="1.5"/></svg>')

def logo(cx, cy, sc=1.0, spin=28):
    """The SyncoreHQ mark (core + three orbiting nodes), with a slow orbit."""
    return (f'<g transform="translate({cx},{cy}) scale({sc})"><circle r="46" fill="url(#scGlow)"/>'
            f'<circle r="32" fill="none" stroke="url(#scRing)" stroke-width="3" stroke-opacity=".5"/>'
            f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="{spin}s" repeatCount="indefinite"/>'
            f'<path d="M0 -36 A36 36 0 0 1 31.2 18" fill="none" stroke="url(#scRing)" stroke-width="4.4" stroke-linecap="round"/>'
            f'<g stroke="url(#scRing)" stroke-width="3.4" stroke-linecap="round"><line x1="0" y1="0" x2="0" y2="-32"/><line x1="0" y1="0" x2="-27.7" y2="16"/><line x1="0" y1="0" x2="27.7" y2="16"/></g>'
            f'<g fill="url(#scRing)"><circle cx="0" cy="-32" r="6"/><circle cx="-27.7" cy="16" r="6"/><circle cx="27.7" cy="16" r="6"/></g></g>'
            f'<circle r="13" fill="url(#scCore)"/><circle r="13" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.4"/></g>')

def wordmark(x, y, size, extra=""):
    return (f'<text x="{x}" y="{y}" class="sans" font-size="{size}" font-weight="800" fill="{TEXT}" letter-spacing="-.5">Syncore'
            f'<tspan fill="url(#brand)">HQ</tspan>{extra}</text>')

def pts(*p): return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)

def box(ox, oy, w, d, h, shade="blue", stroke_op=.35):
    """Isometric box. (ox,oy) = screen position of the bottom front corner."""
    top, left, right = SHADES[shade]
    F, R, L = (ox, oy), (ox + w*C, oy - w*S), (ox - d*C, oy - d*S)
    B = (ox + (w-d)*C, oy - (w+d)*S)
    up = lambda p: (p[0], p[1]-h)
    st = f'stroke="#FFFFFF" stroke-opacity="{stroke_op}" stroke-width="1" stroke-linejoin="round"'
    return (f'<polygon points="{pts(L, F, up(F), up(L))}" fill="{left}"/>'
            f'<polygon points="{pts(F, R, up(R), up(F))}" fill="{right}"/>'
            f'<polygon points="{pts(up(F), up(R), up(B), up(L))}" fill="{top}" {st}/>')

def floor(w, h, horizon, vp_x, op=.55):
    """Perspective grid floor with lines travelling towards the viewer."""
    depth = h - horizon
    rad = "".join(f'<line x1="{vp_x}" y1="{horizon}" x2="{x}" y2="{h}"/>' for x in range(-900, w+901, 150))
    hor = "".join(f'<line x1="0" y1="{horizon}" x2="{w}" y2="{horizon}" style="--d:{depth}px;animation:floor 7s cubic-bezier(.55,0,1,.45) {-i*7/8:.2f}s infinite"/>' for i in range(8))
    return (f'<mask id="fm"><rect x="0" y="{horizon}" width="{w}" height="{depth}" fill="url(#fade)"/></mask>'
            f'<g mask="url(#fm)" stroke="{BLUE}" stroke-width="1.2" opacity="{op}">{rad}{hor}</g>')

def header(num, title, sub="", y=72):
    s = f'<text x="60" y="{y}" class="mono" font-size="16" fill="{AMBER}" letter-spacing="2">{num}</text>'
    s += f'<text x="104" y="{y}" class="sans" font-size="34" font-weight="700" fill="{TEXT}">{esc(title)}</text>'
    if sub:
        s += f'<text x="1140" y="{y}" class="mono" font-size="14" fill="{MUTED}" text-anchor="end">{esc(sub)}</text>'
    return s

def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print("wrote", name, len(content))

# =============================================================== HERO
def hero():
    W, H = 1200, 470
    b = floor(W, H, 300, 520)
    # twinkling points
    for i, (x, y) in enumerate([(90, 60), (300, 40), (520, 90), (700, 50), (640, 180), (1130, 70), (1100, 250), (720, 400)]):
        b += f'<circle cx="{x}" cy="{y}" r="1.6" fill="{CYAN}" class="blink" style="animation-delay:{-i*.37:.2f}s"/>'
    # ---- left: text
    b += logo(86, 112, .34) + f'<text x="114" y="118" class="mono" font-size="15" fill="{CYAN}" letter-spacing="4">FOUNDER · SYNCOREHQ</text>'
    n = 14
    for i in range(n, 0, -1):
        t = i / n
        col = "#%02X%02X%02X" % (int(58 - 36*t), int(111 - 68*t), int(166 - 100*t))
        b += f'<text x="{68 + i*1.1:.1f}" y="{232 + i*1.1:.1f}" class="sans" font-size="104" font-weight="800" fill="{col}" letter-spacing="-2">Ahmed Emam</text>'
    b += f'<text x="68" y="232" class="sans" font-size="104" font-weight="800" fill="url(#name)" letter-spacing="-2">Ahmed Emam</text>'
    b += f'<text x="72" y="300" class="sans" font-size="23" font-weight="500" fill="{TEXT}">Senior Frappe / ERPNext Developer · Development Team Lead</text>'
    lines = ["6+ years in the Frappe ecosystem · 7+ in IT", "certified ERPNext professional",
             "clients in Saudi Arabia · UAE · Egypt", "building SyncoreHQ: audit · ERP · wallet in one core"]
    k = len(lines)
    b += f'<text x="72" y="352" class="mono" font-size="19" fill="{AMBER}">›</text>'
    for i, ln in enumerate(lines):
        b += f'<text x="96" y="352" class="mono" font-size="19" fill="{MUTED}" style="opacity:{0 if i else 1};animation:cyc {k*3}s linear {i*3}s infinite">{esc(ln)}</text>'
    b += (f'<circle cx="78" cy="401" r="4" fill="{AMBER}" class="blink"/>'
          f'<text x="94" y="406" class="mono" font-size="14" fill="{MUTED}">Riyadh, KSA  ·  syncorehq.com</text>')
    # ---- right: the stack
    ox, w, h = 940, 170, 30
    slabs = [(425, "cyan", "PYTHON · MARIADB"), (330, "blue", "FRAPPE / ERPNEXT"), (235, "slate", "SYNCOREHQ")]
    for i, (oy, shade, lab) in enumerate(slabs):
        if i:  # data flowing up from the slab below
            for dx in (-80, 0, 80):
                b += f'<line x1="{ox+dx}" y1="{oy+95-h-85+abs(dx)*.3:.0f}" x2="{ox+dx}" y2="{oy-60+abs(dx)*.3:.0f}" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" class="flow" opacity=".8"/>'
        g = box(ox, oy, w, w, h, shade)
        tcol = "#06231F" if shade == "cyan" else ("#0C1118" if shade == "blue" else "#E6EDF3")
        g += f'<text transform="matrix({C},{S},0,1,{ox-w*C+16:.1f},{oy-w*S-1:.1f})" class="mono" font-size="12" font-weight="700" fill="{tcol}" letter-spacing="1.5">{esc(lab)}</text>'
        for j in range(3):  # status lights on the right face
            g += f'<circle cx="{ox+22+j*16}" cy="{oy-15-(22+j*16)*.577:.1f}" r="2.6" fill="{AMBER if j==0 else "#FFFFFF"}" class="blink" style="animation-delay:{-(i+j)*.5}s"/>'
        if i == 2:  # app blocks on top
            for u, v, hh, sh in [(100, 100, 52, "blue"), (100, 26, 34, "cyan"), (26, 100, 40, "amber")]:  # Audit, ERP, Wallet
                g += box(ox + (u-v)*C, oy - h - (u+v)*S, 36, 36, hh, sh, .5)
        b += f'<g class="bob" style="animation-delay:{-i*.9}s">{g}</g>'
    css = "@keyframes cyc{0%{opacity:0}2%,23%{opacity:1}25%,100%{opacity:0}}"
    write("hero.svg", svg(W, H, b, css, "Ahmed Emam — Founder of SyncoreHQ. Senior Frappe / ERPNext Developer, Development Team Lead. Riyadh, KSA."))

# =============================================================== ABOUT
def about():
    W, H = 1200, 500
    b = header("02", "About", "whoami")
    x, y, w, h = 60, 112, 668, 336
    for i in range(10, 0, -2):
        b += f'<rect x="{x+i}" y="{y+i}" width="{w}" height="{h}" rx="16" fill="#151C26"/>'
    b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#0C1118" stroke="{LINE}" stroke-width="1.5"/>'
    b += "".join(f'<circle cx="{x+26+i*20}" cy="{y+24}" r="5.5" fill="{c}"/>' for i, c in enumerate([AMBER, CYAN, BLUE]))
    b += f'<text x="{x+w/2}" y="{y+29}" class="mono" font-size="13" fill="{MUTED}" text-anchor="middle">ahmed_emam.py</text>'
    b += f'<line x1="{x}" y1="{y+46}" x2="{x+w}" y2="{y+46}" stroke="{LINE}"/>'
    K = lambda s: f'<tspan fill="{CYAN}">{esc(s)}</tspan>'
    Q = lambda s: f'<tspan fill="#FFD9A8">{esc(chr(34)+s+chr(34))}</tspan>'
    D = lambda s: f'<tspan fill="{MUTED}">{esc(s)}</tspan>'
    T = lambda s: esc(s)
    code = [
        K("class ") + f'<tspan fill="#FFFFFF" font-weight="700">AhmedEmam</tspan>' + D("(") + T("Document") + D("):"),
        T("    role     ") + D("= ") + Q("Senior Frappe / ERPNext Developer"),
        T("    founder  ") + D("= ") + Q("SyncoreHQ"),
        T("    company  ") + D("= ") + Q("Hawsabah"),
        T("    location ") + D("= ") + Q("Riyadh, KSA"),
        T("    focus    ") + D("= [") + Q("custom apps") + D(", ") + Q("integrations") + D(", ") + Q("team leadership") + D("]"),
        T("    clients  ") + D("= [") + Q("Saudi Arabia") + D(", ") + Q("UAE") + D(", ") + Q("Egypt") + D("]"),
        "",
        "    " + K("def ") + f'<tspan fill="#FFFFFF">motto</tspan>' + D("(") + T("self") + D("):"),
        "        " + K("return ") + Q("Code · Lead · Innovate"),
    ]
    for i, ln in enumerate(code):
        yy = y + 76 + i*26.5
        b += f'<text x="{x+26}" y="{yy}" class="mono pre fadein" xml:space="preserve" font-size="14.5" fill="{TEXT}" style="animation-delay:{.15+i*.12:.2f}s">{ln}</text>'
    # stats as columns
    stats = [(820, 130, "6+", "years", "Frappe / ERPNext", "cyan"), (955, 155, "7+", "years", "in IT", "blue"), (1090, 185, "90+", "public", "repositories", "amber")]
    base = 392
    for i, (cx, hh, num, l1, l2, sh) in enumerate(stats):
        b += f'<ellipse cx="{cx}" cy="{base-22}" rx="52" ry="20" fill="#000" opacity=".35"/>'
        g = box(cx, base, 46, 46, hh, sh)
        g += f'<text x="{cx}" y="{base-hh-62}" class="sans" font-size="36" font-weight="800" fill="{TEXT}" text-anchor="middle">{num}</text>'
        b += f'<g class="rise" style="animation-delay:{.3+i*.2}s">{g}</g>'
        b += f'<text x="{cx}" y="{base+34}" class="sans" font-size="15" font-weight="600" fill="{TEXT}" text-anchor="middle">{l1}</text>'
        b += f'<text x="{cx}" y="{base+54}" class="sans" font-size="14" fill="{MUTED}" text-anchor="middle">{l2}</text>'
    write("about.svg", svg(W, H, b, "", "About: Senior Frappe / ERPNext Developer at Hawsabah, Riyadh. 6+ years Frappe / ERPNext, 7+ years in IT, 90+ public repositories."))

# =============================================================== STACK
STACK = [
    ("ERP",         BLUE,  ["ERPNext", "Frappe Framework", "Frappe UI", "Bench"]),
    ("LANGUAGES",   CYAN,  ["Python", "JavaScript", "SQL", "Jinja", "HTML / CSS"]),
    ("DATA",        AMBER, ["MariaDB", "MySQL", "Redis"]),
    ("INTEGRATION", CYAN,  ["REST APIs", "Custom APIs", "Webhooks"]),
    ("DEVOPS",      BLUE,  ["Jenkins", "ArgoCD", "Nginx", "Supervisor"]),
    ("GIT",         AMBER, ["Git", "GitHub", "GitLab", "Bitbucket"]),
]
def stack():
    W, H = 1200, 644
    b = header("03", "Tech stack", "what I build with")
    k = 0
    for r, (cat, col, items) in enumerate(STACK):
        y = 118 + r*84
        b += f'<text x="60" y="{y+32}" class="mono" font-size="13" fill="{MUTED}" letter-spacing="2.5">{cat}</text>'
        x = 200
        for it in items:
            kw = 58 + len(it)*10.4
            g = (f'<rect x="{x}" y="{y+8}" width="{kw:.0f}" height="50" rx="13" fill="#080B10"/>'
                 f'<rect x="{x}" y="{y+6}" width="{kw:.0f}" height="50" rx="13" fill="#161D27"/>'
                 f'<rect x="{x}" y="{y}" width="{kw:.0f}" height="50" rx="13" fill="#222B37" stroke="#3D4B5E" stroke-width="1.2"/>'
                 f'<rect x="{x+10}" y="{y+1.5}" width="{kw-20:.0f}" height="1.5" rx="1" fill="#FFFFFF" opacity=".28"/>'
                 f'<circle cx="{x+22}" cy="{y+25}" r="5" fill="{col}"/>'
                 f'<text x="{x+38}" y="{y+31}" class="sans" font-size="17" font-weight="600" fill="{TEXT}">{esc(it)}</text>')
            b += f'<g class="bobs" style="animation-delay:{-k*.31:.2f}s">{g}</g>'
            x += kw + 16; k += 1
    # decorative cluster
    for i, (ox, oy, w, hh, sh) in enumerate([(1085, 480, 54, 70, "ink"), (1040, 385, 40, 40, "blue"), (1120, 300, 30, 30, "cyan"), (1065, 235, 20, 20, "amber")]):
        b += f'<g class="bob" style="animation-delay:{-i*1.1}s">{box(ox, oy, w, w, hh, sh)}</g>'
    write("stack.svg", svg(W, H, b, "", "Tech stack: " + "; ".join(f"{c.title()}: {', '.join(i)}" for c, _, i in STACK)))

# =============================================================== JOURNEY
JOURNEY = [  # role line 1, role line 2, company, years, shade
    ("IT System", "Manager", "Riadco 2000", "2019 – 2021", "ink"),
    ("ERPNext", "Consultant", "Makkatech · remote", "2020 – 2022", "ink"),
    ("Techno-Functional", "Consultant", "ERP Cloud Systems", "2021 – 2022", "ink"),
    ("Frappe / ERPNext", "Developer", "Creative Adv. Tech", "2022 – 2024", "blue"),
    ("Development", "Team Lead", "Creative Adv. Tech", "2024 – 2025", "blue"),
    ("Development", "Team Lead", "Feedco", "2025 – 2026", "blue"),
    ("Senior Frappe", "Developer", "Hawsabah", "2026 – now", "cyan"),
]
def journey():
    W, H = 1200, 572
    b = header("04", "Journey", "2019 → now")
    b += floor(W, H, 400, 600, .16)
    base, heights, tops = 420, [36, 68, 100, 134, 168, 202, 240], []
    for i, (r1, r2, co, yrs, sh) in enumerate(JOURNEY):
        cx, hh = 120 + i*160, heights[i]
        tops.append((cx, base - hh - 27))
        b += f'<g class="rise" style="animation-delay:{i*.18:.2f}s">{box(cx, base, 54, 54, hh, sh)}</g>'
        b += (f'<text x="{cx}" y="{base+40}" class="sans" font-size="16" font-weight="700" fill="{TEXT}" text-anchor="middle">{esc(r1)}</text>'
              f'<text x="{cx}" y="{base+61}" class="sans" font-size="16" font-weight="700" fill="{TEXT}" text-anchor="middle">{esc(r2)}</text>'
              f'<text x="{cx}" y="{base+86}" class="sans" font-size="13.5" fill="{MUTED}" text-anchor="middle">{esc(co)}</text>'
              f'<text x="{cx}" y="{base+110}" class="mono" font-size="12.5" fill="{AMBER}" text-anchor="middle">{yrs}</text>')
    b += f'<polyline points="{pts(*tops)}" fill="none" stroke="{AMBER}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="flow fadein" style="animation:flow 1.6s linear infinite,fadein .6s 1.4s both"/>'
    for i, (x, y) in enumerate(tops):
        b += f'<circle cx="{x}" cy="{y}" r="5" fill="{AMBER}" stroke="{BG0}" stroke-width="2" class="fadein" style="animation-delay:{.4+i*.18:.2f}s"/>'
    x, y = tops[-1]
    b += (f'<g class="bobs"><rect x="{x-30}" y="{y-56}" width="60" height="26" rx="13" fill="{AMBER}"/>'
          f'<text x="{x}" y="{y-38}" class="mono" font-size="13" font-weight="700" fill="#2A1800" text-anchor="middle" letter-spacing="1.5">NOW</text></g>')
    write("journey.svg", svg(W, H, b, "", "Career journey: " + "; ".join(f"{a} {b_} at {c} ({y})" for a, b_, c, y, _ in JOURNEY)))

# =============================================================== EXPERTISE
EXPERTISE = [
    ("Accounting", "GL · AR · AP · Budgets"), ("Sales", "Orders · Invoices"), ("Purchasing", "Suppliers · Purchase orders"),
    ("Stock & Inventory", "Batch · Serial · Warehouses"),
    ("Manufacturing", "BOM · Work orders · QC"), ("HR & Payroll", "Leave · Attendance · Salary"), ("CRM", "Leads · Opportunities"),
    ("Projects", "Tasks · Time · Billing"),
]
def expertise():
    W, H = 1200, 505
    b = header("05", "ERP modules", "functional depth")
    cyc = ["blue", "cyan", "ink", "amber", "ink", "blue", "amber", "cyan"]
    for i, (name, sub) in enumerate(EXPERTISE):
        cx, cy = 180 + (i % 4)*280, 218 + (i // 4)*192
        b += f'<ellipse cx="{cx}" cy="{cy-10}" rx="40" ry="14" fill="#000" class="shadow" style="animation-delay:{-i*.5}s"/>'
        b += f'<g class="bob" style="animation-delay:{-i*.5}s">{box(cx, cy-14, 44, 44, 44, cyc[i])}</g>'
        b += (f'<text x="{cx}" y="{cy+34}" class="sans" font-size="18" font-weight="700" fill="{TEXT}" text-anchor="middle">{esc(name)}</text>'
              f'<text x="{cx}" y="{cy+56}" class="sans" font-size="13.5" fill="{MUTED}" text-anchor="middle">{esc(sub)}</text>')
    write("expertise.svg", svg(W, H, b, "", "ERP modules: " + "; ".join(f"{n} ({s})" for n, s in EXPERTISE)))

# =============================================================== small pieces
def bar(name, num, title, sub):
    write(name, svg(1200, 104, header(num, title, sub, 64), "", title))

PROJECTS = [  # file, repo, owner, line1, line2, tags, shade
    ("biotime", "BioTime-API-Integration", "accurate-systems", "Syncs BioTime attendance devices with ERPNext:", "employee logs, check-ins and device data.", "Python · ERPNext · REST", "amber"),
    ("frappe-client", "frappe-client", "ahmedemamhatem", "Frappe-like Python wrapper for the Frappe REST API:", "login, get, insert, update, delete.", "Python · REST API", "cyan"),
    ("frappe-offline", "frappe_offline", "ahmedemamhatem", "Frappe Sync — keeps Frappe data in sync", "for sites that work offline.", "Python · Frappe", "blue"),
    ("hr-system", "hr_system", "ahmedemamhatem", "HR system built as a Frappe app.", "", "Python · Frappe · HR", "blue"),
    ("project-management", "project_management", "ahmedemamhatem", "Project management app for Frappe / ERPNext.", "", "Frappe · Projects", "cyan"),
    ("timesheet-payroll", "timesheet_payroll", "ahmedemamhatem", "Timesheet-driven payroll for ERPNext.", "", "Python · ERPNext · Payroll", "amber"),
]
def projects():
    for f, repo, owner, l1, l2, tags, sh in PROJECTS:
        b = f'<g class="bob">{box(520, 104, 34, 34, 34, sh)}</g>'
        b += (f'<text x="36" y="50" class="mono" font-size="13" fill="{MUTED}">{esc(owner)} /</text>'
              f'<text x="36" y="82" class="mono" font-size="23" font-weight="700" fill="{CYAN}">{esc(repo)}</text>'
              f'<text x="36" y="124" class="sans" font-size="16.5" fill="{TEXT}">{esc(l1)}</text>'
              f'<text x="36" y="148" class="sans" font-size="16.5" fill="{TEXT}">{esc(l2)}</text>'
              f'<text x="36" y="190" class="mono" font-size="13" fill="{AMBER}">{esc(tags)}</text>'
              f'<text x="564" y="190" class="mono" font-size="13" fill="{MUTED}" text-anchor="end">open →</text>')
        write(f"project-{f}.svg", svg(600, 216, b, "", f"{owner}/{repo}: {l1} {l2}".strip()))

CONTACT = [("website", "SyncoreHQ", "syncorehq.com", "url(#brand)", "#2F5F8F", "#0C1118"), ("linkedin", "LinkedIn", "connect", "#4F8FD0", "#3A6FA6", "#0C1118"),
           ("email", "Email", "drop a line", "#3FB6A8", "#2A8279", "#06231F"), ("whatsapp", "WhatsApp", "let's chat", "#313D4D", "#171E28", "#E6EDF3"),
           ("telegram", "Telegram", "message me", "#F2A35E", "#B85F2A", "#2A1800")]
def contact():
    for f, name, sub, face, side, ink in CONTACT:
        body = (f'<rect x="6" y="16" width="288" height="84" rx="20" fill="{side}"/>'
                f'<g class="bobs"><rect x="6" y="4" width="288" height="84" rx="20" fill="{face}" stroke="#FFFFFF" stroke-opacity=".3" stroke-width="1.2"/>'
                f'<text x="150" y="46" class="sans" font-size="27" font-weight="700" fill="{ink}" text-anchor="middle">{name}</text>'
                f'<text x="150" y="71" class="mono" font-size="15" fill="{ink}" opacity=".85" text-anchor="middle">{sub} →</text></g>')
        s_ = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 104" width="300" height="104" role="img" aria-label="{name}"><title>{name}</title>'
              f'<style>{STYLE}</style><defs><linearGradient id="brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5B9DD9"/><stop offset=".55" stop-color="#4F8FD0"/><stop offset="1" stop-color="#3FB6A8"/></linearGradient></defs>{body}</svg>')
        write(f"btn-{f}.svg", s_)

# =============================================================== SYNCOREHQ
def syncore():
    W, H = 1200, 372
    b = header("01", "SyncoreHQ", "my startup · syncorehq.com")
    b += logo(150, 222, 1.55)
    b += wordmark(262, 196, 58)
    b += (f'<text x="264" y="236" class="sans" font-size="22" font-weight="600" fill="{TEXT}">One core. Every operation, in sync.</text>'
          f'<text x="264" y="278" class="sans" font-size="15.5" fill="{MUTED}">Products that run your operations: an AI financial auditor, a complete</text>'
          f'<text x="264" y="301" class="sans" font-size="15.5" fill="{MUTED}">business-management ERP, and an app for money-service companies.</text>')
    chips = [("Bank-grade encryption", "roles · full audit trail", BLUE), ("No lock-in", "works with any data", CYAN), ("Minutes, not months", "fast to set up", AMBER), ("Arabic & English", "bilingual, RTL-ready", BLUE)]
    for i, (t, sub, col) in enumerate(chips):
        y = 112 + i*60
        g = (f'<rect x="850" y="{y+5}" width="290" height="46" rx="12" fill="#080B10"/>'
             f'<rect x="850" y="{y}" width="290" height="46" rx="12" fill="#222B37" stroke="#3D4B5E" stroke-width="1.2"/>'
             f'<circle cx="872" cy="{y+23}" r="5" fill="{col}"/>'
             f'<text x="890" y="{y+21}" class="sans" font-size="15" font-weight="700" fill="{TEXT}">{esc(t)}</text>'
             f'<text x="890" y="{y+37}" class="mono" font-size="11.5" fill="{MUTED}">{esc(sub)}</text>')
        b += f'<g class="bobs" style="animation-delay:{-i*.6}s">{g}</g>'
    write("syncore.svg", svg(W, H, b, "", "SyncoreHQ — One core. Every operation, in sync. An AI financial auditor, a business-management ERP, and an app for money-service companies. Secure, bilingual, no lock-in."))

PRODUCTS = [  # file, name, tag, lines, foot, shade, colour, new
    ("audit", "Audit", "AI FINANCIAL AUDIT", ["Finds fraud, anomalies and risk", "in minutes: Benford's law,", "ratios and a 0–100 health score."], "ERPNext · Excel · CSV · PDF", "blue", BLUE, False),
    ("erp", "ERP", "BUSINESS MANAGEMENT", ["Accounting, sales, stock and", "people on one core, with live", "dashboards and AI insights."], "multi-company · multi-currency", "cyan", CYAN, False),
    ("wallet", "Wallet", "FOR MONEY-SERVICE COMPANIES", ["Cash boxes and e-wallets in", "one place: top-ups, cash-outs", "and transfers in seconds."], "12 operations · 14 reports · offline", "amber", AMBER, True),
]
def products():
    for f, name, tag, lines, foot, sh, col, new in PRODUCTS:
        b = f'<g class="bob">{box(64, 104, 36, 36, 36, sh)}</g>'
        if new:
            b += f'<rect x="318" y="34" width="54" height="26" rx="13" fill="{AMBER}"/><text x="345" y="52" class="mono" font-size="12.5" font-weight="700" fill="#2A1800" text-anchor="middle" letter-spacing="1">NEW</text>'
        b += (f'<text x="32" y="156" class="sans" font-size="29" font-weight="800" fill="{TEXT}" letter-spacing="-.5">Syncore<tspan fill="url(#brand)">HQ</tspan> <tspan fill="{col}">{name}</tspan></text>'
              f'<text x="32" y="184" class="mono" font-size="13" fill="{col}" letter-spacing="1.5">{tag}</text>')
        for i, ln in enumerate(lines):
            b += f'<text x="32" y="{224+i*27}" class="sans" font-size="19" fill="{TEXT}">{esc(ln)}</text>'
        b += f'<text x="32" y="322" class="mono" font-size="13.5" fill="{MUTED}">{esc(foot)}</text>'
        write(f"product-{f}.svg", svg(400, 348, b, "", f"SyncoreHQ {name} — " + " ".join(lines)))

def certs():
    W, H = 1200, 232
    b = header("07", "Credentials", "")
    items = [("Certified ERPNext Professional", "Frappe Technologies", CYAN), ("Management Information Systems", "Bachelor's degree", BLUE), ("Arabic · English", "native · professional working", AMBER)]
    for i, (t, s, col) in enumerate(items):
        x = 60 + i*368
        b += (f'<rect x="{x}" y="118" width="344" height="78" rx="16" fill="#080B10"/>'
              f'<rect x="{x}" y="110" width="344" height="78" rx="16" fill="#222B37" stroke="#3D4B5E" stroke-width="1.2"/>'
              f'<rect x="{x}" y="110" width="8" height="78" rx="4" fill="{col}"/>'
              f'<text x="{x+30}" y="144" class="sans" font-size="16.5" font-weight="700" fill="{TEXT}">{esc(t)}</text>'
              f'<text x="{x+30}" y="168" class="mono" font-size="13.5" fill="{MUTED}">{esc(s)}</text>')
    write("certs.svg", svg(W, H, b, "", "Credentials: " + "; ".join(f"{t} ({s})" for t, s, _ in items)))

def footer():
    W, H = 1200, 260
    b = floor(W, H, 120, 600, .6)
    b += logo(600, 52, .5)
    b += (f'<text x="600" y="122" class="sans" font-size="40" font-weight="800" fill="url(#name)" text-anchor="middle" letter-spacing="-.5">One core. Every operation, in sync.</text>'
          f'<text x="600" y="186" class="mono" font-size="15" fill="{TEXT}" text-anchor="middle">Ahmed Emam  ·  founder, SyncoreHQ  ·  syncorehq.com</text>'
          f'<text x="600" y="216" class="mono" font-size="13" fill="{MUTED}" text-anchor="middle">thanks for visiting</text>')
    for i, (ox, oy, w, sh) in enumerate([(150, 210, 40, "blue"), (1050, 210, 40, "cyan"), (90, 110, 20, "amber"), (1115, 105, 20, "slate")]):
        b += f'<g class="bob" style="animation-delay:{-i*1.2}s">{box(ox, oy, w, w, w, sh)}</g>'
    write("footer.svg", svg(W, H, b, "", "SyncoreHQ — One core. Every operation, in sync."))

def placeholders():
    """Shown only until the 'Profile activity' workflow has run once; the workflow overwrites them."""
    d = OUT.parent / "profile-3d-contrib"; d.mkdir(exist_ok=True)
    for f, t in [("profile-night-rainbow.svg", "3D contribution calendar"), ("snake.svg", "Contribution snake")]:
        if (d / f).exists() and "placeholder" not in (d / f).read_text()[:400]:
            continue
        b = (f'<g class="bob">{box(110, 96, 30, 30, 30, "cyan")}</g>'
             f'<text x="170" y="62" class="sans" font-size="24" font-weight="700" fill="{TEXT}">{t}</text>'
             f'<text x="170" y="92" class="mono" font-size="14" fill="{MUTED}">generated by the "Profile activity" workflow — run it once from the Actions tab</text>')
        (d / f).write_text(svg(1200, 140, b, "", "placeholder: " + t), encoding="utf-8")

if __name__ == "__main__":
    placeholders()
    hero(); syncore(); products(); about(); stack(); journey(); expertise(); certs(); projects(); contact(); footer()
    bar("bar-projects.svg", "06", "Open source", "tap a card to open the repo")
    bar("bar-activity.svg", "08", "Activity", "live · refreshed daily")
    bar("bar-contact.svg", "09", "Let's talk", "ERPNext · Frappe · SyncoreHQ")
