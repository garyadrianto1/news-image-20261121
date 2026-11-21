#!/usr/bin/env python3
"""news-image-20261121: one dense front page summing up Saturday 21 Nov 2026.

Draws the whole 1024x1024 page with Pillow only. No network, no clock,
no unseeded randomness: two runs write byte-identical PNGs.
Run:  python3 main.py   -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (247, 243, 232)
INK = (20, 20, 20)
SOFT = (74, 74, 66)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
TEAL = (14, 110, 110)
GOLD = (176, 124, 22)
SKY = (178, 208, 224)
RULE = (150, 140, 120)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=0, max_lines=None):
    """Draw a wrapped paragraph; return the y just below the last line."""
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = fnt.size + leading
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, fill=RULE, width=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def tagline(draw, x, y, text, fill=RED):
    draw.text((x, y), text, font=font(SANS_B, 10), fill=fill)
    return y + 14


def sky_scene(d, x, y, w, h, base, sun_xy=None, sun_c=(240, 190, 60)):
    d.rectangle([x, y, x + w, y + h], fill=base)
    if sun_xy:
        sx, sy = x + sun_xy[0], y + sun_xy[1]
        d.ellipse([sx - 16, sy - 16, sx + 16, sy + 16], fill=sun_c,
                  outline=(200, 140, 20), width=2)
    for cx, cy, r in [(18, 16, 7), (44, 10, 5), (w - 30, 20, 6)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r],
                  fill=(255, 255, 255))


def building_row(d, x, y, w, h, tops, fill):
    n = len(tops)
    bw = w // n
    for i, t in enumerate(tops):
        bx = x + i * bw + 2
        d.rectangle([bx, y + t, bx + bw - 4, y + h], fill=fill)
        d.rectangle([bx + 3, y + t + 6, bx + bw - 7, y + t + 10],
                    fill=(255, 230, 120))


def burst(d, cx, cy, r, fill):
    for k in range(8):
        ang = k * 3.14159 / 4
        ex, ey = cx + r * 0.9 * (1 if k % 2 == 0 else 0.6) * (1 if k < 4 else -1), cy
        d.line([(cx, cy), (cx + (r if k % 2 == 0 else r * 0.6) * _cos(k),
                 cy + (r if k % 2 == 0 else r * 0.6) * _sin(k))],
               fill=fill, width=3)


def _cos(k):
    import math
    return math.cos(k * math.pi / 4)


def _sin(k):
    import math
    return math.sin(k * math.pi / 4)


# ---------------------------------------------------------------- scenes
def scene_cop(d, x, y, w, h):
    sky_scene(d, x, y, w, h, (168, 196, 214), sun_xy=(w - 40, 26))
    d.rectangle([x, y + h - 46, x + w, y + h], fill=(96, 122, 84))
    building_row(d, x + 8, y + h - 96, w - 16, 50, [8, 0, 14, 4, 10],
                 (52, 68, 96))
    d.rectangle([x + w // 2 - 52, y + h - 100, x + w // 2 + 52, y + h - 46],
                fill=(226, 214, 180), outline=INK, width=2)
    d.polygon([(x + w // 2 - 60, y + h - 100), (x + w // 2 + 60, y + h - 100),
               (x + w // 2, y + h - 112)], fill=RED)
    d.text((x + w // 2 - 26, y + h - 90), "COP31", font=font(SANS_B, 15),
           fill=RED)
    d.text((x + w // 2 - 34, y + h - 70), "ANTALYA", font=font(SANS_B, 12),
           fill=INK)
    for fx in (x + 16, x + w - 46):
        d.rectangle([fx, y + h - 40, fx + 30, y + h - 8], fill=BLUE)
        d.rectangle([fx + 4, y + h - 36, fx + 26, y + h - 12], fill=(255, 255, 255))


def scene_riyadh(d, x, y, w, h):
    sky_scene(d, x, y, w, h, (24, 32, 58))
    for sx in range(12, w, 34):
        d.ellipse([x + sx, y + 10 + (sx % 23), x + sx + 2, y + 12 + (sx % 23)],
                  fill=(255, 255, 255))
    building_row(d, x + 6, y + h - 84, w - 12, 40, [6, 18, 0, 22, 10, 16],
                 (58, 66, 92))
    d.rectangle([x + w // 2 - 14, y + 8, x + w // 2 + 14, y + h - 44],
                fill=(120, 130, 150), outline=(200, 200, 200), width=1)
    d.polygon([(x + w // 2 - 14, y + 8), (x + w // 2 + 14, y + 8),
               (x + w // 2, y + 2)], fill=(150, 160, 180))
    for mx, my in [(w // 4, 34), (w // 2 + 40, 52), (w - 60, 26)]:
        d.line([(x + mx, y + my + 26), (x + mx + 16, y + my)],
               fill=(255, 200, 60), width=3)
        burst(d, x + mx + 18, y + my - 2, 9, (255, 220, 90))
        d.ellipse([x + mx + 14, y + my - 6, x + mx + 22, y + my + 2],
                  fill=(255, 240, 160))
    d.rectangle([x, y + h - 44, x + w, y + h], fill=(40, 44, 60))


def scene_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 30))
    for sx, sy, r in [(20, 18, 2), (70, 40, 1), (120, 14, 2), (w - 24, 60, 2),
                      (w - 70, 22, 1), (40, 70, 1), (w - 110, 44, 2)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(255, 255, 255))
    mx, my = x + w - 78, y + h // 2 + 6
    d.ellipse([mx - 52, my - 52, mx + 52, my + 52], fill=(196, 160, 120),
              outline=(140, 100, 60), width=2)
    for cx, cy, r in [(mx - 22, my - 14, 7), (mx + 12, my + 18, 9),
                      (mx + 26, my - 24, 5), (mx - 4, my + 30, 4)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 110, 70))
    d.rectangle([x + 26, my - 34, x + 66, my - 18], fill=(210, 210, 220),
                outline=INK, width=1)
    d.rectangle([x + 66, my - 30, x + 86, my - 22], fill=(150, 160, 180))
    d.polygon([(x + 26, my - 18), (x + 14, my - 8), (x + 26, my - 8)],
              fill=(255, 170, 40))
    d.polygon([(x + 26, my - 18), (x + 18, my - 2), (x + 26, my - 6)],
              fill=(255, 220, 90))
    d.text((x + 84, y + 8), "8 YEARS  ·  150M KM", font=font(SANS_B, 11),
           fill=(255, 220, 90))


def scene_strike(d, x, y, w, h):
    sky_scene(d, x, y, w, h, (210, 150, 110), sun_xy=(w - 26, 18))
    building_row(d, x + 4, y + h - 40, w - 8, 22, [4, 0, 8, 2], (70, 60, 60))
    burst(d, x + w // 2, y + h // 2, 16, RED)
    d.ellipse([x + w // 2 - 9, y + h // 2 - 9, x + w // 2 + 9, y + h // 2 + 9],
              fill=(255, 180, 40))
    d.line([(x + 8, y + h - 12), (x + w - 8, y + h - 4)], fill=INK, width=2)


def scene_nato(d, x, y, w, h):
    sky_scene(d, x, y, w, h, (190, 205, 225), sun_xy=(w - 30, 16))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(110, 130, 110))
    for i, col in enumerate([BLUE, (255, 255, 255), RED]):
        fx = x + 14 + i * (w // 3)
        d.rectangle([fx, y + 12, fx + w // 3 - 10, y + h - 34], fill=col,
                    outline=INK, width=1)
    d.ellipse([x + w // 2 - 12, y + 8, x + w // 2 + 12, y + 32],
              fill=GOLD, outline=INK, width=1)
    d.text((x + w // 2 - 5, y + 12), "N", font=font(SANS_B, 14), fill=INK)


def scene_plot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 208, 190))
    d.rectangle([x + 10, y + 10, x + w - 10, y + h - 22], fill=(255, 255, 255),
                outline=INK, width=1)
    d.line([(x + 14, y + 20), (x + w - 14, y + 20)], fill=INK, width=1)
    d.line([(x + 14, y + 30), (x + w - 30, y + 30)], fill=SOFT, width=1)
    d.line([(x + 14, y + 38), (x + w - 44, y + 38)], fill=SOFT, width=1)
    d.ellipse([x + w - 58, y + h - 44, x + w - 18, y + h - 4],
              outline=RED, width=3)
    d.line([(x + w - 60, y + h - 8), (x + w - 72, y + h + 2)], fill=RED,
           width=3)
    d.text((x + 16, y + h - 20), "STOPPED", font=font(SANS_B, 11), fill=RED)


def scene_quake(d, x, y, w, h):
    sky_scene(d, x, y, w, h, (200, 190, 170), sun_xy=(24, 14))
    d.polygon([(x, y + h), (x + w // 3, y + 18), (x + 2 * w // 3, y + h)],
              fill=(120, 110, 100))
    d.polygon([(x + w // 3, y + h), (x + 2 * w // 3, y + 26),
               (x + w, y + h)], fill=(100, 92, 84))
    d.rectangle([x + 12, y + h - 34, x + 44, y + h - 10], fill=(150, 120, 90),
                outline=INK, width=1)
    d.rectangle([x + w - 46, y + h - 30, x + w - 12, y + h - 10],
                fill=(150, 120, 90), outline=INK, width=1)
    d.line([(x + w // 2 - 14, y + h - 8), (x + w // 2 + 6, y + h - 26),
            (x + w // 2 - 2, y + h - 40)], fill=RED, width=2)


def scene_flood(d, x, y, w, h):
    sky_scene(d, x, y, w, h, (170, 185, 205), sun_xy=(w - 28, 16))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(60, 110, 160))
    for wy in (y + h - 24, y + h - 14):
        d.line([(x + 6, wy), (x + w - 6, wy)], fill=(200, 225, 245), width=2)
    for hx in (x + 12, x + w // 2 - 8, x + w - 44):
        d.rectangle([hx, y + h - 52, hx + 32, y + h - 30], fill=(180, 140, 90),
                    outline=INK, width=1)
        d.polygon([(hx - 3, y + h - 52), (hx + 35, y + h - 52),
                   (hx + 16, y + h - 62)], fill=RED)


def scene_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 150, 80))
    d.rectangle([x + w // 2 - 16, y + 6, x + w // 2 + 16, y + h - 6],
                fill=(214, 196, 150))
    d.rectangle([x + w // 2 - 30, y + 10, x + w // 2 - 22, y + 34],
                fill=(190, 150, 90), outline=INK, width=1)
    d.ellipse([x + w - 34, y + h - 30, x + w - 20, y + h - 16], fill=RED)
    d.text((x + 8, y + h - 22), "136", font=font(SANS_B, 16), fill=(255, 255, 255))


def scene_ashes(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 160, 100))
    for sx in (x + w // 2 - 14, x + w // 2, x + w // 2 + 14):
        d.rectangle([sx, y + 12, sx + 5, y + 40], fill=(240, 220, 150),
                    outline=INK, width=1)
    d.ellipse([x + w - 30, y + h - 26, x + w - 16, y + h - 12], fill=RED)
    d.line([(x + 10, y + h - 10), (x + w - 40, y + h - 20)], fill=INK, width=2)
    d.text((x + 8, y + h - 24), "7/58", font=font(SANS_B, 15),
           fill=(255, 255, 255))


def scene_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 44, 58))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(60, 60, 66))
    d.line([(x + 8, y + h - 22), (x + w - 8, y + h - 22)], fill=(255, 255, 255),
           width=2)
    d.rounded_rectangle([x + w // 2 - 52, y + h // 2 - 8, x + w // 2 + 52,
                         y + h // 2 + 10], radius=8, fill=RED, outline=INK)
    d.ellipse([x + w // 2 - 40, y + h // 2 + 8, x + w // 2 - 24,
               y + h // 2 + 24], fill=INK)
    d.ellipse([x + w // 2 + 24, y + h // 2 + 8, x + w // 2 + 40,
               y + h // 2 + 24], fill=INK)
    d.text((x + w // 2 - 30, y + 6), "1:33.893", font=font(SANS_B, 13),
           fill=(255, 220, 90))


def scene_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(70, 110, 170))
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], fill=(60, 140, 90),
                outline=(255, 255, 255), width=2)
    d.line([(x + w // 2, y + 8), (x + w // 2, y + h - 8)],
           fill=(255, 255, 255), width=2)
    d.ellipse([x + w // 2 - 13, y + h // 2 - 13, x + w // 2 + 13,
               y + h // 2 + 13], fill=(200, 230, 60), outline=INK, width=1)
    d.arc([x + w // 2 - 13, y + h // 2 - 13, x + w // 2 + 13,
           y + h // 2 + 13], 300, 60, fill=INK, width=2)


def scene_gaza(d, x, y, w, h):
    sky_scene(d, x, y, w, h, (220, 200, 160), sun_xy=(w - 28, 16))
    building_row(d, x + 6, y + h - 34, w - 12, 18, [4, 0, 6], (140, 125, 105))
    d.ellipse([x + w // 2 - 18, y + 12, x + w // 2 + 18, y + 40],
              fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(x + w // 2 - 18, y + 26), (x + w // 2 - 34, y + 18),
               (x + w // 2 - 18, y + 32)], fill=(255, 255, 255),
              outline=INK)
    d.ellipse([x + w // 2 - 4, y + 20, x + w // 2 + 1, y + 25], fill=INK)


# ---------------------------------------------------------------- data
LEADS = [
    ("ANTALYA · CLIMATE", "COP31 runs into overtime with no deal",
     "Talks meant to end on Friday drag into Saturday as the draft drops "
     "all mention of fossil fuels. A third text is due in the morning. (AP)",
     scene_cop),
    ("RIYADH · MIDDLE EAST", "Three Houthi missiles downed over Riyadh",
     "Air defences intercept the salvo early on Saturday, the third night "
     "of alerts in the capital. A drone aimed south is also destroyed. "
     "(Reuters)", scene_riyadh),
    ("MERCURY · SPACE", "BepiColombo reaches Mercury after 8 years",
     "The ESA-JAXA probe fires its thrusters for 37 minutes from 18:24 UTC "
     "to slip into orbit - only the second craft ever to do so. "
     "(ESA / Sky & Telescope)", scene_mercury),
]

MEDIUMS = [
    ("KRYVYI RIH · UKRAINE", "Double-tap strike kills a boy of 7",
     "A 20-year-old paramedic is also killed; 58 hurt as drones hit "
     "rescuers. (Kyiv Independent)", scene_strike),
    ("WARSAW · NATO", "Rutte flies to Warsaw after Poland breach",
     "Two missiles and a drone landed in Poland on Friday; Tusk calls it "
     "a provocation. (BBC)", scene_nato),
    ("COPENHAGEN · EUROPE", "Denmark urges EU curbs after foiled plot",
     "Police say a Russian-plot killing was stopped; Denmark wants "
     "tourist visas halted. (Reuters)", scene_plot),
    ("JUNIN · PERU", "M6.7 quake shakes the Andes; no deaths",
     "The tremor is felt in Lima; a M5.0 aftershock follows at 05:12 UTC. "
     "(USGS)", scene_quake),
    ("FLORIDA · USA", "St Johns River holds at record 18.8 ft",
     "The 1953 mark is beaten; 120 people rescued in Brevard County. "
     "(NWS)", scene_flood),
    ("WELLINGTON · CRICKET", "Rahul 136 puts India 118 ahead",
     "Gill falls for 98 in the last over; India close day three on 486/4. "
     "(Reuters)", scene_cricket),
    ("PERTH · ASHES", "Starc 7/58 wrecks England for 172",
     "Nineteen wickets fall on day one; Stokes replies with 5/23. (AAP)",
     scene_ashes),
    ("LAS VEGAS · F1", "Antonelli fastest, Verstappen gets pole",
     "A five-place grid penalty drops the champion to sixth for the race. "
     "(FIA)", scene_f1),
    ("TURIN · TENNIS", "ATP Finals semis set for Saturday",
     "Alcaraz meets Shelton; Zverev faces Medvedev for a final place. "
     "(ATP)", scene_tennis),
    ("GAZA · MIDDLE EAST", "Nine killed in Gaza as truce frays",
     "Hamas says Israeli fire keeps violating the ceasefire. "
     "(Gaza health ministry)", scene_gaza),
]

ALSO = [
    "UKRAINE: 148 drones and 3 missiles fired in one night (Air Force)",
    "POLAND asks NATO for more eastern-flank support (BBC)",
    "EU budget draft \u201cdeeply disappointing\u201d, says France (Reuters)",
    "US-IRAN talks stall; Tehran wants a dignified deal (China Daily)",
    "Tanker attacks continue in the Strait of Hormuz",
    "HAITI: Salvadoran troops battle gangs, lose soldiers",
    "PARIS: \u201cAct VI\u201d march sets off from R\u00e9publique at 14:00",
    "COP31: 100 groups warn of \u201cone of the most disappointing COPs\u201d",
    "COP31: the US does not take part directly (AP)",
    "COP31: next summit in Addis Ababa, Nov 2027",
    "RIYADH: PIF tower damaged on Thursday; third night of alerts",
    "BEPICOLOMBO: 16 burns run to March 2027; science starts April",
    "INDIA: Padikkal 80; Pant 55* at stumps in Wellington",
    "ASHES: Australia 123/9 at stumps, trailing by 49",
    "F1: Russell joins Verstappen on the front row",
    "ATP: Alcaraz 3-0 in group; Shelton 2-1",
    "Melania Trump: Ukraine truce \u201cmay come before Christmas\u201d",
    "DENMARK expels Russia\u2019s defence attach\u00e9 (Reuters)",
    "EU: 22nd sanctions package against Russia due shortly",
    "FLORIDA: emergency now covers 21 counties; rain easing",
    "PERU: quake felt in Lima; no major damage reported",
]

DATECHECK = [
    ("S&P 500 enters correction", "Fri 20 Nov close"),
    ("Cyclone Akvan lands in Odisha", "Fri 20 Nov; 372,000 moved, no deaths"),
    ("Missiles + drone land in Poland", "Fri 20 Nov"),
    ("ICJ: Myanmar guilty of Rohingya genocide", "Thu 19 Nov"),
    ("US clears ~900,000 AI chips for China", "Disclosed Thu 19 Nov"),
    ("Coalition strikes Hodeidah", "Fri 20 Nov"),
]

STATS = [
    ("3", "missiles downed over Riyadh"),
    ("148", "drones in one night"),
    ("19", "wickets, Ashes day one"),
    ("M6.7", "quake in Peru, no deaths"),
    ("18.8 ft", "record St Johns River"),
]

# lon, lat, label offset (dx, dy) in px from the true pin point
PINS = [
    (30.7, 36.9, 1, 20, -18), (46.7, 24.7, 2, 24, 10),
    (33.4, 47.9, 4, -2, -20), (21.0, 52.2, 5, -22, -14),
    (12.6, 55.7, 6, -24, 6), (-76.0, -11.2, 7, -8, 8),
    (-80.7, 28.4, 8, 6, 10), (174.8, -41.3, 9, 6, -14),
    (115.9, -32.0, 10, -6, 10), (-115.1, 36.2, 11, -14, -12),
    (7.7, 45.1, 12, 16, 14), (34.5, 31.5, 13, 22, -4),
]

CONTINENTS = [
    # North America (lon, lat)
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
     (-76, 62), (-65, 60), (-60, 47), (-70, 42), (-75, 35), (-81, 26),
     (-84, 30), (-90, 21), (-97, 26), (-105, 20), (-110, 23), (-117, 33),
     (-125, 40), (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    # South America
    [(-78, 7), (-72, 11), (-60, 9), (-52, 5), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-57, -38), (-65, -45), (-68, -52),
     (-73, -44), (-73, -30), (-77, -12), (-80, -4), (-79, 2)],
    # Africa
    [(-17, 15), (-10, 31), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, -1), (40, -10), (36, -18), (33, -26),
     (26, -34), (19, -35), (12, -18), (9, -1), (-8, 4), (-15, 11)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (4, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (40, 68), (44, 68),
     (40, 60), (32, 46), (28, 41), (23, 36), (19, 40), (12, 44), (8, 38),
     (3, 38), (-2, 37)],
    # Asia
    [(44, 68), (60, 69), (75, 72), (100, 76), (130, 72), (160, 70),
     (178, 66), (170, 60), (158, 52), (142, 45), (135, 35), (127, 33),
     (122, 30), (115, 22), (108, 12), (104, 8), (100, 6), (97, 16),
     (92, 22), (88, 22), (80, 13), (76, 8), (72, 20), (66, 25), (60, 25),
     (52, 28), (48, 30), (44, 39), (40, 46), (42, 54)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (132, -32), (137, -35),
     (140, -38), (146, -39), (150, -37), (153, -27), (150, -22),
     (146, -19), (142, -11), (136, -12), (132, -12), (126, -14),
     (122, -17), (114, -22)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 222, 232), outline=INK,
                width=1)

    def px(lon, lat):
        return (x + (lon + 180) / 360.0 * w,
                y + (75 - lat) / 135.0 * h)

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=(232, 224, 196), outline=(120, 110, 90))
    for lon in (-120, -60, 0, 60, 120):
        gx = x + (lon + 180) / 360.0 * w
        d.line([(gx, y), (gx, y + h)], fill=(180, 200, 215), width=1)
    for n, (lon, lat, num, ox, oy) in enumerate(PINS):
        cx, cy = px(lon, lat)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED, outline=INK,
                  width=1)
        lx, ly = cx + ox, cy + oy
        d.line([(cx, cy), (lx, ly)], fill=RED, width=1)
        d.ellipse([lx - 8, ly - 8, lx + 8, ly + 8], fill=RED, outline=(255, 255, 255),
                  width=1)
        f = font(SANS_B, 9)
        tw = d.textlength(str(num), font=f)
        d.text((lx - tw / 2, ly - 5), str(num), font=f, fill=(255, 255, 255))
    # Mercury lives off the map: say so in the corner.
    d.rectangle([x + w - 118, y + 4, x + w - 4, y + 22], fill=(20, 20, 20))
    d.text((x + w - 112, y + 8), "3  MERCURY - OFF MAP", font=font(SANS_B, 9),
           fill=(255, 220, 90))


def lead_card(d, x, y, w, num, tag, head, deck, scene):
    art_h = 118
    scene(d, x, y, w, art_h)
    d.rectangle([x, y, x + w, y + art_h], outline=INK, width=1)
    d.ellipse([x + 6, y + 6, x + 26, y + 26], fill=RED, outline=(255, 255, 255),
              width=1)
    f = font(SANS_B, 12)
    tw = d.textlength(str(num), font=f)
    d.text((x + 16 - tw / 2, y + 9), str(num), font=f, fill=(255, 255, 255))
    ty = y + art_h + 6
    ty = tagline(d, x, ty, tag)
    ty = para(d, x, ty, head, font(SERIF_B, 17), w, leading=1, max_lines=2)
    para(d, x, ty + 2, deck, font(SANS, 11), w, leading=1, max_lines=4)


def medium_card(d, x, y, w, num, tag, head, deck, scene):
    art_h = 62
    scene(d, x, y, w, art_h)
    d.rectangle([x, y, x + w, y + art_h], outline=INK, width=1)
    d.ellipse([x + 4, y + 4, x + 20, y + 20], fill=RED, outline=(255, 255, 255),
              width=1)
    f = font(SANS_B, 9)
    tw = d.textlength(str(num), font=f)
    d.text((x + 12 - tw / 2, y + 7), str(num), font=f, fill=(255, 255, 255))
    ty = y + art_h + 4
    d.text((x, ty), tag, font=font(SANS_B, 8), fill=RED)
    ty += 11
    ty = para(d, x, ty, head, font(SERIF_B, 12), w, leading=0, max_lines=2)
    para(d, x, ty + 1, deck, font(SANS, 9), w, leading=0, max_lines=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=font(SERIF_B, 42),
           fill=INK, anchor="ma")
    hline(d, 8, W - 8, 58, fill=INK, width=2)
    d.text((W // 2, 64), "34 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED",
           font=font(SANS_B, 13), fill=RED, anchor="ma")
    d.text((W // 2, 86), "Saturday 21 November 2026", font=font(SERIF_B, 40),
           fill=INK, anchor="ma")
    d.text((W // 2, 128),
           "COP31 in overtime  \u00b7  Missiles over Riyadh  \u00b7  "
           "BepiColombo reaches Mercury",
           font=font(SANS, 13), fill=SOFT, anchor="ma")

    # Stat strip
    sy, sh = 148, 30
    sw = (W - 16 - 4 * 6) // 5
    for i, (big, small) in enumerate(STATS):
        bx = 8 + i * (sw + 6)
        d.rectangle([bx, sy, bx + sw, sy + sh], fill=(255, 255, 255),
                    outline=RULE, width=1)
        d.text((bx + 6, sy + 6), big, font=font(SANS_B, 13), fill=RED)
        bw = d.textlength(big, font=font(SANS_B, 13))
        d.text((bx + 10 + bw, sy + 9), small, font=font(SANS, 10), fill=INK)

    # Three leads
    ly = 186
    lw = (W - 16 - 2 * 8) // 3
    for i, (tag, head, deck, scene) in enumerate(LEADS):
        lead_card(d, 8 + i * (lw + 8), ly, lw, i + 1, tag, head, deck, scene)

    # Medium stories
    my = 404
    d.text((8, my), "THE DAY IN PICTURES \u2014 10 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    hline(d, 8, W - 8, my + 17, fill=INK, width=1)
    mw = (W - 16 - 4 * 6) // 5
    mh = 132
    for i, (tag, head, deck, scene) in enumerate(MEDIUMS):
        row, col = divmod(i, 5)
        medium_card(d, 8 + col * (mw + 6), my + 22 + row * (mh + 6), mw,
                    i + 4, tag, head, deck, scene)

    # Bottom band: ALSO list | map | DATE CHECK
    by = 700
    hline(d, 8, W - 8, by, fill=INK, width=2)
    d.text((8, by + 6), "ALSO ON SATURDAY 21 NOVEMBER \u2014 21 MORE STORIES",
           font=font(SANS_B, 12), fill=INK)
    col_w = 244
    f_item = font(SANS, 10)
    for i, item in enumerate(ALSO):
        col, row = divmod(i, 11)
        ix = 8 + col * (col_w + 4)
        iy = by + 26 + row * 22
        d.text((ix, iy), "\u2022", font=f_item, fill=RED)
        para(d, ix + 10, iy, item, f_item, col_w - 12, leading=0, max_lines=2)

    mx = 508
    d.text((mx, by + 6), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=INK)
    draw_map(d, mx, by + 26, 288, 204)
    d.text((mx, by + 236),
           "Pins 1-13 match the drawn stories above.",
           font=font(SANS, 9), fill=SOFT)
    d.text((mx, by + 250),
           "1 Antalya  2 Riyadh  4 Kryvyi Rih  5 Warsaw",
           font=font(SANS, 9), fill=SOFT)
    d.text((mx, by + 264),
           "6 Copenhagen  7 Junin  8 Florida  9 Wellington",
           font=font(SANS, 9), fill=SOFT)
    d.text((mx, by + 278),
           "10 Perth  11 Las Vegas  12 Turin  13 Gaza",
           font=font(SANS, 9), fill=SOFT)

    dx = 808
    d.rectangle([dx, by + 6, W - 8, by + 292], fill=(255, 250, 225),
                outline=RED, width=2)
    d.text((dx + 8, by + 12), "DATE CHECK", font=font(SANS_B, 12), fill=RED)
    d.text((dx + 8, by + 28), "NOT 21 Nov \u2014 left out on purpose:",
           font=font(SANS, 9), fill=SOFT)
    cy = by + 46
    for head, when in DATECHECK:
        cy = para(d, dx + 8, cy, head, font(SANS_B, 10), 200, leading=0,
                  max_lines=2)
        cy = para(d, dx + 8, cy, when, font(SANS, 9), 200, leading=0,
                  max_lines=2)
        cy += 8

    # Footer
    fy = 994
    hline(d, 8, W - 8, fy, fill=INK, width=1)
    d.text((W // 2, fy + 5),
           "Every story here happened, or was first reported, on Saturday "
           "21 November 2026.",
           font=font(SANS, 10), fill=SOFT, anchor="ma")
    d.text((W // 2, fy + 18),
           "Sources named beside each story. Original drawings, not "
           "photographs.",
           font=font(SANS, 10), fill=SOFT, anchor="ma")

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
