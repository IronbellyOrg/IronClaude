"""Draw the proto_layouts JSON screens as PNG with DejaVu Sans Mono (one cell = one fixed box).

Run: uv run --no-project --with pillow python .dev/issues/409/visual-parity/layout-compare/rasterise.py
"""

import json
import pathlib

from PIL import Image, ImageDraw, ImageFont

BASE = pathlib.Path(".dev/issues/409/visual-parity/layout-compare")
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SIZE = 16
BG, FG = (11, 22, 32), (225, 233, 238)
regular = ImageFont.truetype(FONT_DIR + "DejaVuSansMono.ttf", SIZE)
bold = ImageFont.truetype(FONT_DIR + "DejaVuSansMono-Bold.ttf", SIZE)
CW = round(regular.getlength("M"))
CH = SIZE + 5
PAD = 14

for src in sorted((BASE / "screens").glob("*.json")):
    lines = json.loads(src.read_text(encoding="utf-8"))
    cols = max(sum(len(t) for t, _, _ in line) for line in lines)
    img = Image.new("RGB", (cols * CW + 2 * PAD, len(lines) * CH + 2 * PAD), BG)
    draw = ImageDraw.Draw(img)
    for row, line in enumerate(lines):
        col = 0
        for text, colour, is_bold in line:
            for ch in text:
                if ch != " ":
                    draw.text((PAD + col * CW, PAD + row * CH), ch,
                              font=bold if is_bold else regular, fill=tuple(colour) if colour else FG)
                col += 1
    out = BASE / (src.stem + ".png")
    img.save(out)
    print(out, img.size)
