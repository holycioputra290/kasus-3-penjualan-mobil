import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title='Car Industry Analytics 2025 | Apple UI',
    page_icon='🚗',
    layout='wide',
    initial_sidebar_state='expanded',
)

# 2. Sidebar: Switcher Theme Mode
st.sidebar.markdown('### 🎨 Pengaturan Tema')
theme_mode = st.sidebar.radio(
    "Pilih Mode Tampilan:",
    options=["Terang (Light Mode) ☀️", "Gelap (Dark Mode) 🌙"],
    index=0
)
st.sidebar.markdown('---')

is_dark = "Gelap" in theme_mode

# 3. Dynamic Custom CSS (Apple UI Design System)
bg_color = "#16181D" if is_dark else "#F5F5F7"
text_primary = "#FFFFFF" if is_dark else "#1D1D1F"
text_secondary = "#A0A5B5" if is_dark else "#86868B"
sidebar_bg = "#21252D" if is_dark else "rgba(255, 255, 255, 0.85)"
card_bg = "#242832" if is_dark else "#FFFFFF"
card_border = "rgba(255, 255, 255, 0.12)" if is_dark else "rgba(0, 0, 0, 0.04)"
grid_color = "rgba(255, 255, 255, 0.08)" if is_dark else "#F0F0F2"

st.markdown(
    f"""
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", Helvetica, Arial, sans-serif !important;
        color: {text_primary} !important;
    }}
    .apple-header {{
        font-weight: 700;
        font-size: 2.2rem;
        letter-spacing: -0.03em;
        color: {text_primary};
        margin-bottom: 4px;
    }}
    .apple-subtitle {{
        font-weight: 400;
        font-size: 1.05rem;
        color: {text_secondary};
        letter-spacing: -0.01em;
        margin-bottom: 24px;
    }}
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid {card_border} !important;
    }}
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] h3 {{
        color: {text_primary} !important;
    }}
    .apple-card {{
        background: {card_bg};
        border-radius: 20px;
        padding: 22px 24px;
        border: 1px solid {card_border};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: transform 0.3s cubic-bezier(0.25, 1, 0.5, 1), box-shadow 0.3s cubic-bezier(0.25, 1, 0.5, 1);
        margin-bottom: 16px;
    }}
    .apple-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
    }}
    .metric-label {{
        font-size: 0.82rem;
        font-weight: 600;
        color: {text_secondary};
        letter-spacing: 0.03em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .metric-value {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {text_primary};
        letter-spacing: -0.03em;
    }}
    .chart-box {{
        background: {card_bg};
        border-radius: 24px;
        padding: 24px;
        border: 1px solid {card_border};
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
    }}
    .chart-title {{
        font-size: 1.15rem;
        font-weight: 600;
        color: {text_primary};
        letter-spacing: -0.02em;
        margin-bottom: 12px;
    }}
    .streamlit-expanderHeader {{
        background-color: {card_bg} !important;
        border-radius: 12px !important;
        border: 1px solid {card_border} !important;
        color: {text_primary} !important;
    }}
    .stExpander p, .stExpander li {{
        color: {text_primary} !important;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""",
    unsafe_allow_html=True,
)

# 4. Load Data Kasus 3 (Mendukung Cars Datasets 2025.csv & dataset_penjualan_mobil.csv)
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('Cars Datasets 2025.csv', encoding='latin1')
    except FileNotFoundError:
        data = pd.read_csv('dataset_penjualan_mobil.csv', encoding='latin1')
    
    # Konversi aman kolom Seats menjadi numeric
    if 'Seats' in data.columns:
        data['Seats_Num'] = pd.to_numeric(data['Seats'], errors='coerce')
    else:
        data['Seats_Num'] = None
        
    return data

df = load_data()

# 5. Header Section
st.markdown(
    '<div class="apple-header">Dashboard Analisis Industri Mobil 2025</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="apple-subtitle">Eksplorasi Spesifikasi & Performa Mobil Global • Bedah Kasus 3</div>',
    unsafe_allow_html=True,
)

# 6. Sidebar Filter
st.sidebar.markdown('### 🎛️ Filter Data')

list_company = sorted(df['Company Names'].dropna().astype(str).unique().tolist())
selected_company = st.sidebar.multiselect(
    'Pilih Pabrikan (Brand):',
    options=list_company,
    default=list_company[:10] if len(list_company) > 10 else list_company,
)

list_fuel = sorted(df['Fuel Types'].dropna().astype(str).unique().tolist())
selected_fuel = st.sidebar.multiselect(
    'Tipe Bahan Bakar:',
    options=list_fuel,
    default=list_fuel,
)

# Filtering Data
filtered_df = df[
    (df['Company Names'].astype(str).isin(selected_company))
    & (df['Fuel Types'].astype(str).isin(selected_fuel))
]

# 7. Apple KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

total_models = len(filtered_df)
total_brands = filtered_df['Company Names'].nunique()
unique_fuels = filtered_df['Fuel Types'].nunique()
avg_seats = filtered_df['Seats_Num'].mean() if len(filtered_df) > 0 and 'Seats_Num' in filtered_df.columns and not filtered_df['Seats_Num'].isna().all() else 0

col1.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Total Model Mobil</div>
        <div class="metric-value">{total_models:,}</div>
    </div>
""",
    unsafe_allow_html=True,
)

col2.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Jumlah Pabrikan</div>
        <div class="metric-value">{total_brands:,} Brand</div>
    </div>
""",
    unsafe_allow_html=True,
)

col3.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Variasi Bahan Bakar</div>
        <div class="metric-value">{unique_fuels} Tipe</div>
    </div>
""",
    unsafe_allow_html=True,
)

col4.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Rata-rata Tempat Duduk</div>
        <div class="metric-value">{avg_seats:.1f} Seats</div>
    </div>
""",
    unsafe_allow_html=True,
)

APPLE_COLORS = ['#0071E3', '#34C759', '#FF9500', '#AF52DE', '#FF2D55', '#5856D6', '#64D2FF']

# 8. Chart Row 1
row1_col1, row1_col2 = st.columns([1.6, 1])

with row1_col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📊 Top Pabrikan dengan Model Terbanyak</div>', unsafe_allow_html=True)

    top_brands = (
        filtered_df['Company Names'].value_counts().nlargest(10).reset_index()
    )
    top_brands.columns = ['Pabrikan', 'Jumlah Model']

    fig_bar = px.bar(
        top_brands,
        x='Jumlah Model',
        y='Pabrikan',
        orientation='h',
        color='Jumlah Model',
        color_continuous_scale=['#64D2FF', '#0071E3'],
        text_auto=True,
    )
    fig_bar.update_traces(marker_cornerradius=6)
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        coloraxis_showscale=False,
        yaxis=dict(autorange='reversed', title='', tickfont=dict(color=text_primary, size=11)),
        xaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11))
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🍕 Proporsi Tipe Bahan Bakar</div>', unsafe_allow_html=True)

    fuel_df = filtered_df['Fuel Types'].value_counts().nlargest(6).reset_index()
    fuel_df.columns = ['Bahan Bakar', 'Jumlah']

    fig_pie = px.pie(
        fuel_df,
        names='Bahan Bakar',
        values='Jumlah',
        hole=0.65,
        color_discrete_sequence=APPLE_COLORS,
    )
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#FFFFFF', width=2)),
    )
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 9. Chart Row 2
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">💺 Distribusi Kapasitas Tempat Duduk (Seats)</div>', unsafe_allow_html=True)

    fig_hist = px.histogram(
        filtered_df,
        x='Seats',
        color_discrete_sequence=['#34C759'],
        text_auto=True,
    )
    fig_hist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, title='Jumlah Seats', tickfont=dict(color=text_primary, size=11)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, title='Jumlah Model', tickfont=dict(color=text_secondary, size=11)),
        showlegend=False,
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">⚡ Tipe Mesin Terbanyak</div>', unsafe_allow_html=True)

    engine_df = filtered_df['Engines'].value_counts().nlargest(8).reset_index()
    engine_df.columns = ['Tipe Mesin', 'Jumlah']

    fig_engine = px.bar(
        engine_df,
        x='Tipe Mesin',
        y='Jumlah',
        color_discrete_sequence=['#AF52DE'],
        text_auto=True,
    )
    fig_engine.update_traces(marker_cornerradius=8)
    fig_engine.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, title='', tickfont=dict(color=text_primary, size=10)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11))
    )
    st.plotly_chart(fig_engine, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 10. Tabel Data Expander
with st.expander('📋 Detail Spesifikasi Mobil Global 2025 (Terfilter)'):
    show_df = filtered_df.drop(columns=['Seats_Num'], errors='ignore')
    st.dataframe(show_df, use_container_width=True)
