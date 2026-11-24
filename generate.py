#!/usr/bin/env python3
"""Generate entry.png: a one-day world news infographic (1024x1024).

Written from scratch for the make.fun 'News Image' bounty
(news-image-20261123). Pure Pillow, no network, deterministic output:
the same code always renders the same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = "entry.png"

FONT_DIR = "/usr/share/fonts/truetype/noto"
BOLD = FONT_DIR + "/NotoSans-Bold.ttf"
REG = FONT_DIR + "/NotoSans-Regular.ttf"

INK = (248, 250, 252)
MUTED = (184, 196, 216)
PANEL = (22, 40, 66)
PANEL_EDGE = (44, 74, 115)
GOLD = (242, 193, 78)
RED = (255, 107, 107)
TEAL = (45, 212, 191)
BLUE = (96, 165, 250)
PURPLE = (192, 132, 252)
ORANGE = (251, 146, 60)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.25, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def panel(draw, box, accent):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=PANEL, outline=PANEL_EDGE, width=2)
    draw.rounded_rectangle([x0, y0, x1, y0 + 10], radius=5, fill=accent)


def label(draw, xy, text, color):
    draw.text(xy, text, font=font(BOLD, 19), fill=color)


def chip(draw, xy, text, color):
    x, y = xy
    f = font(BOLD, 19)
    w = draw.textlength(text, font=f) + 28
    draw.rounded_rectangle([x, y, x + w, y + 36], radius=18, outline=color, width=2)
    draw.text((x + 14, y + 7), text, font=f, fill=color)
    return x + w


def gradient_bg():
    top, bot = (10, 17, 40), (19, 41, 75)
    img = Image.new("RGB", (W, H), top)
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        px[0, y] = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    return img.resize((W, H)) if False else _fill_gradient(img, top, bot)


def _fill_gradient(img, top, bot):
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / (H - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    return img


def main():
    img = gradient_bg()
    d = ImageDraw.Draw(img)
    M = 28            # side margin
    CW = W - 2 * M    # content width

    # ---------- header ----------
    d.text((M, 24), "G L O B A L   N E W S   •   O N E   D A Y ,   O N E   I M A G E",
           font=font(BOLD, 19), fill=GOLD)
    d.text((M, 48), "THE WORLD IN ONE DAY", font=font(BOLD, 63), fill=INK)
    d.text((M, 122), "MONDAY  •  23 NOVEMBER 2026", font=font(BOLD, 24), fill=MUTED)
    d.line([(M, 152), (W - M, 152)], fill=GOLD, width=3)

    # ---------- hero: diplomacy ----------
    box = [M, 166, W - M, 386]
    panel(d, box, GOLD)
    label(d, (M + 24, 188), "DIPLOMACY  •  ABU DHABI", GOLD)
    text_block(d, (M + 24, 216),
               "Ukraine–Russia talks end without a breakthrough",
               font(BOLD, 33), INK, CW - 48, max_lines=2)
    text_block(d, (M + 24, 284),
               "US-mediated negotiations closed with no ceasefire deal — but both "
               "sides agreed in principle to a large prisoner exchange, the day's "
               "one concrete step toward de-escalation.",
               font(REG, 20), MUTED, CW - 48, leading=1.2, max_lines=2)
    chip(d, (M + 24, 344), "PRISONER SWAP: AGREED IN PRINCIPLE", GOLD)

    # ---------- grid row 1 ----------
    gy, gh, gap = 398, 186, 12
    half = (CW - gap) // 2
    # war at sea
    b1 = [M, gy, M + half, gy + gh]
    panel(d, b1, RED)
    label(d, (M + 20, gy + 20), "WAR AT SEA", RED)
    y = text_block(d, (M + 20, gy + 48),
                   "Ukraine says its drones sank a Russian warship",
                   font(BOLD, 25), INK, half - 40, max_lines=2)
    text_block(d, (M + 20, y + 2),
               "Kyiv claims the corvette Merkury was sunk near Benghazi, Libya, "
               "and a Russian cargo ship hit in the Baltic.",
               font(REG, 18), MUTED, half - 40, max_lines=3)
    # climate
    x2 = M + half + gap
    b2 = [x2, gy, W - M, gy + gh]
    panel(d, b2, TEAL)
    label(d, (x2 + 20, gy + 20), "CLIMATE  •  COP31, ANTALYA", TEAL)
    y = text_block(d, (x2 + 20, gy + 48),
                   "Climate summit ends with no pact at all",
                   font(BOLD, 25), INK, half - 40, max_lines=2)
    text_block(d, (x2 + 20, y + 2),
               "The longest UN climate summit collapsed over fossil-fuel wording. "
               "UN chief Guterres: \u201cdeeply disappointed.\u201d",
               font(REG, 18), MUTED, half - 40, max_lines=3)

    # ---------- grid row 2 ----------
    gy2 = gy + gh + gap
    # us politics with big stat
    b3 = [M, gy2, M + half, gy2 + gh]
    panel(d, b3, BLUE)
    label(d, (M + 20, gy2 + 20), "US POLITICS", BLUE)
    d.text((M + 20, gy2 + 44), "258", font=font(BOLD, 64), fill=BLUE)
    d.text((M + 20, gy2 + 116), "House seats for the Democrats",
           font=font(BOLD, 21), fill=INK)
    d.text((M + 20, gy2 + 144), "Their largest majority since 1992.",
           font=font(REG, 18), fill=MUTED)
    # tech with big stat
    b4 = [x2, gy2, W - M, gy2 + gh]
    panel(d, b4, PURPLE)
    label(d, (x2 + 20, gy2 + 20), "TECH  •  NVIDIA", PURPLE)
    d.text((x2 + 20, gy2 + 44), "+30%", font=font(BOLD, 64), fill=PURPLE)
    d.text((x2 + 20, gy2 + 116), "Shares jump in a single day",
           font=font(BOLD, 21), fill=INK)
    d.text((x2 + 20, gy2 + 144), "Founder Jensen Huang returns as CEO.",
           font=font(REG, 18), fill=MUTED)

    # ---------- health band ----------
    hy = gy2 + gh + gap
    b5 = [M, hy, W - M, hy + 118]
    panel(d, b5, ORANGE)
    label(d, (M + 24, hy + 18), "HEALTH EMERGENCY  •  DR CONGO", ORANGE)
    d.text((M + 24, hy + 46), "Ebola response team trapped by fighting in Ituri",
           font=font(BOLD, 27), fill=INK)
    d.text((M + 24, hy + 84),
           "Clashes near a hospital cut off responders as cases pass 11,700.",
           font=font(REG, 20), fill=MUTED)
    d.text((W - M - 24, hy + 30), "11,700+", font=font(BOLD, 44), fill=ORANGE,
           anchor="ra")
    d.text((W - M - 24, hy + 80), "cases", font=font(BOLD, 20), fill=ORANGE,
           anchor="ra")

    # ---------- ticker ----------
    ty = hy + 118 + gap
    d.rounded_rectangle([M, ty, W - M, ty + 62], radius=14, fill=(13, 25, 48),
                        outline=PANEL_EDGE, width=2)
    d.text((M + 20, ty + 19), "ALSO TODAY", font=font(BOLD, 20), fill=GOLD)
    items = ("England to host the 2035 Women's World Cup  •  FBI probes hack of a US "
             "criminal database  •  Mexico arrests fugitive \u2018El Chapo Isidro\u2019")
    text_block(d, (M + 168, ty + 10), items, font(REG, 19), INK, CW - 188,
               leading=1.2, max_lines=2)

    d.text((W // 2, 994), "All stories from Monday 23 November 2026  •  Sources: UN News and wire reports",
           font=font(REG, 16), fill=MUTED, anchor="ma")

    img.save(OUT, format="PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
