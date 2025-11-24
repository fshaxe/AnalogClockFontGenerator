# Analog Clock Font Generator
Generates all 720 analog clock faces (00:00 → 11:59) from 3 SVG components, flattens them, and builds a .TTF font containing one glyph per minute.

## Prerequisites
Linux or macOS  
[Homebrew](https://brew.sh/) (macOS)  
[git](https://git-scm.com/install/)

## Inputs
The clock builder expects 3 components, `frame.svg`, `hour.svg`, and `minute.svg`.  
Each component is optional, mainly for clocks without frames.

Canvas size must be 1000x1000, or `viewbox = "0 0 1000 1000"`.  
You can check this by opening the `.svg` file in a text editor and reading the first few lines.

Hour and Minute hands pivot around the center of the canvas (500, 500), the frame stays still.  
Hour and Minute hands should stand straight up at 00.

**All components must be turned into stroke outlines**  
Expand stroke, Outline curve, or Stroke to path, depending on your design software.  
**Flatten all transforms or properties when exporting**

## Usage
Similar across OS and Shells, read comments for variations.
```
cd ~/Downloads
git clone https://github.com/fshaxe/AnalogClockFontGenerator
cd AnalogClockFontGenerator

python3 -m venv .venv
# fish shell users use: source .venv/bin/activate.fish
source .venv/bin/activate
pip install svgpathtools fonttools

# place your SVG components in this directory

python build_clocks.py

# install librsvg using your package manager
# on macOS: brew install librsvg

chmod +x flatten_with_rsvg.sh
./flatten_with_rsvg.sh

python build_font.py
```
Now your font is ready as a .TTF in the clone root.  
Use your favourite font previewer to inspect.

## Indexing
Glyphs start in the Private Use Area at U+E000.
```
U+E000 → 00:00
U+E001 → 00:01  
U+E002 → 00:02  
…  
U+E03B → 00:59  
U+E03C → 01:00  
…  
U+E35F → 11:59
```
Formula:
```
index = hour * 60 + minute  
codepoint = 0xE000 + index
```
