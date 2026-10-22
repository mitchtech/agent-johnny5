"""Derive the nine-row web pet atlas from the active bundle; never change source art."""

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SHEET = ROOT / "pets" / "johnny5" / "spritesheet.webp"
EXPORT = ROOT / "assets" / "exports" / "agent-johnny5-pet-web.webp"
REVISION = ROOT / "assets" / "pet-revision.json"
# The web format keeps the nine animation rows and omits the two look-direction rows.
WEB_SIZE = (1536, 1872)


def render():
    with Image.open(SHEET) as source:
        return source.convert("RGBA").crop((0, 0, *WEB_SIZE))


def export():
    web = render()
    EXPORT.parent.mkdir(parents=True, exist_ok=True)
    web.save(EXPORT, lossless=True, quality=100, method=6, exact=True)
    revision = json.loads(REVISION.read_text())
    revision["web"] = {"file": EXPORT.relative_to(ROOT).as_posix(), "sha256": hashlib.sha256(EXPORT.read_bytes()).hexdigest()}
    REVISION.write_text(json.dumps(revision, indent=2) + "\n")
    print(json.dumps(revision["web"], indent=2))


if __name__ == "__main__":
    export()
