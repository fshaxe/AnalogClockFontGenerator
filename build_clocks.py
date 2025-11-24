#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import math
import os
import copy

FRAME = "frame.svg"
HOUR = "hour.svg"
MINUTE = "minute.svg"

OUTDIR = "out_svgs"
os.makedirs(OUTDIR, exist_ok=True)

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

def load_children(path):
    if not os.path.exists(path):
        return None, None
    tree = ET.parse(path)
    root = tree.getroot()
    children = [copy.deepcopy(child) for child in root]
    return root, children

frame_root, frame_children = load_children(FRAME)
hour_root, hour_children = load_children(HOUR)
minute_root, minute_children = load_children(MINUTE)

if frame_root is None:
    frame_root = ET.Element(f"{{{SVG_NS}}}svg", {
        "viewBox": "0 0 1000 1000",
        "width": "1000",
        "height": "1000",
    })

viewBox = frame_root.attrib.get("viewBox", "0 0 1000 1000")
width   = frame_root.attrib.get("width",  "1000")
height  = frame_root.attrib.get("height", "1000")

def make_clock(h, m):
    root = copy.deepcopy(frame_root)
    root.set("viewBox", viewBox)
    root.set("width", width)
    root.set("height", height)

    hour_angle = h * 30 + m * 0.5
    minute_angle = m * 6

    # Hour hand
    if hour_children:
        g = ET.Element(f"{{{SVG_NS}}}g", {
            "transform": f"rotate({hour_angle} 500 500)"
        })
        for ch in hour_children:
            g.append(copy.deepcopy(ch))
        root.append(g)

    # Minute hand
    if minute_children:
        g = ET.Element(f"{{{SVG_NS}}}g", {
            "transform": f"rotate({minute_angle} 500 500)"
        })
        for ch in minute_children:
            g.append(copy.deepcopy(ch))
        root.append(g)

    return ET.ElementTree(root)

for h in range(12):
    for m in range(60):
        svg = make_clock(h, m)
        out = f"{OUTDIR}/clock_{h:02d}_{m:02d}.svg"
        svg.write(out, encoding="utf-8", xml_declaration=True)

print("[done] 720 clocks in out_svgs/")
