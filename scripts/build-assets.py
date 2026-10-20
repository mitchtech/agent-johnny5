"""Derive preview artifacts from the committed clips; never change source audio."""

import sys
import tempfile
import wave
from array import array
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
AUDIO = ROOT / "audio"
PREVIEWS = ROOT / "assets" / "previews"
FONTS = ROOT / "site" / "fonts"
# --check renders elsewhere and compares pixels: PNG bytes vary with each platform's zlib.
CHECK = "--check" in sys.argv[1:]
OUT = Path(tempfile.mkdtemp()) if CHECK else PREVIEWS
OUT.mkdir(parents=True, exist_ok=True)
BACKGROUND = (17, 20, 23)
GRID = (30, 33, 33)
CRT = (10, 13, 11)
INK = (236, 230, 217)
MUTED = (163, 170, 174)
AMBER = (255, 176, 0)
GRATICULE = (52, 42, 14)
LED = (255, 59, 48)
HEADLINE_CLIPS = [
    ("alive", "Number five is alive!"),
    ("need-input", "Need input"),
    ("no-disassemble-five", "No disassemble!"),
    ("more-input", "More input"),
    ("malfunction", "Malfunction"),
]


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size, layout_engine=ImageFont.Layout.BASIC)


def tracked(draw, xy, text, typeface, fill, spacing):
    x, y = xy
    for character in text:
        draw.text((x, y), character, font=typeface, fill=fill)
        x += draw.textlength(character, font=typeface) + spacing
    return x


def peaks(clip, columns):
    with wave.open(str(AUDIO / f"{clip}.wav")) as audio:
        samples = array("h", audio.readframes(audio.getnframes()))
    if sys.byteorder == "big":
        samples.byteswap()
    step = max(1, len(samples) // columns)
    values = [max((abs(value) for value in samples[i * step:(i + 1) * step]), default=0) / 32768 for i in range(columns)]
    top = max(values) or 1
    return [value / top for value in values]


def paper(width, height):
    canvas = Image.new("RGBA", (width, height), BACKGROUND + (255,))
    draw = ImageDraw.Draw(canvas)
    for x in range(0, width, 24):
        draw.line((x, 0, x, height), fill=GRID)
    for y in range(0, height, 24):
        draw.line((0, y, width, y), fill=GRID)
    return canvas


def screen(size, clip, reveal=1.0, inset=0):
    """A CRT with graticule and the clip's waveform swept in up to `reveal`."""
    width, height = size
    canvas = Image.new("RGBA", size, CRT + (255,))
    draw = ImageDraw.Draw(canvas)
    for i in range(1, 10):
        x = inset + (width - 2 * inset) * i // 10
        draw.line((x, 0, x, height), fill=GRATICULE)
    for i in range(1, 8):
        y = height * i // 8
        draw.line((0, y, width, y), fill=GRATICULE)
    middle = height // 2
    usable = width - 2 * inset
    columns = max(2, usable // 3)
    values = peaks(clip, columns)
    shown = int(columns * reveal)
    trace = Image.new("RGBA", size, (0, 0, 0, 0))
    lines = ImageDraw.Draw(trace)
    for index in range(columns):
        x = inset + index * usable / columns
        if index < shown:
            amplitude = max(1, values[index] * height * 0.4)
            lines.line((x, middle - amplitude, x, middle + amplitude), fill=AMBER + (255,), width=2)
        else:
            lines.line((x, middle, x + 3, middle), fill=AMBER + (110,), width=1)
    canvas.alpha_composite(trace.filter(ImageFilter.GaussianBlur(4)))
    canvas.alpha_composite(trace)
    for y in range(0, height, 3):
        draw.line((0, y, width, y), fill=(0, 0, 0, 70))
    return canvas


def panel(canvas, box, clip):
    left, top, right, bottom = box
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw.rounded_rectangle(box, radius=18, fill=(34, 38, 43, 255), outline=(58, 65, 72, 255), width=2)
    label = font("share-tech-mono-latin-400-normal.woff2", 18)
    tracked(draw, (left + 22, top + 16), "CH1  VOICE OUTPUT", label, (185, 178, 161), 3)
    draw.ellipse((right - 36, top + 18, right - 22, top + 32), fill=LED)
    crt = screen((right - left - 36, bottom - top - 64), clip, inset=8)
    mask = Image.new("L", crt.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, crt.width - 1, crt.height - 1), radius=14, fill=255)
    canvas.paste(crt, (left + 18, top + 46), mask)


def headline(canvas, xy, size, limit):
    draw = ImageDraw.Draw(canvas, "RGBA")
    x, y = xy
    # Shrink to fit beside the scope panel rather than running under it.
    while draw.textlength("NEED INPUT.", font=font("chakra-petch-latin-700-normal.woff2", size)) > limit:
        size -= 2
    display = font("chakra-petch-latin-700-normal.woff2", size)
    draw.text((x, y), "NEED", font=display, fill=INK)
    offset = x + draw.textlength("NEED ", font=display)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((offset, y), "INPUT.", font=display, fill=AMBER + (140,))
    canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(12)))
    draw.text((offset, y), "INPUT.", font=display, fill=AMBER)


def eyebrow(canvas, xy, size):
    draw = ImageDraw.Draw(canvas, "RGBA")
    x, y = xy
    draw.ellipse((x, y + size // 2 - 5, x + 10, y + size // 2 + 5), fill=LED)
    tracked(draw, (x + 22, y), "AGENT JOHNNY 5", font("share-tech-mono-latin-400-normal.woff2", size), AMBER, 5)


# Waveform previews: a sweep that reveals each clip, then holds.
label_font = font("share-tech-mono-latin-400-normal.woff2", 20)
for clip, line in HEADLINE_CLIPS:
    frames = []
    steps = 14
    for step in range(steps + 1):
        canvas = Image.new("RGBA", (288, 200), BACKGROUND + (255,))
        crt = screen((272, 150), clip, reveal=step / steps, inset=6)
        canvas.alpha_composite(crt, (8, 8))
        draw = ImageDraw.Draw(canvas)
        width = draw.textlength(line.upper(), font=label_font)
        draw.text(((288 - width) / 2, 166), line.upper(), font=label_font, fill=AMBER if step == steps else MUTED)
        frames.append(canvas.convert("RGB"))
    durations = [70] * steps + [1600]
    frames[0].save(OUT / f"{clip}.gif", save_all=True, append_images=frames[1:], duration=durations, loop=0, disposal=2)

# Fonts are the site's self-hosted OFL faces, so the cards match the page on every OS.
card = paper(1200, 630)
draw = ImageDraw.Draw(card, "RGBA")
eyebrow(card, (88, 92), 24)
headline(card, (82, 140), 132, 580)
draw.text((90, 310), "Your coding agent, with a robot's", font=font("chakra-petch-latin-500-normal.woff2", 38), fill=INK)
draw.text((90, 356), "sense of urgency.", font=font("chakra-petch-latin-500-normal.woff2", 38), fill=INK)
for row, text in enumerate(["Short Circuit sound cues for", "Claude Code, Codex, and Gemini CLI"]):
    draw.text((90, 470 + row * 38), text, font=font("ibm-plex-sans-latin-400-normal.woff2", 28), fill=MUTED)
panel(card, (700, 150, 1130, 480), "need-input")
card.convert("RGB").save(OUT / "social.png")

banner = paper(1280, 440)
draw = ImageDraw.Draw(banner, "RGBA")
eyebrow(banner, (92, 80), 22)
headline(banner, (86, 122), 140, 700)
draw.text((94, 300), "Sound cues for coding agents. No disassemble.", font=font("ibm-plex-sans-latin-400-normal.woff2", 30), fill=MUTED)
panel(banner, (830, 70, 1200, 370), "alive")
banner.convert("RGB").save(OUT / "banner.png")

touch = Image.new("RGBA", (180, 180), BACKGROUND + (255,))
draw = ImageDraw.Draw(touch)
draw.rounded_rectangle((12, 44, 168, 136), radius=24, fill=(34, 38, 43), outline=AMBER, width=3)
for cx in (58, 122):
    glow = Image.new("RGBA", touch.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((cx - 34, 56, cx + 34, 124), fill=AMBER + (150,))
    touch.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    draw.ellipse((cx - 28, 62, cx + 28, 118), fill=(138, 84, 0))
    draw.ellipse((cx - 20, 70, cx + 20, 110), fill=AMBER)
    draw.ellipse((cx - 14, 74, cx - 2, 86), fill=(255, 246, 216))
draw.rounded_rectangle((26, 26, 82, 34), radius=4, fill=AMBER)
draw.rounded_rectangle((98, 26, 154, 34), radius=4, fill=AMBER)
touch.convert("RGB").save(OUT / "touch-icon.png")


def frames_of(path):
    with Image.open(path) as image:
        return [(item.convert("RGBA"), item.info.get("duration")) for item in ImageSequence.Iterator(image)]


if CHECK:
    stale = []
    for built in sorted(OUT.iterdir()):
        committed = PREVIEWS / built.name
        if not committed.exists():
            stale.append(built.name)
            continue
        expected, actual = frames_of(committed), frames_of(built)
        if len(expected) != len(actual) or any(a[1] != b[1] or ImageChops.difference(a[0], b[0]).getbbox(alpha_only=False) for a, b in zip(expected, actual)):
            stale.append(built.name)
    if stale:
        sys.exit(f"Preview assets are stale; run python3 scripts/build-assets.py: {', '.join(stale)}")
    print("Preview assets match the current clips and fonts")
else:
    print(f"Built preview assets in {OUT}")
