#!/usr/bin/env python3
"""
build_font.py

Builds a TTF from flattened clock SVGs.

Input:
    out_svgs_flat/clock_HH_MM.svg   (00:00–11:59)

Output:
    AnalogClockFont.ttf

Codepoints:
    U+E000 => 00:00
    U+E001 => 00:01
    ...
    U+E35F => 11:59
"""

import os
from svgpathtools import svg2paths2
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import newTable

SVG_DIR = "out_svgs_flat"
OUT_FONT = "AnalogClockFont.ttf"

EM = 1000
ASCENT = 1000
DESCENT = 0
SAMPLES = 1024  # high to prevent cracking


def svg_to_glyph(svg_path: str):
    """
    Convert one flattened SVG into a TTGlyph.

    Assumes:
    - SVG already flattened (no transforms, only <path>).
    - Coordinates in 0..1000 x 0..1000.
    """
    paths, attrs, svg_attr = svg2paths2(svg_path)
    pen = TTGlyphPen(None)

    for path in paths:
        # Draw each continuous subpath separately (outer ring, inner ring, etc.)
        for sp in path.continuous_subpaths():
            if sp.length() == 0:
                continue

            # Start point
            p0 = sp.point(0)
            x0 = p0.real
            y0 = EM - p0.imag  # flip Y axis for font space
            pen.moveTo((x0, y0))

            # Sample along the curve
            for i in range(1, SAMPLES + 1):
                t = i / SAMPLES
                p = sp.point(t)
                x = p.real
                y = EM - p.imag
                pen.lineTo((x, y))

            pen.closePath()

    return pen.glyph()


def build_font():
    glyph_order = [".notdef"]
    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    h_metrics = {".notdef": (EM, 0)}
    cmap = {}

    codepoint = 0xE000

    for H in range(12):
        for M in range(60):
            name = f"clock_{H:02d}_{M:02d}"
            svg_file = os.path.join(SVG_DIR, f"{name}.svg")

            if not os.path.exists(svg_file):
                # if a particular glyph is missing, just skip it
                continue

            print(f"[glyph] {svg_file}")
            glyph = svg_to_glyph(svg_file)

            glyph_order.append(name)
            glyphs[name] = glyph
            h_metrics[name] = (EM, 0)
            cmap[codepoint] = name

            codepoint += 1

    if len(glyph_order) == 1:
        raise SystemExit("[error] no glyphs found in out_svgs_flat/")

    fb = FontBuilder(EM, isTTF=True)
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(h_metrics)
    fb.setupHorizontalHeader(ascent=ASCENT, descent=-DESCENT)
    fb.setupOS2(
        sTypoAscender=ASCENT,
        sTypoDescender=-DESCENT,
        usWinAscent=ASCENT,
        usWinDescent=DESCENT,
    )
    fb.setupPost()
    fb.setupMaxp()

    # Name table
    name = newTable("name")
    family = "Analog Clock Font"
    records = {
        1: family,                         # Family
        2: "Regular",                      # Subfamily
        4: f"{family} Regular",            # Full name
        6: "AnalogClockFont-Regular" # PostScript name
    }
    for nid, string in records.items():
        name.setName(string, nid, 3, 1, 0x409)  # Windows, Unicode, en-US
        name.setName(string, nid, 1, 0, 0)      # Mac, Roman, English

    fb.font["name"] = name

    fb.save(OUT_FONT)
    print(f"[done] wrote {OUT_FONT}")


if __name__ == "__main__":
    build_font()
