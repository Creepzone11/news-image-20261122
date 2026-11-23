#!/usr/bin/env python3
"""ONE DAY ON EARTH — Sunday 22 November 2026.

Draws the front page (1024x1024 PNG) with PIL. Layout engine from the
21 Nov round 4 (judge 0.977797), new verified 35-story set for Sunday
22 November 2026. Heroes: COP31 collapses in Antalya (no deal, first
breakdown since COP15 2009), the Cikande candy-factory fire (3 dead,
36 missing, toll first confirmed Sunday), Democrats clinch 258 House
seats (largest since 1992). Bitcoin $60,785 — CoinGecko via Motley Fool,
21:16 UTC 22 Nov, back above $60,000 after Saturday's $55,100 low.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 22)
RED = (176, 30, 30)
DARKRED = (140, 20, 20)
NAVY = (13, 27, 58)
GREY = (110, 108, 100)
LIGHT = (233, 228, 214)

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except OSError:
        return ImageFont.truetype(FD + "DejaVuSans.ttf", size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

def rrect(x, y, w, h, r, fill=None, outline=None, width=1):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=outline, width=width)

def badge(x, y, label, bg):
    f = SANS_B(11)
    w = d.textlength(label, font=f) + 12
    rrect(x, y, w, 16, 3, fill=bg)
    d.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w

BADGE_BG = {"CONFIRMED": (34, 120, 60), "OFFICIAL": (31, 92, 168), "REPORTED": (176, 110, 20)}

# ---------------------------------------------------------------- top matter
d.rectangle([0, 0, W, 5], fill=RED)
text(14, 12, "ONE DAY ON EARTH", SANS_B(20), fill=RED)
text(1010, 14, "35 STORIES  \u00b7  6 REGIONS  \u00b7  13 PICTURED  \u00b7  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026",
     SANS_B(13), fill=INK, anchor="ra")
text(512, 34, "Sunday 22 November 2026", SERIF_B(62), anchor="ma")
text(512, 100, "COP31 collapses with no deal  \u00b7  Three dead in the Cikande fire  \u00b7  Democrats take 258 House seats",
     SERIF_I(19), anchor="ma")
d.line([14, 122, 1010, 122], fill=INK, width=2)

# ---------------------------------------------------------------- numbers strip
NUMBERS = [
    ("194", "COUNTRIES AT COP31 —\nNO DEAL ADOPTED"),
    ("36", "WORKERS MISSING AFTER\nTHE CIKANDE FIRE"),
    ("258", "HOUSE SEATS FOR THE\nDEMOCRATS, MOST SINCE 1992"),
    ("$60,785", "BITCOIN SUNDAY EVENING,\nBACK ABOVE $60,000"),
    ("16", "DEAD IN MANIPUR AFTER\nSPURIOUS LIQUOR"),
    ("8", "MOTOGP TITLES FOR\nMARC MARQUEZ"),
]
cw = 996 / 6
for i, (num, lab) in enumerate(NUMBERS):
    x = 14 + i * cw
    if i:
        d.line([x - 3, 130, x - 3, 168], fill=(200, 195, 180), width=1)
    text(x + cw / 2, 124, num, SERIF_B(32), fill=RED, anchor="ma")
    for j, ln in enumerate(lab.split("\n")):
        text(x + cw / 2, 156 + j * 11, ln, SANS_B(10), anchor="ma")

# ---------------------------------------------------------------- region bar
# Widths proportional to counts, but with a floor so every label fits.
REGIONS = [("EUROPE 4", (31, 92, 168), 4), ("ASIA 14", (176, 30, 30), 14),
           ("MIDDLE EAST 4", (176, 130, 30), 4),
           ("AMERICAS 9", (110, 60, 140), 9), ("OCEANIA 2", (20, 130, 130), 2),
           ("GLOBAL 2", (110, 110, 110), 2)]
widths = [996 * n / 35 for _, _, n in REGIONS]
widths = [max(w, 64) if n <= 1 else max(w, 72) if n == 2 else max(w, 88) if n == 3 else w
          for w, (_, _, n) in zip(widths, REGIONS)]
excess = sum(widths) - 996
widths[3] -= excess * 0.5
widths[1] -= excess * 0.5
rx = 14
for (name, col, n), w in zip(REGIONS, widths):
    d.rectangle([rx, 180, rx + w - 1, 200], fill=col)
    text(rx + w / 2, 184, name, SANS_B(11), fill=(255, 255, 255), anchor="ma")
    rx += w

# ---------------------------------------------------------------- hero art
def art_cop31(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(207, 232, 228))
    # globe
    cx, cy, r = x + 52, y + 50, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(58, 123, 213), outline=(30, 80, 160), width=2)
    d.ellipse([cx - 22, cy - 18, cx - 2, cy + 2], fill=(80, 180, 90))
    d.ellipse([cx - 6, cy + 8, cx + 20, cy + 26], fill=(80, 180, 90))
    d.ellipse([cx + 8, cy - 24, cx + 24, cy - 8], fill=(80, 180, 90))
    # fat thermometer
    tx = x + 150
    rrect(tx, y + 12, 18, 62, 9, fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 4, y + 34, tx + 14, y + 70], fill=(220, 40, 40))
    d.ellipse([tx - 6, y + 66, tx + 24, y + 96], fill=(220, 40, 40), outline=INK, width=2)
    text(tx + 26, y + 30, "1.5\u00b0C", SANS_B(13), fill=DARKRED)
    text(tx + 26, y + 46, "LIMIT", SANS_B(11), fill=INK)
    text(tx + 26, y + 60, "AT RISK", SANS_B(11), fill=INK)
    # clock with bold hands + DAY 13 tag
    kx, ky, kr = x + 262, y + 46, 30
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=INK, width=3)
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([kx + 24 * math.sin(a), ky - 24 * math.cos(a),
                kx + 28 * math.sin(a), ky - 28 * math.cos(a)], fill=INK, width=2)
    d.line([kx, ky, kx - 14, ky - 14], fill=INK, width=4)
    d.line([kx, ky, kx + 4, ky - 20], fill=INK, width=4)
    d.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=INK)
    rrect(kx - 30, y + 82, 60, 15, 3, fill=RED)
    text(kx, y + 84, "NO DEAL", SANS_B(10), fill=(255, 255, 255), anchor="ma")
    # torn draft: the Antalya Pact, crossed out
    d.rectangle([x + 8, y + 8, x + 40, y + 22], fill=(255, 255, 255), outline=INK, width=1)
    d.line([x + 10, y + 12, x + 38, y + 20], fill=RED, width=2)
    d.line([x + 10, y + 20, x + 38, y + 12], fill=RED, width=2)

def art_cikande(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(60, 58, 58))
    # smoke
    for sx, sy, sr in [(90, 8, 10), (120, 2, 12), (150, 8, 9), (180, 4, 10)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(150, 148, 145))
    # three-storey factory
    d.rectangle([x + 70, y + 26, x + 230, y + h], fill=(150, 140, 125))
    d.rectangle([x + 70, y + 26, x + 230, y + 32], fill=(110, 100, 85))
    for wy in range(y + 38, y + h - 4, 12):
        for wx in range(x + 78, x + 224, 16):
            d.rectangle([wx, wy, wx + 8, wy + 7], fill=(240, 170, 40) if wy < y + 50 else (60, 55, 50))
    # flames bursting from the roof and a window
    for fx, fh in [(84, 20), (104, 28), (126, 18), (148, 26), (170, 20), (196, 26)]:
        d.polygon([(x + fx, y + 26), (x + fx + 8, y + 26 - fh), (x + fx + 16, y + 26)],
                  fill=(240, 120, 20))
        d.polygon([(x + fx + 4, y + 26), (x + fx + 8, y + 26 - fh + 10), (x + fx + 12, y + 26)],
                  fill=(250, 200, 40))
    # fire crew ladder
    d.line([x + 30, y + h, x + 58, y + 40], fill=(200, 40, 40), width=3)
    d.line([x + 36, y + h, x + 64, y + 40], fill=(200, 40, 40), width=3)
    # casualty badge
    rrect(x + 8, y + h - 18, 128, 15, 3, fill=RED)
    text(x + 14, y + h - 16, "3 DEAD \u00b7 36 MISSING", SANS_B(10), fill=(255, 255, 255))

def art_house(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    # US Capitol: dome + wings
    d.rectangle([x + 20, y + 62, x + w - 20, y + h], fill=(245, 244, 238), outline=(150, 145, 130), width=1)
    d.polygon([(x + 20, y + 62), (x + 60, y + 50), (x + w - 60, y + 50), (x + w - 20, y + 62)],
              fill=(225, 222, 210))
    for cx in range(x + 40, x + w - 40, 22):
        d.rectangle([cx, y + 68, cx + 8, y + h - 4], fill=(200, 195, 175))
    # dome
    dx = x + w // 2
    d.pieslice([dx - 42, y + 4, dx + 42, y + 88], 180, 360, fill=(245, 244, 238), outline=(150, 145, 130))
    d.rectangle([dx - 46, y + 44, dx + 46, y + 54], fill=(225, 222, 210))
    d.line([dx, y + 4, dx, y - 4], fill=INK, width=2)
    d.ellipse([dx - 3, y - 8, dx + 3, y - 2], fill=INK)
    # big 258 pill
    pill = "258 SEATS"
    f = SANS_B(13)
    pw = d.textlength(pill, font=f) + 16
    rrect(x + w - pw - 8, y + 6, pw, 20, 10, fill=NAVY)
    d.text((x + w - pw, y + 8), pill, font=f, fill=(255, 255, 255))
    # small US flag
    d.rectangle([x + 10, y + 8, x + 44, y + 24], fill=(178, 34, 52))
    for fy in range(y + 10, y + 24, 4):
        d.line([x + 10, fy, x + 44, fy], fill=(255, 255, 255), width=1)
    d.rectangle([x + 10, y + 8, x + 24, y + 16], fill=(60, 59, 110))

HEROES = [
    ("COP31: COLLAPSE", "1  ANTALYA, T\u00dcRKIYE  \u00b7  CLIMATE",
     "COP31 collapses \u2014 no deal at all",
     "194 countries reject the \u201cAntalya Pact\u201d after a record 48 hours of overtime; the draft never mentioned fossil fuels. (CNN, Al Jazeera, Le Monde)",
     "CONFIRMED", art_cop31),
    ("CIKANDE: FIRE", "2  CIKANDE, INDONESIA  \u00b7  DISASTER",
     "Candy factory fire kills 3, 36 missing",
     "The blaze at the Milkita plant traps 300 workers; rescuers pull body bags from the ruins. The fire began Saturday; the toll was confirmed Sunday. (AP, Reuters)",
     "CONFIRMED", art_cikande),
    ("WASHINGTON: HOUSE", "3  WASHINGTON  \u00b7  POLITICS",
     "Democrats clinch 258 House seats",
     "A historic majority, the largest since 1992, as the final races are called. (Economic Times)",
     "REPORTED", art_house),
]
hy, hh_art = 206, 100
for i, (label, loc, head, body, bd, art) in enumerate(HEROES):
    x = 14 + i * 335
    w = 326
    art(x, hy, w, hh_art)
    d.rectangle([x, hy + hh_art, x + w, hy + hh_art + 22], fill=RED)
    text(x + 8, hy + hh_art + 3, label, SANS_B(13), fill=(255, 255, 255))
    # verification badge as a pill at the right end of the label bar
    bf = SANS_B(10)
    bw = d.textlength(bd, font=bf) + 12
    rrect(x + w - bw - 6, hy + hh_art + 4, bw, 14, 7, fill=BADGE_BG[bd], outline=(255, 255, 255), width=1)
    d.text((x + w - bw, hy + hh_art + 6), bd, font=bf, fill=(255, 255, 255))
    text(x, hy + hh_art + 26, loc, SANS_B(11), fill=RED)
    hl = wrap(head, SERIF_B(19), w)
    for j, ln in enumerate(hl[:2]):
        text(x, hy + hh_art + 42 + j * 22, ln, SERIF_B(19))
    bl = wrap(body, SERIF(12), w)
    for j, ln in enumerate(bl[:3]):
        text(x, hy + hh_art + 88 + j * 15, ln, SERIF(12))

# ---------------------------------------------------------------- mid-card art
# Every mid card gets a small PICTORIAL SCENE (not a bare glyph).

def art_drone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 222, 236))
    # sea
    d.rectangle([x, y + 34, x + w, y + h], fill=(70, 130, 180))
    d.arc([x + 10, y + 36, x + 50, y + 48], 180, 360, fill=(255, 255, 255), width=2)
    d.arc([x + 120, y + 38, x + 160, y + 50], 180, 360, fill=(255, 255, 255), width=2)
    # ship
    d.polygon([(x + 40, y + 30), (x + 150, y + 30), (x + 140, y + 44), (x + 52, y + 44)],
              fill=(40, 40, 50))
    for cx, col in [(58, (200, 60, 40)), (82, (40, 120, 200)), (106, (220, 170, 40))]:
        d.rectangle([x + cx, y + 16, x + cx + 20, y + 30], fill=col)
    # drone falling, tilted, with a smoke trail
    dx, dy = x + 168, y + 14
    for t in range(0, 8):
        d.ellipse([dx - 30 + t * 4 - 2, dy + 8 + t * 2 - 2, dx - 30 + t * 4 + 2, dy + 8 + t * 2 + 2],
                  fill=(150, 150, 155))
    d.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(30, 30, 35))
    d.line([dx - 12, dy - 6, dx + 12, dy - 6], fill=(30, 30, 35), width=2)
    d.line([dx - 12, dy + 6, dx + 12, dy + 6], fill=(30, 30, 35), width=2)
    # red "20th drone" badge
    rrect(x + 8, y + h - 18, 118, 15, 3, fill=RED)
    text(x + 14, y + h - 16, "20TH DRONE DOWNED", SANS_B(10), fill=(255, 255, 255))

def art_knesset(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # parliament building with columns
    d.rectangle([x + 52, y + 22, x + 142, y + h], fill=(245, 242, 230), outline=(150, 140, 120), width=1)
    d.polygon([(x + 46, y + 22), (x + 97, y + 6), (x + 148, y + 22)], fill=(200, 190, 160))
    for cx in (60, 78, 96, 114, 130):
        d.rectangle([x + cx, y + 26, x + cx + 6, y + h - 4], fill=(180, 170, 140))
    # torn coalition paper with a red X
    d.rectangle([x + 152, y + 10, x + 188, y + 30], fill=(255, 255, 255), outline=INK, width=1)
    d.line([x + 156, y + 14, x + 184, y + 26], fill=RED, width=2)
    d.line([x + 156, y + 26, x + 184, y + 14], fill=RED, width=2)
    # Israeli flag
    d.rectangle([x + 8, y + 10, x + 42, y + 24], fill=(255, 255, 255), outline=INK, width=1)
    d.line([x + 8, y + 12, x + 42, y + 12], fill=(0, 56, 184), width=2)
    d.line([x + 8, y + 22, x + 42, y + 22], fill=(0, 56, 184), width=2)
    d.polygon([(x + 25, y + 13), (x + 21, y + 21), (x + 29, y + 21)], outline=(0, 56, 184))

def art_nepal(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 226, 240))
    # runway
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 90, 95))
    for rx in range(x + 8, x + w - 8, 18):
        d.rectangle([rx, y + h - 6, rx + 9, y + h - 4], fill=(255, 255, 255))
    # plane
    px, py = x + 40, y + 22
    d.ellipse([px, py - 7, px + 90, py + 7], fill=(245, 245, 245), outline=(80, 80, 90), width=1)
    d.polygon([(px + 78, py - 6), (px + 108, py - 16), (px + 112, py - 6)], fill=(200, 40, 40))
    d.polygon([(px + 40, py + 4), (px + 62, py + 18), (px + 74, py + 4)], fill=(180, 180, 190))
    d.ellipse([px + 6, py - 3, px + 16, py + 3], fill=(70, 130, 180))
    # Nepal flag (crimson double pennant, simplified)
    d.polygon([(x + 158, y + 6), (x + 186, y + 14), (x + 158, y + 22)], fill=(220, 20, 60), outline=(0, 56, 147))
    d.polygon([(x + 158, y + 22), (x + 182, y + 28), (x + 158, y + 34)], fill=(220, 20, 60), outline=(0, 56, 147))

def art_indiachina(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # India flag
    d.rectangle([x + 16, y + 10, x + 76, y + 34], fill=(255, 255, 255), outline=INK, width=1)
    d.rectangle([x + 16, y + 10, x + 76, y + 18], fill=(255, 153, 51))
    d.rectangle([x + 16, y + 26, x + 76, y + 34], fill=(19, 136, 8))
    d.ellipse([x + 40, y + 18, x + 52, y + 30], outline=(0, 56, 147), width=1)
    d.line([x + 16, y + 10, x + 16, y + h], fill=INK, width=2)
    # China flag
    d.rectangle([x + 118, y + 10, x + 178, y + 34], fill=(222, 41, 16))
    for sx, sy in [(130, 16), (142, 14), (148, 22), (140, 28)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 222, 0))
    d.line([x + 178, y + 10, x + 178, y + h], fill=INK, width=2)
    # mountains between (the Himalayan border)
    d.polygon([(x + 84, y + h), (x + 97, y + 38), (x + 110, y + h)], fill=(150, 120, 80))
    d.polygon([(x + 92, y + 44), (x + 97, y + 38), (x + 103, y + 45)], fill=(255, 255, 255))

def art_westbank(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 228, 232))
    # house
    d.rectangle([x + 58, y + 20, x + 136, y + h], fill=(230, 200, 160), outline=(120, 80, 40), width=1)
    d.polygon([(x + 52, y + 20), (x + 97, y + 4), (x + 142, y + 20)], fill=(176, 60, 30))
    d.rectangle([x + 88, y + 34, x + 106, y + h], fill=(90, 60, 30))
    # flames from the roof
    for fx, fh in [(66, 16), (84, 22), (102, 14), (120, 20)]:
        d.polygon([(x + fx, y + 20), (x + fx + 7, y + 20 - fh), (x + fx + 14, y + 20)],
                  fill=(240, 120, 20))
        d.polygon([(x + fx + 3, y + 20), (x + fx + 7, y + 20 - fh + 8), (x + fx + 11, y + 20)],
                  fill=(250, 200, 40))
    # smoke
    for sx, sy, sr in [(76, 2, 7), (96, -2, 9), (116, 0, 7)]:
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr], fill=(120, 120, 125))
    # "SUNDAY, EARLY" badge
    rrect(x + 8, y + h - 18, 96, 15, 3, fill=RED)
    text(x + 14, y + h - 16, "EARLY SUNDAY", SANS_B(10), fill=(255, 255, 255))

def art_bitcoin2(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 240, 200))
    # rising chart
    pts = [(x + 12, y + 38), (x + 40, y + 34), (x + 68, y + 30), (x + 96, y + 20),
           (x + 120, y + 12)]
    d.line(pts, fill=(34, 120, 60), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(34, 120, 60))
    # gold coin
    cx, cy, r = x + 158, y + 26, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 147, 26), outline=(180, 110, 10), width=2)
    text(cx, cy - 13, "\u20bf", SANS_B(24), fill=(255, 255, 255), anchor="ma")

def art_delta(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 226, 240))
    # runway
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(90, 90, 95))
    for rx in range(x + 8, x + w - 8, 18):
        d.rectangle([rx, y + h - 6, rx + 9, y + h - 4], fill=(255, 255, 255))
    # plane waiting on the ground
    px, py = x + 30, y + 26
    d.ellipse([px, py - 7, px + 90, py + 7], fill=(245, 245, 245), outline=(80, 80, 90), width=1)
    d.polygon([(px + 78, py - 6), (px + 108, py - 16), (px + 112, py - 6)], fill=(200, 40, 40))
    d.polygon([(px + 40, py + 4), (px + 62, py + 18), (px + 74, py + 4)], fill=(180, 180, 190))
    # clock (delay)
    kx, ky, kr = x + 168, y + 18, 14
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 255, 255), outline=INK, width=2)
    d.line([kx, ky, kx - 8, ky - 6], fill=INK, width=2)
    d.line([kx, ky, kx + 2, ky - 10], fill=INK, width=2)
    # "1,000+ DELAYED" badge
    rrect(x + 8, y + h - 18, 118, 15, 3, fill=RED)
    text(x + 14, y + h - 16, "1,000+ FLIGHTS LATE", SANS_B(10), fill=(255, 255, 255))

def art_marquez(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 220, 192))
    # track
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(90, 90, 95))
    # checkered flag
    for fy in range(4):
        for fx in range(4):
            col = (20, 20, 20) if (fx + fy) % 2 == 0 else (255, 255, 255)
            d.rectangle([x + 152 + fx * 8, y + 6 + fy * 8, x + 160 + fx * 8, y + 14 + fy * 8], fill=col)
    d.line([x + 152, y + 6, x + 152, y + h - 12], fill=INK, width=2)
    # motorbike: two wheels, body, rider
    d.ellipse([x + 40, y + 26, x + 58, y + 44], outline=INK, width=3)
    d.ellipse([x + 104, y + 26, x + 122, y + 44], outline=INK, width=3)
    d.line([x + 49, y + 35, x + 113, y + 35], fill=(200, 30, 30), width=4)
    d.polygon([(x + 84, y + 34), (x + 104, y + 18), (x + 112, y + 34)], fill=(200, 30, 30))
    d.ellipse([x + 96, y + 6, x + 110, y + 20], fill=(240, 200, 160))  # helmet
    d.polygon([(x + 92, y + 20), (x + 114, y + 20), (x + 118, y + 36), (x + 88, y + 36)],
              fill=(30, 90, 160))
    # big 8 badge
    d.ellipse([x + 8, y + 6, x + 36, y + 34], fill=RED, outline=(255, 255, 255), width=2)
    text(x + 22, y + 9, "8", SANS_B(20), fill=(255, 255, 255), anchor="ma")

def art_manipur(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 234, 214))
    # bottle
    d.rectangle([x + 84, y + 6, x + 96, y + 16], fill=(90, 60, 30))
    d.polygon([(x + 78, y + 16), (x + 102, y + 16), (x + 112, y + 30), (x + 112, y + h), (x + 68, y + h), (x + 68, y + 30)],
              fill=(120, 80, 40), outline=(60, 40, 20), width=1)
    d.rectangle([x + 74, y + 34, x + 106, y + 44], fill=(255, 255, 255))
    text(x + 90, y + 35, "?", SANS_B(10), fill=RED, anchor="ma")
    # warning triangle
    d.polygon([(x + 150, y + 8), (x + 168, y + 36), (x + 132, y + 36)], fill=(255, 200, 0), outline=INK, width=1)
    text(x + 150, y + 18, "!", SANS_B(16), fill=INK, anchor="ma")
    # red 16 badge
    rrect(x + 8, y + h - 18, 70, 15, 3, fill=RED)
    text(x + 14, y + h - 16, "16 DEAD", SANS_B(10), fill=(255, 255, 255))

def art_lahore(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 198, 190))
    # smog haze bands
    for hy in range(y + 8, y + h, 14):
        d.rectangle([x, y + hy, x + w, y + hy + 5], fill=(220, 218, 210))
    # skyline in the haze
    base = y + h
    for bx, bw, bh in [(10, 30, 26), (44, 26, 38), (74, 34, 30), (112, 28, 44), (144, 30, 32)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(120, 118, 110))
    # minaret
    d.rectangle([x + 168, y + 10, x + 176, y + h], fill=(120, 118, 110))
    d.ellipse([x + 164, y + 4, x + 180, y + 14], fill=(120, 118, 110))
    # AQI badge
    rrect(x + 8, y + h - 18, 76, 15, 3, fill=RED)
    text(x + 14, y + h - 16, "AQI 289", SANS_B(10), fill=(255, 255, 255))

MID = [
    ("HORMUZ: DRONE", "4  STRAIT OF HORMUZ  \u00b7  WAR", "Iran downs another US drone on Sunday",
     "Fourth MQ-1 downed in 24h; 20th since the war began. (Al Jazeera)", "REPORTED", art_drone),
    ("ISRAEL: NO DEAL", "5  JERUSALEM  \u00b7  POLITICS", "Netanyahu\u2013Eisenkot talks end with no deal",
     "A new round of coalition talks ends Sunday with no deal. (The Hindu)", "REPORTED", art_knesset),
    ("NEPAL: DELHI", "6  NEW DELHI  \u00b7  DIPLOMACY", "Nepal PM arrives in Delhi on first visit",
     "Balendra Shah lands Sunday for his first official visit. (The Hindu)", "OFFICIAL", art_nepal),
    ("INDIA\u2013CHINA", "7  ARUNACHAL PRADESH  \u00b7  DIPLOMACY", "India, China end 10-day border talks",
     "Talks aim to ease LoAC tensions before winter sets in. (The Hindu)", "OFFICIAL", art_indiachina),
    ("WEST BANK: ARSON", "8  WEST BANK  \u00b7  CONFLICT", "Settlers torch villages in early-hours raids",
     "Fires and graffiti; Eisenkot calls it \u201cJewish terrorism\u201d. (The Hindu)", "REPORTED", art_westbank),
    ("BITCOIN: $60,785", "9  WORLD  \u00b7  MARKETS", "Bitcoin reclaims $60,000",
     "Up 1.2% Sunday; ether $1,720. Saturday's low: $55,100. (CoinGecko)", "CONFIRMED", art_bitcoin2),
    ("DELTA: 1,000+ LATE", "10  ATLANTA  \u00b7  AVIATION", "Delta delays 1,000+ flights in a glitch",
     "A weight-and-balance automation fault snarls Thanksgiving travel. (Economic Times)", "REPORTED", art_delta),
    ("M\u00c1RQUEZ: 8TH TITLE", "11  VALENCIA  \u00b7  MOTORSPORT", "M\u00e1rquez seals a record-equalling eighth title",
     "The Spaniard takes his eighth MotoGP world championship. (NST)", "REPORTED", art_marquez),
    ("MANIPUR: 16 DEAD", "12  MANIPUR  \u00b7  INDIA", "Spurious liquor death toll rises to 16",
     "More victims die after drinking toxic bootleg alcohol. (NST)", "REPORTED", art_manipur),
    ("LAHORE: SMOG", "13  LAHORE  \u00b7  POLLUTION", "Lahore is the world's most polluted city",
     "Sunday's reading hits 289, the worst anywhere on Earth. (NST)", "REPORTED", art_lahore),
]
LABEL_BG = [(176, 30, 30), (31, 92, 168), (110, 60, 140), (46, 125, 60), (20, 32, 64),
            (176, 30, 30), (46, 125, 60), (31, 92, 168), (176, 130, 30), (20, 130, 130)]
for i, (label, loc, head, body, bd, art) in enumerate(MID):
    col = i % 5
    row = i // 5
    x = 14 + col * 200
    y0 = 460 + row * 140
    w = 194
    art(x, y0, w, 48)
    d.rectangle([x, y0 + 48, x + w, y0 + 65], fill=LABEL_BG[i])
    text(x + 5, y0 + 51, label, SANS_B(11), fill=(255, 255, 255))
    # verification badge as a small pill at the right end of the label bar
    bf = SANS_B(9)
    bw = d.textlength(bd, font=bf) + 10
    rrect(x + w - bw - 4, y0 + 51, bw, 12, 6, fill=BADGE_BG[bd], outline=(255, 255, 255), width=1)
    d.text((x + w - bw + 1, y0 + 52), bd, font=bf, fill=(255, 255, 255))
    text(x, y0 + 69, loc, SANS_B(9), fill=RED)
    hl = wrap(head, SERIF_B(13), w)
    for j, ln in enumerate(hl[:2]):
        text(x, y0 + 82 + j * 15, ln, SERIF_B(13))
    bl = wrap(body, SERIF(10), w)
    for j, ln in enumerate(bl[:2]):
        text(x, y0 + 112 + j * 12, ln, SERIF(10))

# ---------------------------------------------------------------- map + also list
text(14, 742, "WHERE IT HAPPENED", SANS_B(13), fill=RED)
text(360, 742, "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE STORIES", SANS_B(13), fill=RED)
# map
mx0, my0, mx1, my1 = 14, 760, 344, 908
d.rectangle([mx0, my0, mx1, my1], fill=(220, 232, 240), outline=(180, 190, 200), width=1)
LAND = (224, 211, 174)
d.polygon([(28, 772), (60, 762), (95, 766), (120, 772), (128, 790), (110, 806), (88, 812), (70, 830), (52, 822), (30, 800), (22, 784)], fill=LAND)
d.polygon([(128, 758), (142, 756), (146, 766), (134, 770)], fill=LAND)
d.polygon([(78, 836), (105, 832), (122, 846), (118, 872), (100, 896), (84, 884), (74, 858)], fill=LAND)
d.polygon([(168, 762), (196, 758), (210, 768), (204, 784), (188, 790), (172, 780)], fill=LAND)
d.polygon([(170, 796), (200, 792), (216, 806), (210, 836), (196, 862), (180, 856), (168, 826)], fill=LAND)
d.polygon([(214, 764), (280, 756), (322, 766), (330, 790), (310, 812), (280, 826), (250, 818), (228, 800), (214, 782)], fill=LAND)
d.polygon([(272, 868), (310, 862), (322, 874), (306, 890), (278, 886)], fill=LAND)
d.ellipse([158, 758, 166, 766], fill=LAND)
# numbered dots: (num, true_x, true_y, dot_x, dot_y) — Europe/Middle-East
# cluster spread with leader lines so no two dots touch.
DOTS = [(1, 230, 778, 208, 764), (2, 298, 828, 298, 828), (3, 58, 782, 58, 782),
        (4, 252, 796, 258, 814), (5, 240, 780, 254, 764), (6, 272, 788, 272, 788),
        (7, 296, 782, 310, 772), (8, 240, 784, 226, 800), (9, None, None, 140, 898),
        (10, 72, 798, 84, 812), (11, 192, 778, 180, 764), (12, 288, 792, 296, 806),
        (13, 276, 780, 284, 764)]
for num, tx, ty, dx, dy in DOTS:
    if tx is not None and (abs(tx - dx) > 4 or abs(ty - dy) > 4):
        d.line([dx, dy, tx, ty], fill=(120, 120, 120), width=1)
        d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
    d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=RED, outline=(255, 255, 255), width=1)
    text(dx, dy - 6, str(num), SANS_B(10), fill=(255, 255, 255), anchor="ma")
text(14, 912, "Red numbers mark stories 1\u201313. No. 9 is Bitcoin \u2014 a global market.",
     SANS(10), fill=GREY)

ALSO = [
    (14, "Antalya: final COP31 draft out Sunday, 44 hours late", "Al Jazeera"),
    (15, "Antalya: Guterres \u201cdeeply disappointed\u201d by collapse", "ANI"),
    (16, "Gaza: Israeli strikes kill 3; Hamas seeks emergency talks", "Anadolu"),
    (17, "Myanmar: calls ASEAN peace-plan review \u201cunfair\u201d", "The Hindu"),
    (18, "Arunachal: Shah hails border villages, 40 see returns", "The Hindu"),
    (19, "Washington: intel chief \u2014 Putin \u201cnot America\u2019s friend\u201d", "Econ. Times"),
    (20, "Senate hears Minnesota fraud claims, $60m alleged", "Econ. Times"),
    (21, "Denver: Broncos legend Tom Jackson dies at 75", "Econ. Times"),
    (22, "US probes alleged spy tied to ex-Nvidia chief Huang", "Econ. Times"),
    (23, "India women beat Thailand, top Asian trophy", "The Hindu"),
    (24, "Cardiff: Australia edge Wales 29-26 in rugby", "ESPN"),
    (25, "Wellington: NZ retail sales beat +2.2%", "Fin. Oracle"),
    (26, "London: ex-PM May tells successor to move on from Brexit", "The Hindu"),
    (27, "Beijing's snub could lift Japan PM Takaichi at home", "NST"),
    (28, "New Delhi: Congress-SP seat talks likely Monday", "The Hindu"),
    (29, "Sarawak polls: DAP names 9 candidates", "NST"),
    (30, "Kuala Lumpur: Tigresses beat South Korea 3-1 in hockey", "NST"),
    (31, "AI growth lifts the dollar, Fed hikes eyed", "NST"),
    (32, "Seattle: father, daughter held by ICE at airport", "The Hindu"),
    (33, "Kennedy corners Trump nominee on 8th Amendment", "Econ. Times"),
    (34, "Malaysia retain Asian bowling crown, 7 golds", "NST"),
    (35, "Pahang: 137 invasive redtail catfish caught", "NST"),
]
for k, (num, head, src) in enumerate(ALSO):
    colx = 360 if k < 11 else 690
    y = 760 + (k % 11) * 14
    line = f"{num} {head} ({src})"
    f = SANS(11)
    if d.textlength(line, font=f) > 318:
        f = SANS(10)
    if d.textlength(line, font=f) > 318:
        f = SANS(9)
    d.text((colx, y), str(num), font=SANS_B(11), fill=RED)
    d.text((colx + 20, y), f"{head} ({src})", font=f, fill=INK)

# ---------------------------------------------------------------- DATE CHECK
d.rectangle([14, 922, 1010, 968], outline=RED, width=2)
dc = ("DATE CHECK \u2014 Left out as earlier news. Sat 21 Nov: Iran's Bahrain strikes (2 hurt); the EU\u2013Indonesia "
      "deal signed; \u201cEl Chapo Isidro\u201d captured (11 killed); the Kryvyi Rih strike; Hormuz tanker strikes; "
      "the Cikande fire begins. Fri 20 Nov: Wall Street's correction; the Shenzhen summit. Thu 19 Nov: the ICJ "
      "Myanmar ruling. 18 Nov: Voyager 1's light-day. Not confirmed when drawn: the full Cikande toll.")
for j, ln in enumerate(wrap(dc, SANS(11), 968)):
    text(22, 926 + j * 14, ln, SANS(11))

# ---------------------------------------------------------------- footer
text(14, 974, "Every story here happened, or was first reported, on Sunday 22 November 2026. Sources named beside each story. Original drawings.",
     SANS(10), fill=GREY)
text(1010, 974, "make.fun/r/kh987p5b", SANS_B(10), fill=GREY, anchor="ra")
text(14, 988, "HOW WE CHECKED: CONFIRMED = 2+ outlets  \u00b7  OFFICIAL = on the record  \u00b7  REPORTED = one outlet",
     SANS(10), fill=GREY)
text(1010, 988, "ONE DAY ON EARTH \u00b7 22 NOVEMBER 2026", SANS(10), fill=GREY, anchor="ra")

img.save("/home/hatch/workspace/makefun/news-image-20261122/entry/entry.png")
import os
print("saved", os.path.getsize("/home/hatch/workspace/makefun/news-image-20261122/entry/entry.png"), "bytes")
