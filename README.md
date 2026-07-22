![The stair](image.png)

# Industrial Stair Calculator

Streamlit-based calculation and verification tool for industrial stairs and stepladders per **ISO 14122-3:2016**.

## Features

- **3 input modes:** Steps (N), horizontal run (L), or desired angle
- **Step offsets:** Pd (bottom) and Pup (top) — distances from floor to first/last step
- **Automatic stair/stepladder detection** based on inclination angle
- **ISO 14122-3 compliance checks:** angle range, Blondel formula, tread depth, riser height, stair width
- **Side-view SVG** with all dimensions (H, L, angle, Pd, Pup) and orange offset markers
- **Real-time feedback** — compliant steps in blue, violations in red

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

| Type | Angle | Tread (g) min | Riser (h) max | Width (W) min | Blondel (g+2h) |
|---|---|---|---|---|---|
| Stairs | 20° – 45° | 200 mm | 240 mm | 600 mm | 600–660 mm |
| Stepladders | 45° – 75° | 150 mm | 250 mm | 500 mm | — |

The stair type is detected automatically from the computed angle.
Tread is derived from the Blondel formula `g = 630 − 2h`, then the angle is computed as `atan(h/g)`.

### Step offsets (Pd, Pup)

- **Pd** — vertical distance from lower floor to the first step
- **Pup** — vertical distance from the last step to the upper floor
- Effective rise height for the steps: `H_net = H − Pd − Pup`
- Each step height: `h = H_net / N`
- Horizontal offset: `x_off = (Pd + Pup) / tan(a)`
- Total run: `L = (N−1)·g + x_off`
- The solver iterates (15 iterations) to converge on the correct angle with offsets

## Input modes

| Mode | You set | Calculated |
|---|---|---|
| Steps (N) | H, N, Pd, Pup | h, g, L, angle |
| L (horizontal) | H, L, Pd, Pup | N, h, g, angle |
| Desired angle (°) | H, angle, Pd, Pup | N, h, g, L |

Each mode has a slider + manual number input (synchronised).

## Stack

- **Python 3** + **Streamlit**
- Pure SVG rendering (no extra libs)
- Single-file app: `stair.py`

## Reference

**ISO 14122-3:2016** — Safety of machinery — Permanent means of access to machinery — Part 3: Stairs, stepladders and guard-rails.
