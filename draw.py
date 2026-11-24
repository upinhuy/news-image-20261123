#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news image (1024x1024 PNG).

Deterministic: fixed story list, no randomness, no timestamps, no network.
Run: python3 draw.py  -> writes entry.png next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (17, 24, 39)
PAPER = (247, 245, 239)
NAVY = (16, 38, 63)
GOLD = (201, 162, 39)
MUTED = (100, 116, 139)
LINE = (203, 213, 225)
CARD = (255, 255, 255)
ROW_ALT = (238, 236, 228)
PILL_BG = (226, 232, 240)
PILL_INK = (30, 41, 59)

CAT = {
    "WAR": (185, 28, 28),
    "CLIMATE": (21, 128, 61),
    "TECH": (29, 78, 216),
    "POLITICS": (109, 40, 217),
    "MARKETS": (15, 118, 110),
    "SPORT": (194, 65, 12),
    "CULTURE": (190, 24, 93),
    "US": (51, 65, 85),
    "WORLD": (30, 58, 95),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 40)
F_KICKER = font("DejaVuSans-Bold.ttf", 13)
F_SUB = font("DejaVuSans.ttf", 13)
F_TAG = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_LEAD_BODY = font("DejaVuSans.ttf", 12)
F_LEAD_SRC = font("DejaVuSans-Bold.ttf", 10)
F_SEC = font("DejaVuSans-Bold.ttf", 14)
F_TIME = font("DejaVuSans-Bold.ttf", 11)
F_ROW = font("DejaVuSans.ttf", 11)
F_PILL = font("DejaVuSans-Bold.ttf", 9)
F_FOOT = font("DejaVuSans.ttf", 9)


LEADS = [
    (
        "CLIMATE",
        "COP31 collapses: no deal as EU rejects draft with no fossil fuels",
        "Longest COP on record ends two days late; Guterres \u201cdeeply disappointed\u201d.",
        "REUTERS",
    ),
    (
        "WAR",
        "Ukraine sinks Russian warship in Libya; NATO meets over missiles in Poland",
        "Zelenskyy: seven naval drones sank the corvette Merkury at Benghazi.",
        "AP / REUTERS",
    ),
    (
        "TECH",
        "Nvidia reinstates Jensen Huang as CEO; shares soar about 31%",
        "Board votes unanimously after input from U.S. officials; Wall Street rallies.",
        "AP",
    ),
]

# (UTC time, category, headline, source)
TIMELINE = [
    ("00:10", "CLIMATE", "COP31 blame game: Australian opposition demands minister Bowen resign; Pacific nations despair", "REUTERS"),
    ("00:45", "CLIMATE", "UN chief Guterres \u201cdeeply disappointed\u201d as climate talks end with no final deal", "REUTERS"),
    ("01:20", "WORLD", "Indonesia candy factory fire: 24 dead confirmed, about 30 workers still missing", "REUTERS"),
    ("02:05", "SPORT", "Alcaraz beats world No. 1 Zverev 6-2, 7-6 to win his first ATP Finals title in Turin", "REUTERS"),
    ("02:40", "SPORT", "Broncos beat Raiders 38-24 as rookie Coleman runs for three touchdowns", "AP"),
    ("03:15", "WORLD", "Mexico captures \u201cEl Chapo Isidro\u201d, an FBI most-wanted drug lord; U.S. drone helped track him", "AP"),
    ("03:50", "WORLD", "Eight suspects arrested after firing on Mexican soldiers restoring order in Sinaloa", "BBC"),
    ("04:30", "WAR", "Two more tankers hit near Hormuz as Iran blames mines; Tehran calls strait talks \u201cpointless\u201d", "REUTERS"),
    ("05:10", "SPORT", "FIFA picks U.S. to co-host 2031 Women\u2019s World Cup; UK to host the 2035 edition", "AP"),
    ("05:45", "POLITICS", "Democrats clinch 258 House seats, largest majority since 1992, after N. Carolina recount", "AP"),
    ("06:20", "WORLD", "South Korea\u2019s education minister quits over exam chaos and AI-cheating rule changes", "REUTERS"),
    ("06:55", "POLITICS", "EU proposes sweeping new Russia sanctions targeting banks, crypto and sports events", "AP"),
    ("07:30", "WORLD", "India pledges $1.62bn economic package to flood-hit Nepal in reset of ties", "REUTERS"),
    ("08:05", "WAR", "NATO council meets in Brussels after Russian missiles fell in Poland", "REUTERS"),
    ("08:40", "WAR", "Zelenskyy: Ukraine sank Russian corvette Merkury at a Libyan naval base", "AP"),
    ("09:15", "WAR", "Kremlin calls Ukraine\u2019s Baltic cargo-ship strike \u201cterrorist activity\u201d", "REUTERS"),
    ("09:50", "WAR", "Dymer apartment strike toll rises to 11; 14 people still missing under rubble", "AP"),
    ("10:25", "WAR", "Russian strike on Kryvyi Rih kills a child and a young woman; 25 apartment blocks damaged", "AP"),
    ("11:00", "WAR", "Trump: Iran wants a deal to end hostilities, but not one \u201cacceptable\u201d to him", "AP"),
    ("11:35", "WAR", "Bahrain: Iranian attack hits civilian industrial site, injuring two people", "REUTERS"),
    ("12:10", "WAR", "Vance declines to say if he would have authorised strikes to stop Iran\u2019s nuclear work", "REUTERS"),
    ("12:45", "POLITICS", "Senate GOP open to limiting Iran war funding in a deal to avoid a Dec. 11 shutdown", "WASH. POST"),
    ("13:20", "POLITICS", "U.S. intelligence chief: Trump calling Putin a \u201cfriend\u201d was \u201centirely appropriate\u201d", "GUARDIAN"),
    ("13:55", "MARKETS", "U.S. stocks soar: Nasdaq futures up about 7% as chip stocks lead the rebound", "REUTERS"),
    ("14:30", "TECH", "Nvidia board unanimously reinstates Jensen Huang as president and CEO", "AP"),
    ("15:05", "MARKETS", "Nvidia shares jump about 31% before the open after Huang\u2019s return", "REUTERS"),
    ("15:40", "TECH", "U.S. to blacklist Asian AI firm Megaspeed after the Nvidia scandal", "BBC"),
    ("16:15", "TECH", "Treasury\u2019s Bessent presses Nvidia for answers on its chip sales to China", "REUTERS"),
    ("16:50", "TECH", "CrowdStrike to buy Zscaler in a $44bn all-stock cybersecurity deal", "AP"),
    ("17:25", "US", "FBI investigates apparent hack of its national crime database, the NCIC", "AP"),
    ("17:55", "US", "Trump halts Army plan to detonate bomb-making chemicals in Iowa", "AP"),
    ("18:20", "POLITICS", "California Rep. Jimmy Gomez resigns after ethics probe finds misconduct", "NPR"),
    ("18:45", "WORLD", "WHO chief visits Cuba as the island\u2019s healthcare system breaks down", "AP"),
    ("19:10", "WORLD", "Thai appeal court halves jail term of lawmaker convicted of royal insult", "REUTERS"),
    ("19:35", "WAR", "Israeli forces hit a truck in Gaza; three people killed, Gaza health ministry says", "REUTERS"),
    ("20:00", "WAR", "Israel PM-elect Eisenkot calls settler arson attacks \u201cJewish terrorism\u201d", "REUTERS"),
    ("20:25", "US", "ICE detains father and daughter at Sea-Tac airport en route to a baptism, lawyer says", "SEATTLE TIMES"),
    ("20:50", "US", "Chinese neuroscientist at Princeton held by ICE after detention at Washington airport", "AP"),
    ("21:15", "CULTURE", "Miley Cyrus weds drummer Maxx Morando in intimate California ceremony", "AP"),
    ("21:40", "CULTURE", "Don Toliver concert in Manchester evacuated after unknown substance released", "AP"),
    ("22:05", "CULTURE", "Grand Theft Auto VI launch surpasses expectations, publisher says", "REUTERS"),
    ("22:30", "CULTURE", "Elizabeth Holmes film \u201cYou Can See Everything\u201d passes $100m at the box office", "GUARDIAN"),
    ("22:55", "SPORT", "Houston leaps to No. 1 in AP Top 25 men\u2019s basketball poll", "AP"),
    ("23:10", "SPORT", "TCU fires football coach Sonny Dykes four years after title-game run", "AP"),
    ("23:25", "US", "Extreme weather: deluge soaks California, rivers flood in Florida", "AP"),
    ("23:40", "WORLD", "Indonesia president to nominate vice-presidential candidates on Monday", "REUTERS"),
    ("23:55", "CLIMATE", "More than 90 countries sign COP31 electrification pledge to 35% by 2035", "REUTERS"),
]


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fnt, width):
    if draw.textlength(text, font=fnt) <= width:
        return text
    while text and draw.textlength(text + "\u2026", font=fnt) > width:
        text = text[:-1]
    return text + "\u2026"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.rectangle([0, 76, W, 80], fill=GOLD)
    d.text((MARGIN, 12), "THE WORLD IN ONE DAY", font=F_KICKER, fill=(201, 162, 39))
    d.text((MARGIN, 30), "MONDAY 23 NOVEMBER 2026", font=F_TITLE, fill=(255, 255, 255))
    right_lines = ["50 SOURCED STORIES", "ALL TIMES UTC"]
    for j, ln in enumerate(right_lines):
        lw = d.textlength(ln, font=F_SUB)
        d.text((W - MARGIN - lw, 14 + j * 20), ln, font=F_SUB,
               fill=(203, 213, 225))

    # ---- lead stories ----
    lead_y = 96
    lead_h = 168
    gap = 12
    card_w = (W - 2 * MARGIN - 2 * gap) // 3
    for i, (tag, head, body, src) in enumerate(LEADS):
        x0 = MARGIN + i * (card_w + gap)
        x1 = x0 + card_w
        d.rounded_rectangle([x0, lead_y, x1, lead_y + lead_h], radius=8,
                            fill=CARD, outline=LINE, width=1)
        d.rounded_rectangle([x0, lead_y, x1, lead_y + 6], radius=3, fill=CAT[tag])
        d.rectangle([x0, lead_y + 3, x1, lead_y + 6], fill=CAT[tag])
        d.text((x0 + 14, lead_y + 16), tag, font=F_TAG, fill=CAT[tag])
        lines = wrap(d, head, F_LEAD_HEAD, card_w - 28)
        y = lead_y + 38
        for ln in lines[:3]:
            d.text((x0 + 14, y), ln, font=F_LEAD_HEAD, fill=INK)
            y += 20
        blines = wrap(d, body, F_LEAD_BODY, card_w - 28)
        y = lead_y + 104
        for ln in blines[:3]:
            d.text((x0 + 14, y), ln, font=F_LEAD_BODY, fill=(71, 85, 105))
            y += 15
        d.text((x0 + 14, lead_y + lead_h - 20), "SOURCE: " + src,
               font=F_LEAD_SRC, fill=MUTED)

    # ---- timeline header ----
    sec_y = lead_y + lead_h + 14
    d.text((MARGIN, sec_y), "THE DAY, HOUR BY HOUR", font=F_SEC, fill=NAVY)
    d.text((W - MARGIN - 210, sec_y), "EACH LINE: ONE STORY, ONE SOURCE",
           font=F_TAG, fill=MUTED)
    d.line([(MARGIN, sec_y + 22), (W - MARGIN, sec_y + 22)], fill=NAVY, width=2)

    # ---- timeline rows ----
    top = sec_y + 30
    bottom = H - 26
    row_h = (bottom - top) / len(TIMELINE)
    time_x = MARGIN
    text_x = MARGIN + 52
    pill_right = W - MARGIN
    for i, (t, cat, head, src) in enumerate(TIMELINE):
        y0 = top + i * row_h
        if i % 2 == 0:
            d.rectangle([MARGIN, y0, W - MARGIN, y0 + row_h], fill=ROW_ALT)
        cy = y0 + row_h / 2
        d.ellipse([MARGIN + 44, cy - 3, MARGIN + 50, cy + 3], fill=CAT[cat])
        d.text((time_x, cy - 6), t, font=F_TIME, fill=NAVY)
        pill_w = d.textlength(src, font=F_PILL) + 14
        pill_x0 = pill_right - pill_w
        d.rounded_rectangle([pill_x0, cy - 6.5, pill_right, cy + 6.5], radius=6,
                            fill=PILL_BG)
        d.text((pill_x0 + 7, cy - 5.5), src, font=F_PILL, fill=PILL_INK)
        head_w = pill_x0 - 10 - text_x
        d.text((text_x, cy - 6), fit(d, head, F_ROW, head_w),
               font=F_ROW, fill=INK)

    # ---- footer ----
    foot = ("All events happened or were first reported on Monday 23 November 2026.  "
            "Sources: Reuters  \u2022  AP  \u2022  BBC  \u2022  The Guardian  \u2022  NPR  \u2022  "
            "Washington Post  \u2022  Seattle Times")
    d.text((MARGIN, H - 20), foot, font=F_FOOT, fill=MUTED)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
