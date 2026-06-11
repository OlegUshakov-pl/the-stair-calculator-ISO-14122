# Industrial Stair Calculator

Calculation and verification of industrial stairs per **ISO 14122-3** (Safety of machinery — Permanent means of access to machinery).

## Features

- Calculate stair parameters from: total rise height (H), number of steps (N), or inclination angle
- Automatic ISO 14122-3 compliance checks:
  - Inclination angle: 30°–38°
  - Blondel formula: 600–660 mm
  - Minimum tread depth: 200 mm
  - Minimum stair width: 600 mm
- Side-view SVG visualization
- Non-compliant parameters highlighted in red

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd streamlit
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run stair.py
```

The app will open in your browser.

1. Choose input mode: total height, number of steps, or angle
2. Adjust parameters with the sliders
3. The stair diagram and metrics are displayed on the right
4. Compliance status is shown in the left panel

## Standard

**ISO 14122-3:2016** — Safety of machinery — Permanent means of access to machinery — Part 3: Stairs, stepladders and guard-rails.
