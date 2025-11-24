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
    tree = ET.parse(path)
    root = tree.getroot()
    return [copy.deepcopy(child) for child in root]

frame_tree = ET.parse(FRAME)
frame_root = frame_tree.getroot()

hour_children  = load_children(HOUR)
minute_children = load_children(MINUTE)

viewBox = frame_root.attrib.get("viewBox", "0 0 1000 1000")
width   = frame_root.attrib.get("width",  "1000")
height  = frame_root.attrib.get("height", "1000")

def make_clock(h, m):
    root = copy.deepcopy(frame_root)
    root.set("viewBox", viewBox)
    root.set("width", width)
    root.set("height", height)

    hour_angle   = h * 30 + m * 0.5
    minute_angle = m * 6

    hour_group = ET.Element(f"{{{SVG_NS}}}g", attrib={
        "transform": f"rotate({hour_angle} 500 500)"
    })
    for ch in hour_children:
        hour_group.append(copy.deepcopy(ch))

    minute_group = ET.Element(f"{{{SVG_NS}}}g", attrib={
        "transform": f"rotate({minute_angle} 500 500)"
    })
    for ch in minute_children:
        minute_group.append(copy.deepcopy(ch))

    root.append(hour_group)
    root.append(minute_group)

    return ET.ElementTree(root)

for h in range(12):
    for m in range(60):
        svg = make_clock(h, m)
        out = f"{OUTDIR}/clock_{h:02d}_{m:02d}.svg"
        svg.write(out, encoding="utf-8", xml_declaration=True)

print("[done] 720 clocks in out_svgs/")
