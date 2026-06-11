![The stair](image.png)

# Industrial Stair Calculator

Streamlit-based calculation and verification tool for industrial stairs and stepladders per **ISO 14122-3:2016**.

## Features

- **3 input modes:** total rise height (H), number of steps (N), or desired angle
- **Automatic stair/stepladder detection** based on computed angle
- **ISO 14122-3 compliance checks:** angle range, Blondel formula, tread depth, riser height, stair width
- **Side-view SVG** with dimension labels (H, L, angle)
- **Real-time feedback** — compliant in blue, violations in red

## Quick Start (Windows)

```bash
install.bat   # creates venv and installs deps
start.bat     # launches streamlit app
```

## Manual Install

```bash
git clone <repo-url>
cd the-stair-calculator-ISO-14122
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
streamlit run stair.py
```

## How it works

| Input | Stair | Stepladder |
|---|---|---|
| Angle range | 20° – 45° | 45° – 75° |
| Tread (g) min | 200 mm | 150 mm |
| Riser (h) max | 240 mm | 250 mm |
| Width (W) min | 600 mm | 500 mm |
| Blondel (g+2h) | 600–660 mm | — |

Tread is derived from the Blondel formula `g = 630 − 2h`, then the angle is computed as `atan(h/g)`.

## Stack

- **Python 3** + **Streamlit**
- Pure SVG rendering (no extra libs)
- Single-file app: `stair.py` (231 lines)

## Reference

**ISO 14122-3:2016** — Safety of machinery — Permanent means of access to machinery — Part 3: Stairs, stepladders and guard-rails.
