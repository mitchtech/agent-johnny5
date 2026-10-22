"""Build labeled promotional previews from the committed clips and pet atlas, not host recordings."""

import hashlib
import json
import shutil
import subprocess
import wave
from array import array
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "promotion"
OUT.mkdir(parents=True, exist_ok=True)
SIZE, FPS, RATE = 1080, 15, 32000
BG, INK, MUTED, AMBER, RED = (17, 20, 23), (236, 230, 217), (163, 170, 174), (255, 176, 0), (255, 59, 48)
CRT, GRATICULE = (10, 13, 11), (52, 42, 14)
FONTS = ROOT / "site" / "fonts"
TITLE = FONTS / "chakra-petch-latin-700-normal.woff2"
BODY = FONTS / "ibm-plex-sans-latin-400-normal.woff2"
MONO = FONTS / "share-tech-mono-latin-400-normal.woff2"
ATLAS = ROOT / "pets" / "johnny5" / "spritesheet.webp"
SHEET = Image.open(ATLAS).convert("RGBA")
# Atlas rows and frame counts for the host animation states used below.
STATES = {"idle": (0, 6), "waving": (3, 4), "failure": (5, 8), "waiting": (6, 6), "working": (7, 6), "review": (8, 6)}


def samples(clip):
    with wave.open(str(ROOT / f"audio/{clip}.wav")) as source:
        assert (source.getframerate(), source.getnchannels(), source.getsampwidth()) == (RATE, 1, 2)
        data = array("h", source.readframes(source.getnframes()))
    if sys.byteorder == "big":
        data.byteswap()
    return data


def little_endian(data):
    copy = array("h", data)
    if sys.byteorder == "big":
        copy.byteswap()
    return copy.tobytes()


def peaks(data, columns):
    step = max(1, len(data) // columns)
    values = [max((abs(v) for v in data[i * step:(i + 1) * step]), default=0) for i in range(columns)]
    top = max(values) or 1
    return [value / top for value in values]


def text(draw, y, content, size=42, color=INK, face=BODY):
    font = ImageFont.truetype(str(face), size)
    for line in content.split("\n"):
        width = draw.textlength(line, font=font)
        if width > 940:
            raise ValueError(f"Caption exceeds safe width: {line}")
        draw.text(((SIZE - width) / 2, y), line, font=font, fill=color)
        y += size * 1.25


def card(title, subtitle, footer, command=None):
    image = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)
    for x in range(0, SIZE, 24):
        draw.line((x, 0, x, SIZE), fill=(28, 31, 32))
        draw.line((0, x, SIZE, x), fill=(28, 31, 32))
    draw.ellipse((396, 98, 408, 110), fill=RED)
    text(draw, 90, "AGENT JOHNNY 5", 30, AMBER, MONO)
    text(draw, 150, title.upper(), 76, INK, TITLE)
    text(draw, 270, subtitle, 38)
    if command:
        text(draw, 790, command, 36, AMBER, MONO)
    text(draw, 870, "github.com/mitchtech/agent-johnny5", 34, AMBER, MONO)
    text(draw, 944, footer, 26, MUTED)
    return image


def robot(state, second, scale):
    """The state's animation frame at `second`, scaled; frames advance every 160 ms like the host."""
    row, count = STATES[state]
    column = int(second / 0.16) % count
    cell = SHEET.crop((column * 192, row * 208, (column + 1) * 192, (row + 1) * 208))
    return cell.resize((round(192 * scale), round(208 * scale)), Image.Resampling.LANCZOS)


def scope(values, reveal, width=720, height=360):
    """A width x height CRT with the waveform swept in up to `reveal` (0-1)."""
    screen = Image.new("RGBA", (width, height), CRT + (255,))
    draw = ImageDraw.Draw(screen)
    for i in range(1, 10):
        draw.line((width * i // 10, 0, width * i // 10, height), fill=GRATICULE)
    for i in range(1, 8):
        draw.line((0, height * i // 8, width, height * i // 8), fill=GRATICULE)
    trace = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    lines = ImageDraw.Draw(trace)
    middle = height // 2
    shown = int(len(values) * reveal)
    for index, value in enumerate(values):
        x = 10 + index * (width - 20) / len(values)
        if index < shown:
            amplitude = max(1, value * height * 0.42)
            lines.line((x, middle - amplitude, x, middle + amplitude), fill=AMBER + (255,), width=3)
        else:
            lines.line((x, middle, x + 4, middle), fill=AMBER + (110,), width=2)
    screen.alpha_composite(trace.filter(ImageFilter.GaussianBlur(5)))
    screen.alpha_composite(trace)
    for y in range(0, height, 3):
        draw.line((0, y, width, y), fill=(0, 0, 0, 70))
    return screen


# (start, end, title, subtitle, command, cue clip or None, pet state)
sound_scenes = [
    (0, 6, "Session started", '"Number five is alive!"', None, "alive", "waving"),
    (6, 10, "Approval needed", '"Need input"', None, "need-input", "waiting"),
    (10, 15, "Destructive command", '"No disassemble, Number Five!"', "$ rm -rf ./build", "no-disassemble-five", "failure"),
    (15, 19, "Ready for input", '"More input"', None, "more-input", "idle"),
    (19, 24, "Need input.", "Local audio. No telemetry. Never blocks anything.\nOptional Codex pet installs separately.", None, None, "idle"),
]
attention_scenes = [
    (0, 5, "Keep the useful cues", "Use the attention preset", "agent-johnny5 preset attention", None, "idle"),
    (5, 12, "Less prompt chatter", "Approval, question, and ready cues stay on\nwhere your host supports them.", "agent-johnny5 preset attention", "need-input", "waiting"),
]
pet_scenes = [
    (0, 4, "Codex companion", "Independent pet. Sounds not required.", "state: idle", None, "idle"),
    (4, 8, "Host animated", "Compatible Codex hosts drive activity.", "state: working", None, "working"),
    (8, 12, "Nine animations", "Sixteen look directions. Tank treads.", "state: review", None, "review"),
    (12, 16, "Your choice", "Download the ZIP. Choose Johnny 5 yourself.", "state: waving", None, "waving"),
]
CUE_OFFSET = 0.5


def build(name, scenes, footer):
    duration = scenes[-1][1]
    temporary = ROOT / "dist/promotion/render"
    temporary.mkdir(parents=True, exist_ok=True)
    video = temporary / f"{name}.mp4"
    command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
               "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{SIZE}x{SIZE}",
               "-framerate", str(FPS), "-i", "pipe:0",
               "-frames:v", str(duration * FPS), "-c:v", "libx264", "-threads", "2",
               "-preset", "fast", "-crf", "26", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(video)]
    cards = [card(title, subtitle, footer, cmd) for _, _, title, subtitle, cmd, _, _ in scenes]
    clips = {scene[5]: samples(scene[5]) for scene in scenes if scene[5]}
    pet_only = not clips
    waves = {clip: peaks(data, 180) for clip, data in clips.items()}
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for tick in range(duration * FPS):
            second = tick / FPS
            index = next(i for i, scene in enumerate(scenes) if scene[0] <= second < scene[1])
            start, _, _, _, _, clip, state = scenes[index]
            image = cards[index].copy()
            if pet_only:
                sprite = robot(state, second, 2.0)
                image.paste(sprite, (540 - sprite.width // 2, 360), sprite)
            else:
                if clip:
                    length = len(clips[clip]) / RATE
                    reveal = min(1.0, max(0.0, (second - start - CUE_OFFSET) / length))
                    screen = scope(waves[clip], reveal, 560, 330)
                else:
                    screen = scope([0.01] * 180, 1.0, 560, 330)
                image.paste(screen.convert("RGB"), (420, 410))
                sprite = robot(state, second, 1.5)
                image.paste(sprite, (100, 770 - round(205 * 1.5)), sprite)
            process.stdin.write(image.tobytes())
            if tick == FPS * 3:
                image.save(OUT / f"{name}.png")
    finally:
        process.stdin.close()
    if process.wait():
        raise RuntimeError(f"ffmpeg failed for {name}")
    if pet_only:
        # The pet is independent of the sounds, so its preview has no audio track.
        shutil.copyfile(video, OUT / f"{name}.mp4")
    else:
        track = bytearray(duration * RATE * 2)
        for start, _, _, _, _, clip, _ in scenes:
            if clip:
                data = little_endian(clips[clip])
                offset = int((start + CUE_OFFSET) * RATE) * 2
                track[offset:offset + len(data)] = data
        audio = temporary / f"{name}.wav"
        with wave.open(str(audio), "wb") as destination:
            destination.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
            destination.writeframes(bytes(track))
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(video), "-i", str(audio),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k",
                        "-t", str(duration), "-movflags", "+faststart", str(OUT / f"{name}.mp4")], check=True)

    def timestamp(second):
        return f"00:{second // 60:02d}:{second % 60:02d},000"

    subtitles = [f"{index}\n{timestamp(start)} --> {timestamp(end)}\n{title}\n{subtitle}\n{footer}\n"
                 for index, (start, end, title, subtitle, *_) in enumerate(scenes, 1)]
    (OUT / f"{name}.srt").write_text("\n".join(subtitles))
    return sorted(clips)


used = build("sound-preview", sound_scenes, "Illustrated sound preview - not a live host recording")
used += build("attention-preview", attention_scenes, "Configuration preview - event coverage varies by host")
used += build("pet-preview", pet_scenes, "Atlas animation preview - not a native host recording")
sources = [ROOT / f"audio/{clip}.wav" for clip in sorted(set(used))] + [ATLAS, TITLE, BODY, MONO]


def record(path):
    return {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


manifest = {
    "kind": "illustrated-previews", "dimensions": [SIZE, SIZE], "fps": FPS,
    "sources": [record(path) for path in sources],
    "artifacts": [record(path) for path in sorted(OUT.iterdir()) if path.suffix in (".mp4", ".png", ".srt")],
    "tools": {"Pillow": __import__("PIL").__version__, "ffmpeg": subprocess.check_output(
        ["ffmpeg", "-version"], text=True).splitlines()[0]},
    "credentials_used": [],
    "limitations": ["Not a live host or physical audio recording.",
                     "No claim of hook execution or native pet rendering in these videos.",
                     "Audio is assembled from the bundled, separately noticed Short Circuit clips."],
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(f"Built three captioned previews in {OUT.relative_to(ROOT)}")
