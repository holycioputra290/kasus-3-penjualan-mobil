import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title='Car Sales Analytics | Apple UI',
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

# 4. Load Data Kasus 3 (Mobil)
@st.cache_data
def load_data():
    data = pd.read_csv('dataset_penjualan_mobil.csv')
    data['Tanggal'] = pd.to_datetime(data['Tanggal'])
    return data.sort_values('Tanggal')

df = load_data()

# 5. Header Section
st.markdown(
    '<div class="apple-header">Dashboard Penjualan Mobil Terlaris di Indonesia</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="apple-subtitle">Analisis Operasional & Tren Industri Otomotif Mobil • Bedah Kasus 3</div>',
    unsafe_allow_html=True,
)

# 6. Sidebar Filter
st.sidebar.markdown('### 🎛️ Filter Data')

min_date = df['Tanggal'].min().date()
max_date = df['Tanggal'].max().date()

date_range = st.sidebar.date_input(
    'Rentang Tanggal',
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

selected_kategori = st.sidebar.multiselect(
    'Kategori Mobil',
    options=df['Kategori'].unique(),
    default=df['Kategori'].unique(),
)

selected_produk = st.sidebar.multiselect(
    'Pilih Model Mobil',
    options=df[df['Kategori'].isin(selected_kategori)]['Produk'].unique(),
    default=df[df['Kategori'].isin(selected_kategori)]['Produk'].unique(),
)

# Terapkan Filter
if len(date_range) == 2:
    start_d, end_d = date_range
    filtered_df = df[
        (df['Tanggal'].dt.date >= start_d)
        & (df['Tanggal'].dt.date <= end_d)
        & (df['Kategori'].isin(selected_kategori))
        & (df['Produk'].isin(selected_produk))
    ]
else:
    filtered_df = df[
        (df['Kategori'].isin(selected_kategori))
        & (df['Produk'].isin(selected_produk))
    ]

# 7. Apple KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

total_revenue = filtered_df['Total Penjualan (Rp)'].sum()
total_units = filtered_df['Jumlah Terjual'].sum()
avg_transaction = filtered_df['Total Penjualan (Rp)'].mean() if len(filtered_df) > 0 else 0
total_tx = len(filtered_df)

col1.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Total Pendapatan</div>
        <div class="metric-value">Rp {total_revenue/1e12:,.2f}T</div>
    </div>
""",
    unsafe_allow_html=True,
)

col2.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Total Mobil Terjual</div>
        <div class="metric-value">{total_units:,} Unit</div>
    </div>
""",
    unsafe_allow_html=True,
)

col3.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Rata-rata Transaksi</div>
        <div class="metric-value">Rp {avg_transaction/1e6:,.1f}Jt</div>
    </div>
""",
    unsafe_allow_html=True,
)

col4.markdown(
    f"""
    <div class="apple-card">
        <div class="metric-label">Jumlah Transaksi</div>
        <div class="metric-value">{total_tx:,}</div>
    </div>
""",
    unsafe_allow_html=True,
)

APPLE_COLORS = ['#0071E3', '#34C759', '#FF9500', '#AF52DE', '#FF2D55', '#5856D6', '#64D2FF']

# 8. Chart Row 1
row1_col1, row1_col2 = st.columns([1.6, 1])

with row1_col1:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Tren Penjualan Mobil Harian</div>', unsafe_allow_html=True)

    trend_df = (
        filtered_df.groupby('Tanggal')['Total Penjualan (Rp)']
        .sum()
        .reset_index()
    )

    fig_line = px.line(
        trend_df,
        x='Tanggal',
        y='Total Penjualan (Rp)',
        labels={'Total Penjualan (Rp)': 'Pendapatan (Rp)'},
    )
    fig_line.update_traces(line_color='#0071E3', line_width=3, line_shape='spline')
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, title='', tickfont=dict(color=text_secondary, size=11)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11)),
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🍕 Proporsi Kategori Mobil</div>', unsafe_allow_html=True)

    fig_pie = px.pie(
        filtered_df,
        names='Kategori',
        values='Total Penjualan (Rp)',
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
    st.markdown('<div class="chart-title">📊 Total Terjual per Model Mobil</div>', unsafe_allow_html=True)

    prod_df = (
        filtered_df.groupby(['Produk', 'Kategori'])['Jumlah Terjual']
        .sum()
        .reset_index()
    )

    fig_bar = px.bar(
        prod_df,
        x='Produk',
        y='Jumlah Terjual',
        color='Kategori',
        color_discrete_sequence=APPLE_COLORS,
        text_auto=True,
    )
    fig_bar.update_traces(marker_cornerradius=8)
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, title='', tickfont=dict(color=text_primary, size=11)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11)),
        showlegend=False,
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2_col2:
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🏷️ Distribusi Harga Mobil</div>', unsafe_allow_html=True)

    fig_hist = px.histogram(
        filtered_df,
        x='Harga (Rp)',
        color='Kategori',
        nbins=25,
        color_discrete_sequence=APPLE_COLORS,
        opacity=0.85,
    )
    fig_hist.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_primary, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, title='', tickfont=dict(color=text_secondary, size=11)),
        yaxis=dict(showgrid=True, gridcolor=grid_color, title='', tickfont=dict(color=text_secondary, size=11)),
        showlegend=False,
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 10. Tabel Data Expander
with st.expander('📋 Detail Data Penjualan Mobil (Terfilter)'):
    st.dataframe(filtered_df, use_container_width=True)