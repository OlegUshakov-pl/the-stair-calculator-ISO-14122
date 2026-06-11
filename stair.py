import streamlit as st
import math

# Настройка страницы
st.set_page_config(page_title="ISO 14122-3 Stair Calculator", layout="wide")

st.title("📐 Интерактивный калькулятор промышленных лестниц")
st.caption("Расчет и верификация параметров согласно стандарту ISO 14122-3 (Безопасность машин)")

# --- МАКЕТ: ДВЕ КОЛОНКИ ---
col_sidebar, col_main = st.columns([1, 2])

with col_sidebar:
    st.header("⚙️ Исходные данные")
    
    # Ввод параметров пользователя
    H = st.number_input("Общая высота подъема (H), мм", min_value=300, max_value=4000, value=1500, step=50)
    h_target = st.slider("Желаемая высота ступени (h), мм", 140, 250, 180)
    W = st.slider("Ширина лестничного марша, мм", 600, 1200, 800)

    # --- МАТЕМАТИКА РАСЧЕТА ---
    # 1. Считаем количество ступеней (округление до ближайшего целого)
    N = round(H / h_target)
    if N == 0: N = 1
    
    # 2. Точная высота ступени
    h_actual = H / N
    
    # 3. Из формулы Блонделя (g + 2h = 630 мм) находим оптимальную проступь g
    g_actual = 630 - (2 * h_actual)
    
    # Защита от отрицательных или слишком маленьких значений проступи для формул
    if g_actual < 50: g_actual = 50 
    
    # 4. Угол наклона лестницы
    angle = math.degrees(math.atan(h_actual / g_actual))
    
    # 5. Полная длина заложения (проекция на пол)
    # Количество проступей на одну меньше, чем подъемов (верхняя ступень вровень с площадкой)
    L = g_actual * (N - 1) 

    # --- ВАЛИДАЦИЯ ISO 14122-3 ---
    blondel = g_actual + 2 * h_actual
    is_valid_blondel = 600 <= blondel <= 660
    is_valid_angle = 30 <= angle <= 38
    is_valid_h = h_actual <= 250
    is_valid_g = g_actual >= 200
    is_valid_w = W >= 600

    is_all_valid = all([is_valid_blondel, is_valid_angle, is_valid_h, is_valid_g, is_valid_w])

    # --- ВЫВОД СТАТУСА ВАЛИДАЦИИ ---
    st.markdown("---")
    st.subheader("Проверка ISO 14122-3")
    
    if is_all_valid:
        st.success("✅ Лестница полностью соответствует стандарту!")
    else:
        st.error("❌ Есть нарушения требований стандарта:")
        if not is_valid_angle:
            st.warning(f"Угол наклона {angle:.1f}° вне нормы (30°–38°).")
        if not is_valid_blondel:
            st.warning(f"Формула шага {blondel:.0f} мм вне нормы (600–660 мм).")
        if not is_valid_g:
            st.warning(f"Глубина проступи {g_actual:.1f} мм слишком мала (мин. 200 мм).")

with col_main:
    # --- БЛОК С РЕЗУЛЬТАТАМИ (METRICS) ---
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Ступеней (N)", f"{N} шт")
    m_col2.metric("Высота шага (h)", f"{h_actual:.1f} мм")
    m_col3.metric("Проступь (g)", f"{g_actual:.1f} мм")
    m_col4.metric("Угол наклона", f"{angle:.1f}°")

    # --- ГЕНЕРАЦИЯ ДИНАМИЧЕСКОГО SVG ---
    # Настроим масштабирование, чтобы рисунок вписывался в область 800x500
    svg_w = 800
    svg_h = 500
    padding = 50
    
    # Масштабные коэффициенты, чтобы вписать лестницу в размеры SVG
    max_real_w = max(L, 500)
    max_real_h = max(H, 500)
    
    scale_x = (svg_w - padding * 2) / max_real_w
    scale_y = (svg_h - padding * 2) / max_real_h
    scale = min(scale_x, scale_y) # сохраняем пропорции 1:1

    # Функция перевода реальных координат (мм) в координаты SVG
    # Точка (0,0) лестницы — это левый нижний угол (начало подъема)
    def to_svg(x, y):
        svg_x = padding + x * scale
        svg_y = (svg_h - padding) - y * scale
        return svg_x, svg_y

    # Начинаем собирать строки SVG
    svg_lines = []
    
    # 1. Сетка/Пол и верхняя площадка
    x_start, y_start = to_svg(-200, 0)
    x_floor_end, _ = to_svg(L + 200, 0)
    svg_lines.append(f'<line x1="{x_start}" y1="{y_start}" x2="{x_floor_end}" y2="{y_start}" stroke="#94a3b8" stroke-width="2" stroke-dasharray="5,5" />')
    
    # 2. Отрисовка ступеней
    step_color = "#3b82f6" if is_all_valid else "#ef4444"
    for i in range(N):
        # Текущая координата угла ступени
        x_curr = i * g_actual
        y_curr = i * h_actual
        
        # Конвертируем в SVG
        sx, sy = to_svg(x_curr, y_curr)
        
        # Длина проступи на чертеже
        s_g = g_actual * scale
        s_h = h_actual * scale
        
        # Рисуем горизонтальную линию ступени
        svg_lines.append(f'<line x1="{sx}" y1="{sy}" x2="{sx + s_g}" y2="{sy}" stroke="{step_color}" stroke-width="4" stroke-linecap="round" />')
        
        # Рисуем вертикальный пунктир подступенка (высоту шага), если это не земля
        if i < N - 1:
            svg_lines.append(f'<line x1="{sx + s_g}" y1="{sy}" x2="{sx + s_g}" y2="{sy - s_h}" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="2,2" />')

    # 3. Несущая тетива (основание косоура) — линия от первой ступени до последней
    x1_t, y1_t = to_svg(0, 0)
    x2_t, y2_t = to_svg(L, H - h_actual)
    svg_lines.append(f'<line x1="{x1_t}" y1="{y1_t}" x2="{x2_t}" y2="{y2_t}" stroke="#1e293b" stroke-width="6" opacity="0.7" />')

    # 4. Размеры и выноски
    # Выноска общей высоты H
    x_h_line, y_h_bottom = to_svg(L + 100, 0)
    _, y_h_top = to_svg(L + 100, H)
    svg_lines.append(f'<line x1="{x_h_line}" y1="{y_h_bottom}" x2="{x_h_line}" y2="{y_h_top}" stroke="#64748b" stroke-width="1.5" />')
    svg_lines.append(f'<text x="{x_h_line + 10}" y="{(y_h_bottom + y_h_top)/2}" fill="#64748b" font-family="sans-serif" font-size="12">H = {H} мм</text>')

    # Выноска общей длины L
    x_l_left, y_l_line = to_svg(0, -100)
    x_l_right, _ = to_svg(L, -100)
    svg_lines.append(f'<line x1="{x_l_left}" y1="{y_l_line}" x2="{x_l_right}" y2="{y_l_line}" stroke="#64748b" stroke-width="1.5" />')
    svg_lines.append(f'<text x="{(x_l_left + x_l_right)/2 - 30}" y="{y_l_line + 15}" fill="#64748b" font-family="sans-serif" font-size="12">L = {L:.0f} мм</text>')
    
    # Отрисовка дуги угла наклона (упрощенно в виде текста рядом с началом)
    x_a, y_a = to_svg(80, 20)
    svg_lines.append(f'<text x="{x_a}" y="{y_a}" fill="#0f172a" font-family="sans-serif" font-weight="bold" font-size="14">{angle:.1f}°</text>')

    # Собираем всё в единый SVG тег
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

    # Выводим рисунок в Streamlit
    st.subheader("📊 Чертеж марша (вид сбоку)")
    st.components.v1.html(svg_wrapper, height=svg_h + 20)
    
    # Дополнительная техническая информация
    st.info(f"💡 **Справочно (Формула Блонделя):** значение расчета равно **{blondel:.1f} мм** (норма по ISO: 600–660 мм).")