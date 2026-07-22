import math

import streamlit as st

st.set_page_config(page_title="ISO 14122-3 Stair Calculator", layout="wide")

st.title("Industrial Stair Calculator")
st.caption("Calculation and verification per ISO 14122-3 (Safety of machinery)")

col_sidebar, col_main = st.columns([1, 2])

with col_sidebar:
    st.header("Input Parameters")

    H = st.number_input(
        "Total rise height (H), mm", min_value=300, max_value=4000, value=1500, step=50,
    )

    Pd = st.number_input("Pd (vertical bottom offset), mm", min_value=0, max_value=1000, value=0, step=10)
    Pup = st.number_input("Pup (vertical top offset), mm", min_value=0, max_value=1000, value=0, step=10)

    edit_param = st.radio(
        "Edit parameter",
        ["Steps (N)", "L (horizontal)", "Desired angle (°)"],
        horizontal=True,
    )

    def solve_offsets(N_val, angle_deg):
        a_rad = math.radians(angle_deg)
        for _ in range(15):
            H_net = H - (Pd + Pup)
            h_val = H_net / N_val
            g_val = 630 - 2 * h_val
            if g_val < 50:
                g_val = 50
            a_rad = math.atan(h_val / g_val)
        return H - (Pd + Pup), h_val, g_val, math.degrees(a_rad)

    def offs_L(a_deg):
        a_r = math.radians(a_deg)
        return (Pd + Pup) / math.tan(a_r) if math.tan(a_r) > 0 else 0

    if edit_param == "Steps (N)":
        N = st.number_input(
            "Steps (N)", min_value=1, max_value=30, step=1, value=8, key="inp_n",
        )
        angle_init = math.degrees(math.atan((H / N) / max(630 - 2 * H / N, 50)))
        H_net, h_actual, g_actual, angle = solve_offsets(N, angle_init)
        L = g_actual * (N - 1) + offs_L(angle)
    elif edit_param == "L (horizontal)":
        if "inp_l_val" not in st.session_state:
            st.session_state["inp_l_val"] = 1000
        col_l1, col_l2 = st.columns([3, 1])
        with col_l1:
            st.slider(
                "L (horizontal), mm", min_value=100, max_value=5000, step=1,
                value=st.session_state["inp_l_val"], key="inp_l_slider",
            )
        with col_l2:
            st.number_input(
                "L (horizontal), mm", min_value=100, max_value=5000, step=1,
                value=st.session_state["inp_l_val"], key="inp_l_num",
                label_visibility="collapsed",
            )
        if st.session_state["inp_l_slider"] != st.session_state["inp_l_val"]:
            st.session_state["inp_l_val"] = st.session_state["inp_l_slider"]
        elif st.session_state["inp_l_num"] != st.session_state["inp_l_val"]:
            st.session_state["inp_l_val"] = st.session_state["inp_l_num"]
        L_desired = st.session_state["inp_l_val"]
        best_n = 1
        best_diff = float("inf")
        best_result = None
        for n_test in range(1, 31):
            angle_init = math.degrees(math.atan((H / n_test) / max(630 - 2 * H / n_test, 50)))
            H_net_t, h_t, g_t, a_t = solve_offsets(n_test, angle_init)
            L_t = g_t * (n_test - 1) + offs_L(a_t)
            diff = abs(L_t - L_desired)
            if diff < best_diff:
                best_diff = diff
                best_result = (n_test, H_net_t, h_t, g_t, a_t, L_t)
        N, H_net, h_actual, g_actual, angle, L = best_result
    else:
        if "inp_a_val" not in st.session_state:
            st.session_state["inp_a_val"] = 33.0
        col_a1, col_a2 = st.columns([3, 1])
        with col_a1:
            st.slider(
                "Desired angle (°)", min_value=20.0, max_value=75.0, step=0.1,
                value=st.session_state["inp_a_val"], key="inp_a_slider",
            )
        with col_a2:
            st.number_input(
                "Desired angle (°)", min_value=20.0, max_value=75.0, step=0.1,
                value=st.session_state["inp_a_val"], key="inp_a_num",
                format="%.1f", label_visibility="collapsed",
            )
        if st.session_state["inp_a_slider"] != st.session_state["inp_a_val"]:
            st.session_state["inp_a_val"] = st.session_state["inp_a_slider"]
        elif st.session_state["inp_a_num"] != st.session_state["inp_a_val"]:
            st.session_state["inp_a_val"] = st.session_state["inp_a_num"]
        angle_desired = st.session_state["inp_a_val"]
        a_rad = math.radians(angle_desired)
        H_net = H - (Pd + Pup)
        tan_a = math.tan(a_rad)
        g_approx = 630 / (1 + 2 * tan_a) if tan_a > 0 else 630
        N = max(1, min(round(H_net / ((630 - g_approx) / 2)), 30))
        h_actual = H_net / N
        g_actual = 630 - 2 * h_actual
        if g_actual < 50:
            g_actual = 50
        angle = math.degrees(math.atan(h_actual / g_actual))
        L = g_actual * (N - 1) + offs_L(angle_desired)

    st.markdown("---")
    if edit_param != "Steps (N)":
        st.number_input("Steps (N)", value=N, disabled=True, key="__dn")
    if edit_param != "L (horizontal)":
        st.number_input("L (horizontal), mm", value=round(L, 0), disabled=True, format="%.0f", key="__dl")
    if edit_param != "Desired angle (°)":
        st.number_input("Desired angle (°)", value=round(angle, 1), disabled=True, format="%.1f", key="__da")
    st.number_input("Riser (h), mm", value=round(h_actual, 1), disabled=True, format="%.1f", key="__dh")
    st.number_input("Tread (g), mm", value=round(g_actual, 1), disabled=True, format="%.1f", key="__dg")

    if edit_param == "L (horizontal)":
        l_dev = L_desired - L
        st.caption(f"Desired L: {L_desired:.0f} mm | Actual L: {L:.0f} mm | Δ = {l_dev:+.0f} mm")
        if N > 1:
            h_prev = H / (N - 1)
            g_prev = max(630 - 2 * h_prev, 50)
            l_prev = g_prev * (N - 2)
            st.caption(f"Try N={N-1} → L≈{l_prev:.0f} mm")
        if N < 30:
            h_next = H / (N + 1)
            g_next = max(630 - 2 * h_next, 50)
            l_next = g_next * N
            st.caption(f"Try N={N+1} → L≈{l_next:.0f} mm")
    elif edit_param == "Desired angle (°)":
        a_dev = angle_desired - angle
        st.caption(f"Desired angle: {angle_desired:.1f}° | Actual angle: {angle:.1f}° | Δ = {a_dev:+.1f}°")
        if N > 1:
            h_prev = H / (N - 1)
            g_prev = max(630 - 2 * h_prev, 50)
            a_prev = math.degrees(math.atan(h_prev / g_prev))
            st.caption(f"Try N={N-1} → angle≈{a_prev:.1f}°")
        if N < 30:
            h_next = H / (N + 1)
            g_next = max(630 - 2 * h_next, 50)
            a_next = math.degrees(math.atan(h_next / g_next))
            st.caption(f"Try N={N+1} → angle≈{a_next:.1f}°")

    W = st.slider("Stair width, mm", 400, 1200, 600)

    st.markdown("---")
    st.subheader("Step Offsets")
    angle_rad = math.radians(angle)
    Ad = Pd / math.sin(angle_rad) if math.sin(angle_rad) > 0 else 0
    Aup = Pup / math.sin(angle_rad) if math.sin(angle_rad) > 0 else 0
    st.number_input("Ad (along stair, bottom), mm", value=round(Ad, 1), disabled=True, format="%.1f")
    st.number_input("Aup (along stair, top), mm", value=round(Aup, 1), disabled=True, format="%.1f")

    if angle < 45:
        stair_type = "Stairs (20°–45°)"
        angle_min_ok, angle_max_ok = 20, 45
        g_min_ok = 200
        h_max_ok = 240
        w_min_ok = 600
        blondel_applies = True
    else:
        stair_type = "Stepladders (45°–75°)"
        angle_min_ok, angle_max_ok = 45, 75
        g_min_ok = 150
        h_max_ok = 250
        w_min_ok = 500
        blondel_applies = False

    blondel = g_actual + 2 * h_actual

    is_valid_blondel = 600 <= blondel <= 660 if blondel_applies else True
    is_valid_angle = angle_min_ok <= angle <= angle_max_ok
    is_valid_h = h_actual <= h_max_ok
    is_valid_g = g_actual >= g_min_ok
    is_valid_w = W >= w_min_ok

    is_all_valid = all(
        [is_valid_blondel, is_valid_angle, is_valid_h, is_valid_g, is_valid_w]
    )

with col_main:
    col_draw, col_metrics = st.columns([3, 1])

    with col_metrics:
        st.subheader("Parameters")
        st.metric("Steps (N)", f"{N}")
        st.metric("Riser (h)", f"{h_actual:.1f} mm")
        st.metric("Tread (g)", f"{g_actual:.1f} mm")
        if edit_param == "L (horizontal)":
            st.metric("Desired L", f"{L_desired:.0f} mm")
            st.metric("Actual L", f"{L:.0f} mm", delta=f"{L_desired - L:+.0f}")
        else:
            st.metric("L (horizontal)", f"{L:.0f} mm")
        if edit_param == "Desired angle (°)":
            st.metric("Desired angle", f"{angle_desired:.1f}°")
            st.metric("Actual angle", f"{angle:.1f}°", delta=f"{angle_desired - angle:+.1f}")
        else:
            st.metric("Angle (a)", f"{angle:.1f}°")

    with col_draw:
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

        a_rad_svg = math.radians(angle)
        x_off = (Pd / math.tan(a_rad_svg)) if a_rad_svg > 0 and math.tan(a_rad_svg) > 0 else 0

        step_color = "#3b82f6" if is_all_valid else "#ef4444"
        for i in range(N):
            x_curr = x_off + i * g_actual
            y_curr = Pd + i * h_actual

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

        x_last = x_off + (N - 1) * g_actual
        y_last = Pd + (N - 1) * h_actual
        x1_t, y1_t = to_svg(x_off, Pd)
        x2_t, y2_t = to_svg(x_last, y_last)
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

        if Pd > 0:
            px1, py1 = to_svg(x_off, 0)
            _, py2 = to_svg(x_off, Pd)
            svg_lines.append(
                f'<line x1="{px1}" y1="{py1}" x2="{px1}" y2="{py2}" '
                f'stroke="#f97316" stroke-width="2" />'
            )
            svg_lines.append(
                f'<text x="{px1 + 5}" y="{(py1 + py2) / 2}" fill="#f97316" '
                f'font-family="sans-serif" font-size="11">Pd = {Pd:.0f} mm</text>'
            )
        if Pup > 0:
            px1, py1 = to_svg(x_last + g_actual, H - Pup)
            _, py2 = to_svg(x_last + g_actual, H)
            svg_lines.append(
                f'<line x1="{px1}" y1="{py1}" x2="{px1}" y2="{py2}" '
                f'stroke="#f97316" stroke-width="2" />'
            )
            svg_lines.append(
                f'<text x="{px1 + 5}" y="{(py1 + py2) / 2}" fill="#f97316" '
                f'font-family="sans-serif" font-size="11">Pup = {Pup:.0f} mm</text>'
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

    if blondel_applies:
        st.info(
            f"**Blondel formula:** calculated value is **{blondel:.1f} mm** "
            f"(ISO range: 600–660 mm)."
        )

    st.markdown("---")
    st.subheader("Compliance")

    st.info(f"Detected type: **{stair_type}**")

    if is_all_valid:
        st.success("Fully complies with requirements!")
    else:
        st.error("Violations detected:")
        if not is_valid_angle:
            st.warning(
                f"Inclination angle {angle:.1f}° outside allowed range ({angle_min_ok}°–{angle_max_ok}°)."
            )
        if not is_valid_blondel:
            st.warning(
                f"Blondel formula {blondel:.0f} mm outside allowed range (600–660 mm)."
            )
        if not is_valid_g:
            st.warning(f"Tread depth {g_actual:.1f} mm too small (min. {g_min_ok} mm).")
        if not is_valid_h:
            st.warning(
                f"Riser height {h_actual:.1f} mm exceeds max allowed ({h_max_ok} mm)."
            )
        if not is_valid_w:
            st.warning(f"Stair width {W} mm below minimum ({w_min_ok} mm).")

st.markdown("---")
st.caption("Version: 1.6")
