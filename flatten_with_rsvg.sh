#!/usr/bin/env bash
set -e

# This script flattens all SVGs in a folder using rsvg-convert.
# It removes all transforms, groups, strokes, masks, etc., and outputs
# pure-path SVGs suitable for font building.

IN_DIR="out_svgs"
OUT_DIR="out_svgs_flat"

mkdir -p "$OUT_DIR"

echo "[flatten] Using rsvg-convert…"

for FILE in "$IN_DIR"/*.svg; do
    NAME=$(basename "$FILE")
    OUTFILE="$OUT_DIR/$NAME"

    echo " → $NAME"
    rsvg-convert "$FILE" --format=svg --output="$OUTFILE"
done

echo "[done] Flattened SVGs saved to $OUT_DIR/"
