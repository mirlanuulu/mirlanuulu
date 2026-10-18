"""Собирает dark_mode.svg и light_mode.svg для README профиля в стиле neofetch.
Запуск: python3 gen.py  (глобус — из frames.json, его делает globe.mjs; без него берётся art.txt)."""
from html import escape
from pathlib import Path

HERE = Path(__file__).parent
ART = (HERE / "art.txt").read_text(encoding="utf-8").splitlines()
ART_W = max(len(l) for l in ART)
INFO_W = 60  # ширина правой колонки в символах

# (ключ, значение) — None = пустая строка, ("#", заголовок) = разделитель
INFO = [
    ("@", "yusuf@mirlanuulu"),
    ("OS", "Kyrgyzstan → remote, GMT+3"),
    ("Uptime", "coding since 2023, shipping since 2024"),
    ("Host", "Freelance · ABM Express, domix.kg"),
    ("Kernel", "Frontend Developer"),
    ("IDE", "VS Code + Claude Code"),
    None,
    ("Languages.Programming", "TypeScript, JavaScript, HTML, CSS"),
    ("Languages.Real", "Kyrgyz, Russian, Turkish"),
    ("Stack.UI", "React, Next.js, Tailwind CSS, GSAP"),
    ("Stack.Data", "REST API, Supabase, PostgreSQL, Drizzle"),
    None,
    ("#", "Projects"),
    ("ABM.Express", "cargo CRM · admin panel, 4 roles"),
    ("domix.kg", "e-commerce · live store, real orders"),
    ("WhatsApp.Bot", "AI sales bot · LLM + Telegram"),
    ("glee", "invitation sites · GSAP, KG/RU"),
    None,
    ("#", "Contact"),
    ("Telegram", "@YusMrln"),
    ("Email", "mirlanuulu.04@gmail.com"),
    ("CV", "cv-yusuf-mirlanuulu.vercel.app"),
]

THEMES = {
    "dark": dict(bg="#161b22", border="#30363d", art="#e3b341", kg="#ff7b72", key="#ffa657", val="#a5d6ff", dot="#616e7f", head="#c9d1d9"),
    "light": dict(bg="#f6f8fa", border="#d0d7de", art="#9a6700", kg="#cf222e", key="#953800", val="#0a3069", dot="#c2cfde", head="#24292f"),
}

FONT = 15
LINE = 20
CHAR = 9.05  # примерная ширина символа моноширинного шрифта при 15px


def info_spans(item):
    """Возвращает список (класс, текст) для одной строки правой колонки."""
    if item is None:
        return []
    k, v = item
    if k == "@":
        return [("h", v + " "), ("c", "—" * (INFO_W - len(v) - 1))]
    if k == "#":
        t = f"- {v} "
        return [("h", t), ("c", "—" * (INFO_W - len(t)))]
    left = f"{k}:"
    dots = INFO_W - len(left) - len(v) - 2
    return [("k", left), ("c", " " + "." * max(dots, 1) + " "), ("v", v)]


import json

FRAMES_FILE = HERE / "frames.json"
CYCLE = 9  # секунд на полный оборот глобуса


def build(theme):
    t = THEMES[theme]
    if FRAMES_FILE.exists():
        data = json.loads(FRAMES_FILE.read_text(encoding="utf-8"))
        frames, art_w, art_h = data["frames"], data["cols"], data["rows"]
    else:  # статичный рисунок из art.txt
        frames, art_w, art_h = [[[("a", l)] for l in ART]], ART_W, len(ART)
    rows = max(art_h, len(INFO))
    ipad = (rows - len(INFO)) // 2
    info = [None] * ipad + INFO + [None] * (rows - len(INFO) - ipad)
    apad = (rows - art_h) // 2

    info_x = round(24 + (art_w + 4) * CHAR)
    width = round(info_x + INFO_W * CHAR + 24)
    height = rows * LINE + 44
    y0 = 24 + LINE - 5
    n = len(frames)
    share = 100 / n
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,\'JetBrains Mono\',Menlo,monospace" '
        f'width="{width}px" height="{height}px" font-size="{FONT}px">',
        "<style>"
        "@font-face{src:local('Consolas'),local('Consolas Bold');font-family:'ConsolasFallback';font-display:swap;"
        "-webkit-size-adjust:109%;size-adjust:109%}"
        f".a{{fill:{t['art']}}}.kg{{fill:{t['kg']};font-weight:bold}}.o{{fill:{t['dot']}}}"
        f".k{{fill:{t['key']}}}.v{{fill:{t['val']}}}.c{{fill:{t['dot']}}}"
        f".h{{fill:{t['head']};font-weight:bold}}text,tspan{{white-space:pre}}"
        + (
            f".f{{opacity:0;animation:spin {CYCLE}s step-end infinite}}"
            f"@keyframes spin{{0%{{opacity:1}}{share:.4f}%{{opacity:0}}100%{{opacity:0}}}}"
            if n > 1 else ""
        )
        + "</style>",
        f'<rect width="{width}px" height="{height}px" rx="15" fill="{t["bg"]}" stroke="{t["border"]}"/>',
    ]
    for fi, fr in enumerate(frames):
        delay = -(CYCLE - fi * CYCLE / n) if fi else 0
        attr = f' class="f" style="animation-delay:{delay:.4f}s"' if n > 1 else ""
        out.append(f'<text x="24" y="{y0 + apad * LINE}" xml:space="preserve"{attr}>')
        for i, runs in enumerate(fr):
            dy = "0" if i == 0 else str(LINE)
            parts = "".join(f'<tspan class="{c}">{escape(txt)}</tspan>' for c, txt in runs)
            out.append(f'<tspan x="24" dy="{dy}">{parts}</tspan>')
        out.append("</text>")
    out.append(f'<text x="{info_x}" y="{y0}" xml:space="preserve">')
    for i in range(rows):
        dy = "0" if i == 0 else str(LINE)
        spans = "".join(f'<tspan class="{c}">{escape(x)}</tspan>' for c, x in info_spans(info[i])) or " "
        out.append(f'<tspan x="{info_x}" dy="{dy}">{spans}</tspan>')
    out.append("</text></svg>")
    (HERE / f"{theme}_mode.svg").write_text("\n".join(out), encoding="utf-8")


for th in THEMES:
    build(th)
print("ok")
