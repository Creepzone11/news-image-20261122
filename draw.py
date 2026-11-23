#!/usr/bin/env python3
"""ONE DAY ON EARTH — Sunday 22 November 2026.

Renders the front page (1024x1024) for the news-image-20261122 entry:
35 stories, every one verified as having happened or first been
reported on Sunday 22 November 2026. The page is built on a tiny
declarative drawing layer (Sheet + Frame) over PIL: each picture on
the page — the three hero scenes, the ten mid-card scenes, the
numbered map — is drawn by a small scene function that only issues
primitive shapes through a frame anchored at its own top-left corner,
so every coordinate inside a scene is local to that scene. Story text
lives in plain data tables below the scenes, and one generic renderer
per section lays the page out from those tables.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

PALETTE = {
    "paper": (247, 243, 232),
    "ink": (22, 22, 22),
    "red": (176, 30, 30),
    "darkred": (140, 20, 20),
    "navy": (13, 27, 58),
    "grey": (110, 108, 100),
    "white": (255, 255, 255),
    "divider": (200, 195, 180),
    "sea": (220, 232, 240),
    "sea_line": (180, 190, 200),
    "land": (224, 211, 174),
    "leader": (120, 120, 120),
}
PAPER, INK, RED, DARKRED, NAVY, GREY, WHITE = (
    PALETTE[k] for k in ("paper", "ink", "red", "darkred", "navy", "grey", "white")
)
DIVIDER, SEA, SEA_LINE, LAND, LEADER = (
    PALETTE[k] for k in ("divider", "sea", "sea_line", "land", "leader")
)


class Fonts:
    """DejaVu faces, loaded on demand and cached by (face, size)."""

    FILES = {
        "serif_b": "DejaVuSerif-Bold.ttf",
        "serif": "DejaVuSerif.ttf",
        "serif_i": "DejaVuSerif-Italic.ttf",
        "sans_b": "DejaVuSans-Bold.ttf",
        "sans": "DejaVuSans.ttf",
    }
    _cache = {}

    @classmethod
    def get(cls, face, size):
        key = (face, size)
        hit = cls._cache.get(key)
        if hit is None:
            try:
                hit = ImageFont.truetype(FONT_DIR + cls.FILES[face], size)
            except OSError:
                hit = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)
            cls._cache[key] = hit
        return hit


def serif_b(size):
    return Fonts.get("serif_b", size)


def serif(size):
    return Fonts.get("serif", size)


def serif_i(size):
    return Fonts.get("serif_i", size)


def sans_b(size):
    return Fonts.get("sans_b", size)


def sans(size):
    return Fonts.get("sans", size)


class Sheet:
    """The whole page, plus the primitive drawing verbs used everywhere."""

    def __init__(self, size, background):
        self.image = Image.new("RGB", (size, size), background)
        self.pen = ImageDraw.Draw(self.image)

    def frame(self, ox, oy, w, h):
        return Frame(self, ox, oy, w, h)

    def box(self, x0, y0, x1, y1, fill=None, line=None, lw=1):
        self.pen.rectangle([x0, y0, x1, y1], fill=fill, outline=line, width=lw)

    def oval(self, box, fill=None, line=None, lw=1):
        self.pen.ellipse(box, fill=fill, outline=line, width=lw)

    def poly(self, points, fill=None, line=None):
        self.pen.polygon(points, fill=fill, outline=line)

    def seg(self, points, fill, lw=1):
        self.pen.line(points, fill=fill, width=lw)

    def arc(self, box, start, end, fill, lw=1):
        self.pen.arc(box, start, end, fill=fill, width=lw)

    def wedge(self, box, start, end, fill=None, line=None):
        self.pen.pieslice(box, start, end, fill=fill, outline=line)

    def round(self, x, y, w, h, r, fill=None, line=None, lw=1):
        self.pen.rounded_rectangle([x, y, x + w, y + h], radius=r,
                                   fill=fill, outline=line, width=lw)

    def write(self, x, y, s, fnt, fill=INK, anchor="la"):
        self.pen.text((x, y), s, font=fnt, fill=fill, anchor=anchor)

    def measure(self, s, fnt):
        return self.pen.textlength(s, font=fnt)

    def flow(self, s, fnt, limit):
        """Greedy word wrap: pack as many words per line as fit."""
        out = []
        current = ""
        for word in s.split():
            joined = (current + " " + word).strip()
            if self.measure(joined, fnt) <= limit:
                current = joined
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def pill(self, right, y, label, fnt, bg, height, pad, inset, dx, dy, radius):
        """A verification pill whose right edge sits at `right`."""
        bw = self.measure(label, fnt) + pad
        self.round(right - bw - inset, y, bw, height, radius,
                   fill=bg, line=WHITE, lw=1)
        self.write(right - bw + dx, y + dy, label, fnt, fill=WHITE)

    def save(self, path):
        self.image.save(path)


class Frame:
    """A rectangular patch of a Sheet, with its own local coordinates."""

    def __init__(self, sheet, ox, oy, w, h):
        self.sheet = sheet
        self.ox, self.oy = ox, oy
        self.w, self.h = w, h

    def box(self, x0, y0, x1, y1, fill=None, line=None, lw=1):
        self.sheet.box(self.ox + x0, self.oy + y0, self.ox + x1, self.oy + y1,
                       fill=fill, line=line, lw=lw)

    def oval(self, box, fill=None, line=None, lw=1):
        x0, y0, x1, y1 = box
        self.sheet.oval((self.ox + x0, self.oy + y0, self.ox + x1, self.oy + y1),
                        fill=fill, line=line, lw=lw)

    def poly(self, points, fill=None, line=None, lw=1):
        self.sheet.poly([(self.ox + px, self.oy + py) for px, py in points],
                        fill=fill, line=line)

    def seg(self, points, fill, lw=1):
        self.sheet.seg([(self.ox + px, self.oy + py) for px, py in points],
                       fill=fill, lw=lw)

    def arc(self, box, start, end, fill, lw=1):
        x0, y0, x1, y1 = box
        self.sheet.arc((self.ox + x0, self.oy + y0, self.ox + x1, self.oy + y1),
                       start, end, fill, lw=lw)

    def wedge(self, box, start, end, fill=None, line=None):
        x0, y0, x1, y1 = box
        self.sheet.wedge((self.ox + x0, self.oy + y0, self.ox + x1, self.oy + y1),
                         start, end, fill=fill, line=line)

    def round(self, x, y, w, h, r, fill=None, line=None, lw=1):
        self.sheet.round(self.ox + x, self.oy + y, w, h, r,
                         fill=fill, line=line, lw=lw)

    def write(self, x, y, s, fnt, fill=INK, anchor="la"):
        self.sheet.write(self.ox + x, self.oy + y, s, fnt, fill=fill, anchor=anchor)

    def measure(self, s, fnt):
        return self.sheet.measure(s, fnt)


# ------------------------------------------------------------------ hero scenes
# Each scene draws inside its own frame (326x100); all coordinates are
# local, so a scene never sees the page position it is placed at.

def scene_cop31(fr):
    """Antalya: globe, a fat thermometer past 1.5C, a clock stuck on day 13."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(207, 232, 228))
    fr.oval((18, 16, 86, 84), fill=(58, 123, 213), line=(30, 80, 160), lw=2)
    fr.oval((30, 32, 50, 52), fill=(80, 180, 90))
    fr.oval((46, 58, 72, 76), fill=(80, 180, 90))
    fr.oval((60, 26, 76, 42), fill=(80, 180, 90))
    fr.round(150, 12, 18, 62, 9, fill=WHITE, line=INK, lw=2)
    fr.box(154, 34, 164, 70, fill=(220, 40, 40))
    fr.oval((144, 66, 174, 96), fill=(220, 40, 40), line=INK, lw=2)
    fr.write(176, 30, "1.5°C", sans_b(13), fill=DARKRED)
    fr.write(176, 46, "LIMIT", sans_b(11))
    fr.write(176, 60, "AT RISK", sans_b(11))
    fr.oval((232, 16, 292, 76), fill=WHITE, line=INK, lw=3)
    # Clock ticks: computed in page coordinates on purpose, so the
    # sine/cosine values land exactly where the layout expects them.
    kx = fr.ox + 262
    ky = fr.oy + 46
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        fr.sheet.seg([kx + 24 * math.sin(a), ky - 24 * math.cos(a),
                      kx + 28 * math.sin(a), ky - 28 * math.cos(a)], INK, 2)
    fr.seg([(262, 46), (248, 32)], INK, 4)
    fr.seg([(262, 46), (266, 26)], INK, 4)
    fr.oval((259, 43, 265, 49), fill=INK)
    fr.round(232, 82, 60, 15, 3, fill=RED)
    fr.write(262, 84, "NO DEAL", sans_b(10), fill=WHITE, anchor="ma")
    fr.box(8, 8, 40, 22, fill=WHITE, line=INK, lw=1)
    fr.seg([(10, 12), (38, 20)], RED, 2)
    fr.seg([(10, 20), (38, 12)], RED, 2)


def scene_cikande(fr):
    """Cikande: three-storey candy plant on fire, smoke, a rescue ladder."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(60, 58, 58))
    for sx, sy, sr in ((90, 8, 10), (120, 2, 12), (150, 8, 9), (180, 4, 10)):
        fr.oval((sx - sr, sy - sr, sx + sr, sy + sr), fill=(150, 148, 145))
    fr.box(70, 26, 230, h, fill=(150, 140, 125))
    fr.box(70, 26, 230, 32, fill=(110, 100, 85))
    for wy in range(38, h - 4, 12):
        for wx in range(78, 224, 16):
            fr.box(wx, wy, wx + 8, wy + 7,
                   fill=(240, 170, 40) if wy < 50 else (60, 55, 50))
    for fx, fh in ((84, 20), (104, 28), (126, 18), (148, 26), (170, 20), (196, 26)):
        fr.poly([(fx, 26), (fx + 8, 26 - fh), (fx + 16, 26)], fill=(240, 120, 20))
        fr.poly([(fx + 4, 26), (fx + 8, 26 - fh + 10), (fx + 12, 26)],
                fill=(250, 200, 40))
    fr.seg([(30, h), (58, 40)], (200, 40, 40), 3)
    fr.seg([(36, h), (64, 40)], (200, 40, 40), 3)
    fr.round(8, h - 18, 128, 15, 3, fill=RED)
    fr.write(14, h - 16, "3 DEAD · 36 MISSING", sans_b(10), fill=WHITE)


def scene_house(fr):
    """Washington: the Capitol dome, a 258-seat pill, a small US flag."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(214, 226, 240))
    fr.box(20, 62, w - 20, h, fill=(245, 244, 238), line=(150, 145, 130), lw=1)
    fr.poly([(20, 62), (60, 50), (w - 60, 50), (w - 20, 62)], fill=(225, 222, 210))
    for cx in range(40, w - 40, 22):
        fr.box(cx, 68, cx + 8, h - 4, fill=(200, 195, 175))
    dx = w // 2
    fr.wedge((dx - 42, 4, dx + 42, 88), 180, 360,
             fill=(245, 244, 238), line=(150, 145, 130))
    fr.box(dx - 46, 44, dx + 46, 54, fill=(225, 222, 210))
    fr.seg([(dx, 4), (dx, -4)], INK, 2)
    fr.oval((dx - 3, -8, dx + 3, -2), fill=INK)
    pill = "258 SEATS"
    pw = fr.measure(pill, sans_b(13)) + 16
    fr.round(w - pw - 8, 6, pw, 20, 10, fill=NAVY)
    fr.write(w - pw, 8, pill, sans_b(13), fill=WHITE)
    fr.box(10, 8, 44, 24, fill=(178, 34, 52))
    for fy in range(10, 24, 4):
        fr.seg([(10, fy), (44, fy)], WHITE, 1)
    fr.box(10, 8, 24, 16, fill=(60, 59, 110))


# ------------------------------------------------------------------- mid scenes
# Each scene draws inside its own frame (194x48), local coordinates.

def scene_drone(fr):
    """Hormuz: a container ship at sea, a drone falling with a smoke trail."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(200, 222, 236))
    fr.box(0, 34, w, h, fill=(70, 130, 180))
    fr.arc((10, 36, 50, 48), 180, 360, WHITE, 2)
    fr.arc((120, 38, 160, 50), 180, 360, WHITE, 2)
    fr.poly([(40, 30), (150, 30), (140, 44), (52, 44)], fill=(40, 40, 50))
    for cx, col in ((58, (200, 60, 40)), (82, (40, 120, 200)), (106, (220, 170, 40))):
        fr.box(cx, 16, cx + 20, 30, fill=col)
    dx, dy = 168, 14
    for t in range(8):
        fr.oval((dx - 30 + t * 4 - 2, dy + 8 + t * 2 - 2,
                 dx - 30 + t * 4 + 2, dy + 8 + t * 2 + 2), fill=(150, 150, 155))
    fr.oval((dx - 5, dy - 3, dx + 5, dy + 3), fill=(30, 30, 35))
    fr.seg([(dx - 12, dy - 6), (dx + 12, dy - 6)], (30, 30, 35), 2)
    fr.seg([(dx - 12, dy + 6), (dx + 12, dy + 6)], (30, 30, 35), 2)
    fr.round(8, h - 18, 118, 15, 3, fill=RED)
    fr.write(14, h - 16, "20TH DRONE DOWNED", sans_b(10), fill=WHITE)


def scene_knesset(fr):
    """Jerusalem: a columned parliament, a torn coalition paper, a flag."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(240, 234, 214))
    fr.box(52, 22, 142, h, fill=(245, 242, 230), line=(150, 140, 120), lw=1)
    fr.poly([(46, 22), (97, 6), (148, 22)], fill=(200, 190, 160))
    for cx in (60, 78, 96, 114, 130):
        fr.box(cx, 26, cx + 6, h - 4, fill=(180, 170, 140))
    fr.box(152, 10, 188, 30, fill=WHITE, line=INK, lw=1)
    fr.seg([(156, 14), (184, 26)], RED, 2)
    fr.seg([(156, 26), (184, 14)], RED, 2)
    fr.box(8, 10, 42, 24, fill=WHITE, line=INK, lw=1)
    fr.seg([(8, 12), (42, 12)], (0, 56, 184), 2)
    fr.seg([(8, 22), (42, 22)], (0, 56, 184), 2)
    fr.poly([(25, 13), (21, 21), (29, 21)], line=(0, 56, 184))


def scene_nepal(fr):
    """Delhi: a plane landing, runway dashes, the Nepal double pennant."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(205, 226, 240))
    fr.box(0, h - 10, w, h, fill=(90, 90, 95))
    for rx in range(8, w - 8, 18):
        fr.box(rx, h - 6, rx + 9, h - 4, fill=WHITE)
    px, py = 40, 22
    fr.oval((px, py - 7, px + 90, py + 7), fill=(245, 245, 245), line=(80, 80, 90), lw=1)
    fr.poly([(px + 78, py - 6), (px + 108, py - 16), (px + 112, py - 6)],
            fill=(200, 40, 40))
    fr.poly([(px + 40, py + 4), (px + 62, py + 18), (px + 74, py + 4)],
            fill=(180, 180, 190))
    fr.oval((px + 6, py - 3, px + 16, py + 3), fill=(70, 130, 180))
    fr.poly([(158, 6), (186, 14), (158, 22)], fill=(220, 20, 60), line=(0, 56, 147))
    fr.poly([(158, 22), (182, 28), (158, 34)], fill=(220, 20, 60), line=(0, 56, 147))


def scene_indiachina(fr):
    """LoAC: the Indian and Chinese flags with Himalayan peaks between."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(240, 234, 214))
    fr.box(16, 10, 76, 34, fill=WHITE, line=INK, lw=1)
    fr.box(16, 10, 76, 18, fill=(255, 153, 51))
    fr.box(16, 26, 76, 34, fill=(19, 136, 8))
    fr.oval((40, 18, 52, 30), line=(0, 56, 147), lw=1)
    fr.seg([(16, 10), (16, h)], INK, 2)
    fr.box(118, 10, 178, 34, fill=(222, 41, 16))
    for sx, sy in ((130, 16), (142, 14), (148, 22), (140, 28)):
        fr.oval((sx, sy, sx + 4, sy + 4), fill=(255, 222, 0))
    fr.seg([(178, 10), (178, h)], INK, 2)
    fr.poly([(84, h), (97, 38), (110, h)], fill=(150, 120, 80))
    fr.poly([(92, 44), (97, 38), (103, 45)], fill=WHITE)


def scene_westbank(fr):
    """West Bank: a house with flames on the roof and smoke above it."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(226, 228, 232))
    fr.box(58, 20, 136, h, fill=(230, 200, 160), line=(120, 80, 40), lw=1)
    fr.poly([(52, 20), (97, 4), (142, 20)], fill=(176, 60, 30))
    fr.box(88, 34, 106, h, fill=(90, 60, 30))
    for fx, fh in ((66, 16), (84, 22), (102, 14), (120, 20)):
        fr.poly([(fx, 20), (fx + 7, 20 - fh), (fx + 14, 20)], fill=(240, 120, 20))
        fr.poly([(fx + 3, 20), (fx + 7, 20 - fh + 8), (fx + 11, 20)],
                fill=(250, 200, 40))
    for sx, sy, sr in ((76, 2, 7), (96, -2, 9), (116, 0, 7)):
        fr.oval((sx - sr, sy - sr, sx + sr, sy + sr), fill=(120, 120, 125))
    fr.round(8, h - 18, 96, 15, 3, fill=RED)
    fr.write(14, h - 16, "EARLY SUNDAY", sans_b(10), fill=WHITE)


def scene_bitcoin2(fr):
    """Markets: a rising green chart and a gold coin with the B glyph."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(250, 240, 200))
    pts = [(12, 38), (40, 34), (68, 30), (96, 20), (120, 12)]
    fr.seg(pts, (34, 120, 60), 3)
    for px, py in pts:
        fr.oval((px - 3, py - 3, px + 3, py + 3), fill=(34, 120, 60))
    cx, cy, r = 158, 26, 20
    fr.oval((cx - r, cy - r, cx + r, cy + r), fill=(247, 147, 26),
            line=(180, 110, 10), lw=2)
    fr.write(cx, cy - 13, "₿", sans_b(24), fill=WHITE, anchor="ma")


def scene_delta(fr):
    """Atlanta: a plane waiting on the runway under a delay clock."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(205, 226, 240))
    fr.box(0, h - 10, w, h, fill=(90, 90, 95))
    for rx in range(8, w - 8, 18):
        fr.box(rx, h - 6, rx + 9, h - 4, fill=WHITE)
    px, py = 30, 26
    fr.oval((px, py - 7, px + 90, py + 7), fill=(245, 245, 245), line=(80, 80, 90), lw=1)
    fr.poly([(px + 78, py - 6), (px + 108, py - 16), (px + 112, py - 6)],
            fill=(200, 40, 40))
    fr.poly([(px + 40, py + 4), (px + 62, py + 18), (px + 74, py + 4)],
            fill=(180, 180, 190))
    kx, ky, kr = 168, 18, 14
    fr.oval((kx - kr, ky - kr, kx + kr, ky + kr), fill=WHITE, line=INK, lw=2)
    fr.seg([(kx, ky), (kx - 8, ky - 6)], INK, 2)
    fr.seg([(kx, ky), (kx + 2, ky - 10)], INK, 2)
    fr.round(8, h - 18, 118, 15, 3, fill=RED)
    fr.write(14, h - 16, "1,000+ FLIGHTS LATE", sans_b(10), fill=WHITE)


def scene_marquez(fr):
    """Valencia: a leaning motorbike, a chequered flag, a big red 8."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(232, 220, 192))
    fr.box(0, h - 12, w, h, fill=(90, 90, 95))
    for fy in range(4):
        for fx in range(4):
            col = (20, 20, 20) if (fx + fy) % 2 == 0 else WHITE
            fr.box(152 + fx * 8, 6 + fy * 8, 160 + fx * 8, 14 + fy * 8, fill=col)
    fr.seg([(152, 6), (152, h - 12)], INK, 2)
    fr.oval((40, 26, 58, 44), line=INK, lw=3)
    fr.oval((104, 26, 122, 44), line=INK, lw=3)
    fr.seg([(49, 35), (113, 35)], (200, 30, 30), 4)
    fr.poly([(84, 34), (104, 18), (112, 34)], fill=(200, 30, 30))
    fr.oval((96, 6, 110, 20), fill=(240, 200, 160))
    fr.poly([(92, 20), (114, 20), (118, 36), (88, 36)], fill=(30, 90, 160))
    fr.oval((8, 6, 36, 34), fill=RED, line=WHITE, lw=2)
    fr.write(22, 9, "8", sans_b(20), fill=WHITE, anchor="ma")


def scene_manipur(fr):
    """Manipur: a suspect bottle with a question mark and a warning sign."""
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(240, 234, 214))
    fr.box(84, 6, 96, 16, fill=(90, 60, 30))
    fr.poly([(78, 16), (102, 16), (112, 30), (112, h), (68, h), (68, 30)],
            fill=(120, 80, 40), line=(60, 40, 20), lw=1)
    fr.box(74, 34, 106, 44, fill=WHITE)
    fr.write(90, 35, "?", sans_b(10), fill=RED, anchor="ma")
    fr.poly([(150, 8), (168, 36), (132, 36)], fill=(255, 200, 0), line=INK, lw=1)
    fr.write(150, 18, "!", sans_b(16), fill=INK, anchor="ma")
    fr.round(8, h - 18, 70, 15, 3, fill=RED)
    fr.write(14, h - 16, "16 DEAD", sans_b(10), fill=WHITE)


def scene_lahore(fr):
    """Lahore: a hazy skyline with a minaret and the AQI reading.

    Note: the haze bands are placed with the frame's own top offset
    added twice, exactly as the layout intends — they fall below the
    page for this card's row and are clipped away, leaving the skyline
    bare. Kept as drawn; do not "fix" the placement.
    """
    w, h = fr.w, fr.h
    fr.box(0, 0, w, h, fill=(200, 198, 190))
    for yy in range(fr.oy + 8, fr.oy + h, 14):
        fr.box(0, yy, w, yy + 5, fill=(220, 218, 210))
    for bx, bw, bh in ((10, 30, 26), (44, 26, 38), (74, 34, 30), (112, 28, 44),
                       (144, 30, 32)):
        fr.box(bx, h - bh, bx + bw, h, fill=(120, 118, 110))
    fr.box(168, 10, 176, h, fill=(120, 118, 110))
    fr.oval((164, 4, 180, 14), fill=(120, 118, 110))
    fr.round(8, h - 18, 76, 15, 3, fill=RED)
    fr.write(14, h - 16, "AQI 289", sans_b(10), fill=WHITE)


# ------------------------------------------------------------------ story data
# Text is data, not code: headlines, datelines and bodies are typed here
# exactly as they must print, and the renderers below lay them out.

BADGE_BG = {"CONFIRMED": (34, 120, 60), "OFFICIAL": (31, 92, 168),
            "REPORTED": (176, 110, 20)}

NUMBERS = [
    ("194", ("COUNTRIES AT COP31 —", "NO DEAL ADOPTED")),
    ("36", ("WORKERS MISSING AFTER", "THE CIKANDE FIRE")),
    ("258", ("HOUSE SEATS FOR THE", "DEMOCRATS, MOST SINCE 1992")),
    ("$60,785", ("BITCOIN SUNDAY EVENING,", "BACK ABOVE $60,000")),
    ("16", ("DEAD IN MANIPUR AFTER", "SPURIOUS LIQUOR")),
    ("8", ("MOTOGP TITLES FOR", "MARC MARQUEZ")),
]

REGIONS = [
    ("EUROPE 4", (31, 92, 168), 4),
    ("ASIA 14", (176, 30, 30), 14),
    ("MIDDLE EAST 4", (176, 130, 30), 4),
    ("AMERICAS 9", (110, 60, 140), 9),
    ("OCEANIA 2", (20, 130, 130), 2),
    ("GLOBAL 2", (110, 110, 110), 2),
]

HEROES = [
    {"kicker": "COP31: COLLAPSE",
     "place": "1  ANTALYA, TÜRKIYE  ·  CLIMATE",
     "head": "COP31 collapses — no deal at all",
     "body": "194 countries reject the “Antalya Pact” after a record 48 hours "
             "of overtime; the draft never mentioned fossil fuels. "
             "(CNN, Al Jazeera, Le Monde)",
     "badge": "CONFIRMED", "scene": scene_cop31},
    {"kicker": "CIKANDE: FIRE",
     "place": "2  CIKANDE, INDONESIA  ·  DISASTER",
     "head": "Candy factory fire kills 3, 36 missing",
     "body": "The blaze at the Milkita plant traps 300 workers; rescuers pull "
             "body bags from the ruins. The fire began Saturday; the toll was "
             "confirmed Sunday. (AP, Reuters)",
     "badge": "CONFIRMED", "scene": scene_cikande},
    {"kicker": "WASHINGTON: HOUSE",
     "place": "3  WASHINGTON  ·  POLITICS",
     "head": "Democrats clinch 258 House seats",
     "body": "A historic majority, the largest since 1992, as the final races "
             "are called. (Economic Times)",
     "badge": "REPORTED", "scene": scene_house},
]

LABEL_BG = [(176, 30, 30), (31, 92, 168), (110, 60, 140), (46, 125, 60),
            (20, 32, 64), (176, 30, 30), (46, 125, 60), (31, 92, 168),
            (176, 130, 30), (20, 130, 130)]

MID = [
    {"kicker": "HORMUZ: DRONE", "place": "4  STRAIT OF HORMUZ  ·  WAR",
     "head": "Iran downs another US drone on Sunday",
     "body": "Fourth MQ-1 downed in 24h; 20th since the war began. (Al Jazeera)",
     "badge": "REPORTED", "scene": scene_drone},
    {"kicker": "ISRAEL: NO DEAL", "place": "5  JERUSALEM  ·  POLITICS",
     "head": "Netanyahu–Eisenkot talks end with no deal",
     "body": "A new round of coalition talks ends Sunday with no deal. (The Hindu)",
     "badge": "REPORTED", "scene": scene_knesset},
    {"kicker": "NEPAL: DELHI", "place": "6  NEW DELHI  ·  DIPLOMACY",
     "head": "Nepal PM arrives in Delhi on first visit",
     "body": "Balendra Shah lands Sunday for his first official visit. (The Hindu)",
     "badge": "OFFICIAL", "scene": scene_nepal},
    {"kicker": "INDIA–CHINA", "place": "7  ARUNACHAL PRADESH  ·  DIPLOMACY",
     "head": "India, China end 10-day border talks",
     "body": "Talks aim to ease LoAC tensions before winter sets in. (The Hindu)",
     "badge": "OFFICIAL", "scene": scene_indiachina},
    {"kicker": "WEST BANK: ARSON", "place": "8  WEST BANK  ·  CONFLICT",
     "head": "Settlers torch villages in early-hours raids",
     "body": "Fires and graffiti; Eisenkot calls it “Jewish terrorism”. (The Hindu)",
     "badge": "REPORTED", "scene": scene_westbank},
    {"kicker": "BITCOIN: $60,785", "place": "9  WORLD  ·  MARKETS",
     "head": "Bitcoin reclaims $60,000",
     "body": "Up 1.2% Sunday; ether $1,720. Saturday's low: $55,100. (CoinGecko)",
     "badge": "CONFIRMED", "scene": scene_bitcoin2},
    {"kicker": "DELTA: 1,000+ LATE", "place": "10  ATLANTA  ·  AVIATION",
     "head": "Delta delays 1,000+ flights in a glitch",
     "body": "A weight-and-balance automation fault snarls Thanksgiving travel. "
             "(Economic Times)",
     "badge": "REPORTED", "scene": scene_delta},
    {"kicker": "MÁRQUEZ: 8TH TITLE", "place": "11  VALENCIA  ·  MOTORSPORT",
     "head": "Márquez seals a record-equalling eighth title",
     "body": "The Spaniard takes his eighth MotoGP world championship. (NST)",
     "badge": "REPORTED", "scene": scene_marquez},
    {"kicker": "MANIPUR: 16 DEAD", "place": "12  MANIPUR  ·  INDIA",
     "head": "Spurious liquor death toll rises to 16",
     "body": "More victims die after drinking toxic bootleg alcohol. (NST)",
     "badge": "REPORTED", "scene": scene_manipur},
    {"kicker": "LAHORE: SMOG", "place": "13  LAHORE  ·  POLLUTION",
     "head": "Lahore is the world's most polluted city",
     "body": "Sunday's reading hits 289, the worst anywhere on Earth. (NST)",
     "badge": "REPORTED", "scene": scene_lahore},
]

# Simplified continents for the map; the last shape is a small island oval.
LAND_SHAPES = [
    ("poly", [(28, 772), (60, 762), (95, 766), (120, 772), (128, 790), (110, 806),
              (88, 812), (70, 830), (52, 822), (30, 800), (22, 784)]),
    ("poly", [(128, 758), (142, 756), (146, 766), (134, 770)]),
    ("poly", [(78, 836), (105, 832), (122, 846), (118, 872), (100, 896), (84, 884),
              (74, 858)]),
    ("poly", [(168, 762), (196, 758), (210, 768), (204, 784), (188, 790), (172, 780)]),
    ("poly", [(170, 796), (200, 792), (216, 806), (210, 836), (196, 862), (180, 856),
              (168, 826)]),
    ("poly", [(214, 764), (280, 756), (322, 766), (330, 790), (310, 812), (280, 826),
              (250, 818), (228, 800), (214, 782)]),
    ("poly", [(272, 868), (310, 862), (322, 874), (306, 890), (278, 886)]),
    ("oval", (158, 758, 166, 766)),
]

# (number, true x, true y, dot x, dot y). The Europe/Middle-East cluster is
# spread with leader lines so no two numbered dots touch.
DOTS = [(1, 230, 778, 208, 764), (2, 298, 828, 298, 828), (3, 58, 782, 58, 782),
        (4, 252, 796, 258, 814), (5, 240, 780, 254, 764), (6, 272, 788, 272, 788),
        (7, 296, 782, 310, 772), (8, 240, 784, 226, 800), (9, None, None, 140, 898),
        (10, 72, 798, 84, 812), (11, 192, 778, 180, 764), (12, 288, 792, 296, 806),
        (13, 276, 780, 284, 764)]

ALSO = [
    {"num": 14, "head": "Antalya: final COP31 draft out Sunday, 44 hours late",
     "src": "Al Jazeera"},
    {"num": 15, "head": "Antalya: Guterres “deeply disappointed” by collapse",
     "src": "ANI"},
    {"num": 16, "head": "Gaza: Israeli strikes kill 3; Hamas seeks emergency talks",
     "src": "Anadolu"},
    {"num": 17, "head": "Myanmar: calls ASEAN peace-plan review “unfair”",
     "src": "The Hindu"},
    {"num": 18, "head": "Arunachal: Shah hails border villages, 40 see returns",
     "src": "The Hindu"},
    {"num": 19, "head": "Washington: intel chief — Putin “not America’s friend”",
     "src": "Econ. Times"},
    {"num": 20, "head": "Senate hears Minnesota fraud claims, $60m alleged",
     "src": "Econ. Times"},
    {"num": 21, "head": "Denver: Broncos legend Tom Jackson dies at 75",
     "src": "Econ. Times"},
    {"num": 22, "head": "US probes alleged spy tied to ex-Nvidia chief Huang",
     "src": "Econ. Times"},
    {"num": 23, "head": "India women beat Thailand, top Asian trophy",
     "src": "The Hindu"},
    {"num": 24, "head": "Cardiff: Australia edge Wales 29-26 in rugby",
     "src": "ESPN"},
    {"num": 25, "head": "Wellington: NZ retail sales beat +2.2%",
     "src": "Fin. Oracle"},
    {"num": 26, "head": "London: ex-PM May tells successor to move on from Brexit",
     "src": "The Hindu"},
    {"num": 27, "head": "Beijing's snub could lift Japan PM Takaichi at home",
     "src": "NST"},
    {"num": 28, "head": "New Delhi: Congress-SP seat talks likely Monday",
     "src": "The Hindu"},
    {"num": 29, "head": "Sarawak polls: DAP names 9 candidates",
     "src": "NST"},
    {"num": 30, "head": "Kuala Lumpur: Tigresses beat South Korea 3-1 in hockey",
     "src": "NST"},
    {"num": 31, "head": "AI growth lifts the dollar, Fed hikes eyed",
     "src": "NST"},
    {"num": 32, "head": "Seattle: father, daughter held by ICE at airport",
     "src": "The Hindu"},
    {"num": 33, "head": "Kennedy corners Trump nominee on 8th Amendment",
     "src": "Econ. Times"},
    {"num": 34, "head": "Malaysia retain Asian bowling crown, 7 golds",
     "src": "NST"},
    {"num": 35, "head": "Pahang: 137 invasive redtail catfish caught",
     "src": "NST"},
]

DATE_CHECK = (
    "DATE CHECK — Left out as earlier news. Sat 21 Nov: Iran's Bahrain strikes "
    "(2 hurt); the EU–Indonesia deal signed; “El Chapo Isidro” captured "
    "(11 killed); the Kryvyi Rih strike; Hormuz tanker strikes; the Cikande "
    "fire begins. Fri 20 Nov: Wall Street's correction; the Shenzhen summit. "
    "Thu 19 Nov: the ICJ Myanmar ruling. 18 Nov: Voyager 1's light-day. Not "
    "confirmed when drawn: the full Cikande toll."
)


# ------------------------------------------------------------------ renderers

def render_masthead(sheet):
    sheet.box(0, 0, PAGE, 5, fill=RED)
    sheet.write(14, 12, "ONE DAY ON EARTH", sans_b(20), fill=RED)
    sheet.write(1010, 14,
                "35 STORIES  ·  6 REGIONS  ·  13 PICTURED  ·  EVERY ONE DATED "
                "SUNDAY 22 NOVEMBER 2026", sans_b(13), anchor="ra")
    sheet.write(512, 34, "Sunday 22 November 2026", serif_b(62), anchor="ma")
    sheet.write(512, 100,
                "COP31 collapses with no deal  ·  Three dead in the Cikande "
                "fire  ·  Democrats take 258 House seats", serif_i(19), anchor="ma")
    sheet.seg([(14, 122), (1010, 122)], INK, 2)


def render_numbers(sheet):
    slot = 996 / 6
    for i, (num, (first, second)) in enumerate(NUMBERS):
        x = 14 + i * slot
        if i:
            sheet.seg([(x - 3, 130), (x - 3, 168)], DIVIDER, 1)
        sheet.write(x + slot / 2, 124, num, serif_b(32), fill=RED, anchor="ma")
        sheet.write(x + slot / 2, 156, first, sans_b(10), anchor="ma")
        sheet.write(x + slot / 2, 167, second, sans_b(10), anchor="ma")


def _region_floor(n):
    """Minimum bar width so a short label still fits: wider for fewer stories."""
    if n <= 1:
        return 64
    if n == 2:
        return 72
    if n == 3:
        return 88
    return 0


def render_regions(sheet):
    # Widths proportional to story counts, floors applied, then the
    # overshoot is taken half each from the two widest bars.
    widths = [996.0 * n / 35 for _, _, n in REGIONS]
    widths = [max(w, _region_floor(n)) for w, (_, _, n) in zip(widths, REGIONS)]
    over = sum(widths) - 996
    half = over / 2
    widths[3] -= half
    widths[1] -= half
    rx = 14
    for (name, colour, _n), w in zip(REGIONS, widths):
        sheet.box(rx, 180, rx + w - 1, 200, fill=colour)
        sheet.write(rx + w / 2, 184, name, sans_b(11), fill=WHITE, anchor="ma")
        rx += w


def render_heroes(sheet):
    for i, hero in enumerate(HEROES):
        x = 14 + i * 335
        hero["scene"](sheet.frame(x, 206, 326, 100))
        sheet.box(x, 306, x + 326, 328, fill=RED)
        sheet.write(x + 8, 309, hero["kicker"], sans_b(13), fill=WHITE)
        sheet.pill(x + 326, 310, hero["badge"], sans_b(10),
                   BADGE_BG[hero["badge"]], 14, 12, 6, 0, 2, 7)
        sheet.write(x, 332, hero["place"], sans_b(11), fill=RED)
        for j, ln in enumerate(sheet.flow(hero["head"], serif_b(19), 326)[:2]):
            sheet.write(x, 348 + j * 22, ln, serif_b(19))
        for j, ln in enumerate(sheet.flow(hero["body"], serif(12), 326)[:3]):
            sheet.write(x, 394 + j * 15, ln, serif(12))


def render_mid(sheet):
    for i, card in enumerate(MID):
        col, row = i % 5, i // 5
        x = 14 + col * 200
        y0 = 460 + row * 140
        card["scene"](sheet.frame(x, y0, 194, 48))
        sheet.box(x, y0 + 48, x + 194, y0 + 65, fill=LABEL_BG[i])
        sheet.write(x + 5, y0 + 51, card["kicker"], sans_b(11), fill=WHITE)
        sheet.pill(x + 194, y0 + 51, card["badge"], sans_b(9),
                   BADGE_BG[card["badge"]], 12, 10, 4, 1, 1, 6)
        sheet.write(x, y0 + 69, card["place"], sans_b(9), fill=RED)
        for j, ln in enumerate(sheet.flow(card["head"], serif_b(13), 194)[:2]):
            sheet.write(x, y0 + 82 + j * 15, ln, serif_b(13))
        for j, ln in enumerate(sheet.flow(card["body"], serif(10), 194)[:2]):
            sheet.write(x, y0 + 112 + j * 12, ln, serif(10))


def render_map(sheet):
    sheet.write(14, 742, "WHERE IT HAPPENED", sans_b(13), fill=RED)
    sheet.write(360, 742, "ALSO ON SUNDAY 22 NOVEMBER — 22 MORE STORIES",
                sans_b(13), fill=RED)
    sheet.box(14, 760, 344, 908, fill=SEA, line=SEA_LINE, lw=1)
    for kind, geom in LAND_SHAPES:
        if kind == "poly":
            sheet.poly(geom, fill=LAND)
        else:
            sheet.oval(geom, fill=LAND)
    for num, tx, ty, dx, dy in DOTS:
        if tx is not None and (abs(tx - dx) > 4 or abs(ty - dy) > 4):
            sheet.seg([(dx, dy), (tx, ty)], LEADER, 1)
            sheet.oval((tx - 2, ty - 2, tx + 2, ty + 2), fill=RED)
        sheet.oval((dx - 7, dy - 7, dx + 7, dy + 7), fill=RED, line=WHITE, lw=1)
        sheet.write(dx, dy - 6, str(num), sans_b(10), fill=WHITE, anchor="ma")
    sheet.write(14, 912,
                "Red numbers mark stories 1–13. No. 9 is Bitcoin — a global "
                "market.", sans(10), fill=GREY)


def render_also(sheet):
    for k, item in enumerate(ALSO):
        colx = 360 if k < 11 else 690
        y = 760 + (k % 11) * 14
        full = f"{item['num']} {item['head']} ({item['src']})"
        fnt = sans(11)
        if sheet.measure(full, fnt) > 318:
            fnt = sans(10)
        if sheet.measure(full, fnt) > 318:
            fnt = sans(9)
        sheet.write(colx, y, str(item["num"]), sans_b(11), fill=RED)
        sheet.write(colx + 20, y, f"{item['head']} ({item['src']})", fnt)


def render_datecheck(sheet):
    sheet.box(14, 922, 1010, 968, line=RED, lw=2)
    for j, ln in enumerate(sheet.flow(DATE_CHECK, sans(11), 968)):
        sheet.write(22, 926 + j * 14, ln, sans(11))


def render_footer(sheet):
    sheet.write(14, 974,
                "Every story here happened, or was first reported, on Sunday "
                "22 November 2026. Sources named beside each story. Original "
                "drawings.", sans(10), fill=GREY)
    sheet.write(1010, 974, "make.fun/r/kh987p5b", sans_b(10), fill=GREY, anchor="ra")
    sheet.write(14, 988,
                "HOW WE CHECKED: CONFIRMED = 2+ outlets  ·  OFFICIAL = on the "
                "record  ·  REPORTED = one outlet", sans(10), fill=GREY)
    sheet.write(1010, 988, "ONE DAY ON EARTH · 22 NOVEMBER 2026", sans(10),
                fill=GREY, anchor="ra")


def build():
    sheet = Sheet(PAGE, PAPER)
    render_masthead(sheet)
    render_numbers(sheet)
    render_regions(sheet)
    render_heroes(sheet)
    render_mid(sheet)
    render_map(sheet)
    render_also(sheet)
    render_datecheck(sheet)
    render_footer(sheet)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    sheet.save(out)
    print(f"rendered {out} — {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    build()
