import streamlit as st
import math

st.set_page_config(page_title="ISO 14122-3 Stair Calculator", layout="wide")

st.title("Industrial Stair Calculator")
st.caption("Calculation and verification per ISO 14122-3 (Safety of machinery)")

col_sidebar, col_main = st.columns([1, 2])

with col_sidebar:
    st.header("Input Parameters")

    input_mode = st.selectbox(
        "Input mode",
        ["Total rise height (H)", "Steps (N)", "Angle"]
    )

    H = st.number_input("Total rise height (H), mm", min_value=300, max_value=4000, value=1500, step=50)

    if input_mode == "Steps (N)":
        N = st.number_input("Number of steps (N)", min_value=1, max_value=30, value=round(H / 180), step=1)
        h_actual = H / N
    elif input_mode == "Angle":
        angle_desired = st.slider("Desired angle (°)", 30, 38, 33)
        angle_rad = math.radians(angle_desired)
        h_actual = 630 * math.tan(angle_rad) / (1 + 2 * math.tan(angle_rad))
        N = round(H / h_actual)
        if N == 0:
            N = 1
        h_actual = H / N
    else:
        h_target = st.slider("Desired riser height (h), mm", 140, 250, 180)
        N = round(H / h_target)
        if N == 0:
            N = 1
        h_actual = H / N

    W = st.slider("Stair width, mm", 600, 1200, 800)

    g_actual = 630 - (2 * h_actual)

    if g_actual < 50:
        g_actual = 50

    angle = math.degrees(math.atan(h_actual / g_actual))

    L = g_actual * (N - 1)

    blondel = g_actual + 2 * h_actual
    is_valid_blondel = 600 <= blondel <= 660
    is_valid_angle = 30 <= angle <= 38
    is_valid_h = h_actual <= 250
    is_valid_g = g_actual >= 200
    is_valid_w = W >= 600

    is_all_valid = all([is_valid_blondel, is_valid_angle, is_valid_h, is_valid_g, is_valid_w])

    st.markdown("---")
    st.subheader("ISO 14122-3 Compliance")

    if is_all_valid:
        st.success("Staircase fully complies with the standard!")
    else:
        st.error("Standard requirements violations detected:")
        if not is_valid_angle:
            st.warning(f"Inclination angle {angle:.1f}° outside allowed range (30°–38°).")
        if not is_valid_blondel:
            st.warning(f"Blondel formula {blondel:.0f} mm outside allowed range (600–660 mm).")
        if not is_valid_g:
            st.warning(f"Tread depth {g_actual:.1f} mm too small (min. 200 mm).")

with col_main:
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Steps (N)", f"{N}")
    m_col2.metric("Riser (h)", f"{h_actual:.1f} mm")
    m_col3.metric("Tread (g)", f"{g_actual:.1f} mm")
    m_col4.metric("Angle", f"{angle:.1f}°")

    svg_w = 800
    svg_h = 500
    padding = 50

    max_real_w = max(L, 500)
    max_real_h = max(H, 500)

    scale_x = (svg_w - padding * 2) / max_real_w
    scale_y = (svg_h - padding * 2) / max_real_h
    scale = min(scale_x, scale_y)

    def to_svg(x, y):
        svg_x = padding + x * scale
        svg_y = (svg_h - padding) - y * scale
        return svg_x, svg_y

    svg_lines = []

    x_start, y_start = to_svg(-200, 0)
    x_floor_end, _ = to_svg(L + 200, 0)
    svg_lines.append(
        f'<line x1="{x_start}" y1="{y_start}" x2="{x_floor_end}" y2="{y_start}" '
        f'stroke="#94a3b8" stroke-width="2" stroke-dasharray="5,5" />'
    )

    step_color = "#3b82f6" if is_all_valid else "#ef4444"
    for i in range(N):
        x_curr = i * g_actual
        y_curr = i * h_actual

        sx, sy = to_svg(x_curr, y_curr)

        s_g = g_actual * scale
        s_h = h_actual * scale

        svg_lines.append(
            f'<line x1="{sx}" y1="{sy}" x2="{sx + s_g}" y2="{sy}" '
            f'stroke="{step_color}" stroke-width="4" stroke-linecap="round" />'
        )

        if i < N - 1:
            svg_lines.append(
                f'<line x1="{sx + s_g}" y1="{sy}" x2="{sx + s_g}" y2="{sy - s_h}" '
                f'stroke="#cbd5e1" stroke-width="1" stroke-dasharray="2,2" />'
            )

    x1_t, y1_t = to_svg(0, 0)
    x2_t, y2_t = to_svg(L, H - h_actual)
    svg_lines.append(
        f'<line x1="{x1_t}" y1="{y1_t}" x2="{x2_t}" y2="{y2_t}" '
        f'stroke="#1e293b" stroke-width="6" opacity="0.7" />'
    )

    x_h_line, y_h_bottom = to_svg(L + 100, 0)
    _, y_h_top = to_svg(L + 100, H)
    svg_lines.append(
        f'<line x1="{x_h_line}" y1="{y_h_bottom}" x2="{x_h_line}" y2="{y_h_top}" '
        f'stroke="#64748b" stroke-width="1.5" />'
    )
    svg_lines.append(
        f'<text x="{x_h_line + 10}" y="{(y_h_bottom + y_h_top) / 2}" '
        f'fill="#64748b" font-family="sans-serif" font-size="12">H = {H} mm</text>'
    )

    x_l_left, y_l_line = to_svg(0, -100)
    x_l_right, _ = to_svg(L, -100)
    svg_lines.append(
        f'<line x1="{x_l_left}" y1="{y_l_line}" x2="{x_l_right}" y2="{y_l_line}" '
        f'stroke="#64748b" stroke-width="1.5" />'
    )
    svg_lines.append(
        f'<text x="{(x_l_left + x_l_right) / 2 - 30}" y="{y_l_line + 15}" '
        f'fill="#64748b" font-family="sans-serif" font-size="12">L = {L:.0f} mm</text>'
    )

    x_a, y_a = to_svg(80, 20)
    svg_lines.append(
        f'<text x="{x_a}" y="{y_a}" fill="#0f172a" font-family="sans-serif" '
        f'font-weight="bold" font-size="14">{angle:.1f}°</text>'
    )

    svg_content = "\n".join(svg_lines)
    svg_wrapper = f"""
    <svg width="{svg_w}" height="{svg_h}" style="background-color: #f8fafc; border-radius: 8px; border: 1px solid #e2e8f0;">
        <defs>
            <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f1f5f9" stroke-width="1"/>
            </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />

        {svg_content}
    </svg>
    """

    st.subheader("Side View Drawing")
    st.components.v1.html(svg_wrapper, height=svg_h + 20)

    st.info(
        f"**Blondel formula:** calculated value is **{blondel:.1f} mm** "
        f"(ISO range: 600–660 mm)."
    )
