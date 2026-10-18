"""Собирает dark_mode.svg и light_mode.svg для README профиля в стиле neofetch.
Запуск: python3 gen.py  (ASCII-рисунок берётся из art.txt рядом)."""
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
    "dark": dict(bg="#161b22", border="#30363d", art="#e3b341", key="#ffa657", val="#a5d6ff", dot="#616e7f", head="#c9d1d9"),
    "light": dict(bg="#f6f8fa", border="#d0d7de", art="#9a6700", key="#953800", val="#0a3069", dot="#c2cfde", head="#24292f"),
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


def build(theme):
    t = THEMES[theme]
    rows = max(len(ART), len(INFO))
    art = ART + [""] * (rows - len(ART))
    ipad = (rows - len(INFO)) // 2
    info = [None] * ipad + INFO + [None] * (rows - len(INFO) - ipad)
    # рисунок по центру по вертикали относительно текста
    pad_top = (rows - len(ART)) // 2
    art = [""] * pad_top + ART + [""] * (rows - len(ART) - pad_top)

    width = round((ART_W + 3 + INFO_W) * CHAR + 48)
    height = rows * LINE + 44
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,\'JetBrains Mono\',Menlo,monospace" '
        f'width="{width}px" height="{height}px" font-size="{FONT}px">',
        "<style>"
        "@font-face{src:local('Consolas'),local('Consolas Bold');font-family:'ConsolasFallback';font-display:swap;"
        "-webkit-size-adjust:109%;size-adjust:109%}"
        f".a{{fill:{t['art']}}}.k{{fill:{t['key']}}}.v{{fill:{t['val']}}}.c{{fill:{t['dot']}}}"
        f".h{{fill:{t['head']};font-weight:bold}}text,tspan{{white-space:pre}}"
        "</style>",
        f'<rect width="{width}px" height="{height}px" rx="15" fill="{t["bg"]}" stroke="{t["border"]}"/>',
        f'<text x="24" y="{24 + LINE - 5}" xml:space="preserve">',
    ]
    for i in range(rows):
        dy = "0" if i == 0 else str(LINE)
        a = art[i].ljust(ART_W)
        parts = [f'<tspan x="24" dy="{dy}" class="a">{escape(a)}   </tspan>']
        for cls, txt in info_spans(info[i]):
            parts.append(f'<tspan class="{cls}">{escape(txt)}</tspan>')
        out.append("".join(parts))
    out.append("</text></svg>")
    (HERE / f"{theme}_mode.svg").write_text("\n".join(out), encoding="utf-8")


for th in THEMES:
    build(th)
print("ok")
