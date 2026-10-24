import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
 
st.set_page_config(page_title="Dashboard Penjualan Cafe", layout="wide")
 
PALET = ["#2A9D8F", "#E9C46A", "#F4A261", "#6D9DC5", "#8AB17D",
         "#E76F51", "#B5838D", "#264653", "#A8DADC"]
WARNA_UTAMA = "#2A9D8F"
WARNA_TEKS = "#1F2D3D" 
TINGGI_CHART = 900      
 
st.markdown(
    """
<style>
h1 {font-size: 3.6vw !important; color: #264653; line-height: 1.15; font-weight: 800;}
h3 {font-size: 2.6vw !important; color: #264653; margin-top: 2.5rem; font-weight: 700;}
 
/* KPI: teks boleh turun baris, angka nggak boleh kepotong */
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] div, [data-testid="stMetricLabel"] p {
    white-space: normal !important; overflow: visible !important; text-overflow: clip !important;
}
[data-testid="stMetricLabel"] p {font-size: 1.25vw !important; color: #3d4f57;}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] div {
    font-size: 3.2vw !important; color: #2A9D8F; font-weight: 700;
    overflow: visible !important; text-overflow: clip !important;
}
[data-testid="stCaptionContainer"] p {font-size: 1.2vw !important;}
[data-testid="stExpander"] summary p {font-size: 1.6vw !important; font-weight: 600;}
 
/* sidebar filter dibikin lebar dan gede */
section[data-testid="stSidebar"] {width: 26vw !important; min-width: 26vw !important;}
[data-testid="stSidebar"] h2 {font-size: 2.2vw !important;}
[data-testid="stSidebar"] label p {font-size: 1.5vw !important; font-weight: 600;}
[data-testid="stSidebar"] [data-baseweb="select"] > div {min-height: 3.2vw;}
[data-testid="stSidebar"] [data-baseweb="select"] * {font-size: 1.2vw !important;}
[data-testid="stSidebar"] [data-tag] {height: auto !important; padding: 0.25vw 0.7vw !important; max-width: none !important;}
[data-testid="stSidebar"] [data-tag] span {font-size: 1.2vw !important; max-width: none !important;}
[data-testid="stSidebar"] [data-tag] svg {width: 0.9vw !important; height: 0.9vw !important;}
[data-testid="stDateInputField"] {min-height: 3.2vw;}
[data-testid="stDateInputField"] span, [data-testid="stDateInputField"] input {font-size: 1.4vw !important;}
[data-testid="stSlider"] label p {font-size: 1.5vw !important; font-weight: 600;}
[data-testid="stSlider"] p {font-size: 1.2vw !important;}
 
/* tabel data transaksi */
[data-testid="stTable"] table {font-size: 1.15vw !important;}
[data-testid="stTable"] th {font-size: 1.15vw !important;}
</style>
""",
    unsafe_allow_html=True,
)
 
 
def tampilkan(fig, tinggi=TINGGI_CHART):
    fig.update_layout(
        height=tinggi,
        template="plotly_white",
        font=dict(size=UKURAN_FONT, color=WARNA_TEKS),
        margin=dict(l=110, r=40, t=50, b=110),
        legend=dict(font=dict(size=UKURAN_FONT)),
        hoverlabel=dict(font_size=UKURAN_FONT),
    )
    fig.update_xaxes(tickfont=dict(size=UKURAN_FONT, color=WARNA_TEKS),
                     title_font=dict(size=UKURAN_JUDUL_SUMBU, color=WARNA_TEKS))
    fig.update_yaxes(tickfont=dict(size=UKURAN_FONT, color=WARNA_TEKS),
                     title_font=dict(size=UKURAN_JUDUL_SUMBU, color=WARNA_TEKS))
 
    st.plotly_chart(fig, width="stretch", theme=None, config={"displayModeBar": False})
 
UKURAN_FONT = 32          
UKURAN_JUDUL_SUMBU = 36
 
@st.cache_data
def muat_data():
    lokasi_file = Path(__file__).parent / "data_clean.csv"
    df = pd.read_csv(lokasi_file, parse_dates=["Transaction Date"])
 
    kosong = df["Total Spent"].isna()
    df.loc[kosong, "Total Spent"] = df["Quantity"] * df["Price Per Unit"]
 
    df = df.dropna(subset=["Total Spent"]).copy()
 
    df["Bulan"] = df["Transaction Date"].dt.to_period("M").dt.to_timestamp()
    df["Hari"] = df["Transaction Date"].dt.day_name()
    return df
 
 
df = muat_data()
 
st.title("Dashboard Penjualan Cafe 2023")
st.markdown(
    """
<div style="font-size: 1.5vw; line-height: 1.7; color: #3d4f57; margin-bottom: 1.5rem;">
Dashboard ini menampilkan data transaksi sebuah cafe sepanjang tahun 2023
(dataset <b>Cafe Sales</b> dari Kaggle). Tiap baris adalah satu transaksi yang berisi
item yang dibeli, jumlah, harga, metode pembayaran, dan lokasi pembelian.
Pakai filter di sebelah kiri buat melihat data sesuai kebutuhan.
</div>
""",
    unsafe_allow_html=True,
)
 
st.sidebar.header("Filter Data")
 
pilihan_item = sorted(df["Item"].unique())
item_dipilih = st.sidebar.multiselect("Item", pilihan_item, default=pilihan_item)
 
pilihan_bayar = sorted(df["Payment Method"].unique())
bayar_dipilih = st.sidebar.multiselect("Metode Pembayaran", pilihan_bayar, default=pilihan_bayar)
 
pilihan_lokasi = sorted(df["Location"].unique())
lokasi_dipilih = st.sidebar.multiselect("Lokasi", pilihan_lokasi, default=pilihan_lokasi)
 
tgl_min = df["Transaction Date"].min().date()
tgl_max = df["Transaction Date"].max().date()
rentang = st.sidebar.date_input(
    "Rentang Tanggal", value=(tgl_min, tgl_max), min_value=tgl_min, max_value=tgl_max
)
 
if isinstance(rentang, tuple) and len(rentang) == 2:
    tgl_awal, tgl_akhir = rentang
else:
    tgl_awal, tgl_akhir = tgl_min, tgl_max
 
df_filter = df[
    df["Item"].isin(item_dipilih)
    & df["Payment Method"].isin(bayar_dipilih)
    & df["Location"].isin(lokasi_dipilih)
    & (df["Transaction Date"].dt.date >= tgl_awal)
    & (df["Transaction Date"].dt.date <= tgl_akhir)
]
 
st.sidebar.caption(f"Menampilkan {len(df_filter):,} dari {len(df):,} transaksi")
 
if df_filter.empty:
    st.warning("Nggak ada data yang cocok dengan filter. Coba longgarkan filternya.")
    st.stop()
 
total_penjualan = df_filter["Total Spent"].sum()
total_transaksi = df_filter["Transaction ID"].nunique()
rata_transaksi = total_penjualan / total_transaksi
total_item = df_filter["Quantity"].sum()
 
k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Penjualan", f"${total_penjualan:,.0f}")
k2.metric("Total Transaksi", f"{total_transaksi:,}")
k3.metric("Rata-rata per Transaksi", f"${rata_transaksi:,.2f}")
k4.metric("Total Item Terjual", f"{total_item:,.0f}")
 
st.divider()
 
st.subheader("Tren Penjualan Bulanan")
tren = df_filter.groupby("Bulan", as_index=False)["Total Spent"].sum()
fig_line = px.line(
    tren, x="Bulan", y="Total Spent", markers=True,
    labels={"Bulan": "Bulan (2023)", "Total Spent": "Total Penjualan ($)"},
    color_discrete_sequence=[WARNA_UTAMA],
)
fig_line.update_traces(
    line=dict(width=5), marker=dict(size=14),
    text=tren["Total Spent"].map(lambda x: f"${x:,.0f}"),
    mode="lines+markers+text", textposition="top center",
    textfont=dict(size=UKURAN_FONT - 4, color=WARNA_TEKS), cliponaxis=False,
)
 
fig_line.update_xaxes(dtick="M1", tickformat="%b")
fig_line.update_yaxes(tickprefix="$", tickformat=",.0f")
tampilkan(fig_line)
 
st.subheader("Penjualan per Item")
per_item = (
    df_filter.groupby("Item", as_index=False)["Total Spent"].sum()
    .sort_values("Total Spent", ascending=False)
)
 
peta_warna = {nama: PALET[i % len(PALET)] for i, nama in enumerate(per_item["Item"])}  
per_item = per_item.sort_values("Total Spent", ascending=True)
fig_bar = px.bar(
    per_item, x="Total Spent", y="Item", color="Item", orientation="h",
    labels={"Total Spent": "Total Penjualan ($)", "Item": ""},
    color_discrete_map=peta_warna,
)
fig_bar.update_layout(showlegend=False, margin=dict(l=20, r=160, t=50, b=110))
fig_bar.update_traces(
    texttemplate="$%{x:,.0f}", textposition="outside",
    textfont=dict(size=UKURAN_FONT, color=WARNA_TEKS), cliponaxis=False,
    hovertemplate="%{y}<br>$%{x:,.0f}<extra></extra>",
)
fig_bar.update_xaxes(tickprefix="$", tickformat="~s", range=[0, per_item["Total Spent"].max() * 1.25])
tampilkan(fig_bar, tinggi=950)
 
st.subheader("Proporsi Metode Pembayaran")
per_bayar = df_filter.groupby("Payment Method", as_index=False)["Total Spent"].sum()
fig_pie = px.pie(
    per_bayar, names="Payment Method", values="Total Spent", hole=0.3,
    color_discrete_sequence=PALET,
)
fig_pie.update_traces(
    textfont=dict(size=UKURAN_FONT + 4, color=WARNA_TEKS), textinfo="percent+label",
    textposition="inside", insidetextorientation="horizontal",
    marker=dict(line=dict(color="white", width=3)),
    hovertemplate="%{label}<br>$%{value:,.0f} (%{percent})<extra></extra>",
)
fig_pie.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(font=dict(size=UKURAN_FONT + 6), itemsizing="constant", yanchor="middle", y=0.5),
)
tampilkan(fig_pie, tinggi=1000)
 
st.subheader("Distribusi Nilai Transaksi")
batas = np.arange(0, 28, 2)
jumlah, _ = np.histogram(df_filter["Total Spent"], bins=batas)
data_hist = pd.DataFrame({"Tengah": batas[:-1] + 1, "Jumlah": jumlah})
fig_hist = px.bar(
    data_hist, x="Tengah", y="Jumlah",
    labels={"Tengah": "Nilai Transaksi ($)", "Jumlah": "Jumlah Transaksi"},
    color_discrete_sequence=["#6D9DC5"],
)
fig_hist.update_traces(
    width=1.88,
    text=[f"{j:,}" if j > 0 else "" for j in jumlah], textposition="outside",
    textfont=dict(size=UKURAN_FONT, color=WARNA_TEKS), cliponaxis=False,
    hovertemplate="$%{x:.0f} (+-1)<br>%{y:,} transaksi<extra></extra>",
)
fig_hist.update_xaxes(tickmode="linear", tick0=0, dtick=2, tickprefix="$", range=[0, 26])
tampilkan(fig_hist)
 
st.subheader("Heatmap Penjualan: Item x Hari")
urutan_hari = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
pivot = (
    df_filter.pivot_table(index="Item", columns="Hari", values="Total Spent", aggfunc="sum")
    .reindex(columns=urutan_hari)
    .fillna(0)
    .rename(columns={"Monday": "Senin", "Tuesday": "Selasa", "Wednesday": "Rabu", "Thursday": "Kamis",
                     "Friday": "Jumat", "Saturday": "Sabtu", "Sunday": "Minggu"})
)
fig_heat = px.imshow(
    pivot, text_auto=".0f", aspect="auto",
    color_continuous_scale=["#F2F9F7", "#CBE9E2", "#9BD6CA", "#66BFAE", "#3FA897"],
    labels={"color": "Penjualan ($)", "x": "Hari", "y": "Item"},
)
 
fig_heat.update_traces(textfont=dict(size=UKURAN_FONT, color="#12232E"), xgap=3, ygap=3)
fig_heat.update_coloraxes(colorbar=dict(tickfont=dict(size=UKURAN_FONT), title_font=dict(size=UKURAN_FONT)))
fig_heat.update_xaxes(tickangle=0)
tampilkan(fig_heat, tinggi=950)
 
st.subheader("Data Transaksi")
jumlah_baris = 20
tabel = (
    df_filter.drop(columns=["Bulan", "Hari"])
    .sort_values("Transaction Date")
    .head(jumlah_baris)
    .copy()
)
tabel["Transaction Date"] = tabel["Transaction Date"].dt.strftime("%Y-%m-%d")
tabel["Quantity"] = tabel["Quantity"].map(lambda x: "kosong" if pd.isna(x) else f"{x:.0f}")
tabel["Price Per Unit"] = tabel["Price Per Unit"].map(lambda x: "kosong" if pd.isna(x) else f"${x:.2f}")
tabel["Total Spent"] = tabel["Total Spent"].map(lambda x: f"${x:.2f}")
tabel = tabel.rename(columns={
    "Transaction ID": "ID Transaksi", "Quantity": "Jumlah", "Price Per Unit": "Harga Satuan",
    "Total Spent": "Total", "Payment Method": "Metode Bayar", "Location": "Lokasi",
    "Transaction Date": "Tanggal",
}).set_index("ID Transaksi")
st.table(tabel)
 
st.caption("Sumber data: Kaggle - Cafe Sales")