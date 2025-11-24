#!/usr/bin/env python3
import os
from svgpathtools import svg2paths2, Path, wsvg

FRAME = "frame.svg"
HOUR = "hour.svg"
MINUTE = "minute.svg"

OUTDIR = "out_svgs"
os.makedirs(OUTDIR, exist_ok=True)

CENTER = 500 + 500j


def load_paths(filename):
    if not os.path.exists(filename):
        return []
    paths, attrs, svgattrs = svg2paths2(filename)
    return paths


frame_paths = load_paths(FRAME)
hour_base = load_paths(HOUR)
minute_base = load_paths(MINUTE)


def rotate_paths(paths, angle_deg):
    ang = angle_deg * 3.141592653589793 / 180
    return [Path(*[seg.rotated(ang, CENTER) for seg in p]) for p in paths]


for H in range(12):
    for M in range(60):
        outname = f"{OUTDIR}/clock_{H:02d}_{M:02d}.svg"

        svgpaths = []

        # frame (no rotation)
        svgpaths += frame_paths

        # hour hand
        if hour_base:
            hour_angle = (H % 12) * 30 + (M / 60) * 30
            svgpaths += rotate_paths(hour_base, hour_angle)

        # minute hand
        if minute_base:
            minute_angle = M * 6
            svgpaths += rotate_paths(minute_base, minute_angle)

        wsvg(svgpaths, filename=outname, svg_attributes={'viewBox': '0 0 1000 1000'})

print("[done] generated 720 clock SVGs in out_svgs/")
