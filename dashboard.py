import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt

# Set konfigurasi halaman Streamlit
st.set_page_config(
    page_title="E-Commerce Public Data Analysis", 
    page_icon="📊", 
    layout="wide"
)

# ==========================================
# 1. LOAD DATA & CLEANING
# ==========================================
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    
    # Menghapus baris jika ada data penting yang kosong (NaN)
    df = df.dropna(subset=["order_purchase_timestamp", "product_category_name", "price", "customer_id"])
    
    # Mengubah kolom waktu menjadi datetime
    datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
    for col in datetime_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    df = df.sort_values(by="order_purchase_timestamp")
    df = df.reset_index(drop=True)
    return df

all_df = load_data()

# ==========================================
# 2. FILTER TANGGAL INTERAKTIF DI SIDEBAR
# ==========================================
st.sidebar.header("Filter Berdasarkan Waktu")

min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        value=[min_date.date(), max_date.date()],
        min_value=min_date.date(),
        max_value=max_date.date()
    )

main_df = all_df[(all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date) + pd.Timedelta(days=1))]

# ==========================================
# 3. KONTEN UTAMA DASHBOARD
# ==========================================
st.title("📊 E-Commerce Public Data Analysis Dashboard")
st.markdown("---")

# --- PERTANYAAN 1: Tertinggi dan Terendah ---
st.subheader("Pertanyaan 1: Kategori Produk dengan Pendapatan Tertinggi & Terendah")
st.markdown("*Kategori produk apa yang menghasilkan total pendapatan (revenue) tertinggi dan terendah?*")

# Hitung revenue per kategori
revenue_by_category = main_df.groupby("product_category_name").agg({
    "price": "sum"
}).rename(columns={"price": "total_revenue"}).sort_values(by="total_revenue", ascending=False).reset_index()

top_5_rev = revenue_by_category.head(5)
bottom_5_rev = revenue_by_category.tail(5).sort_values(by="total_revenue", ascending=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 🏆 Top 5 Kategori Pendapatan Tertinggi")
    fig, ax = plt.subplots(figsize=(8, 4))
    colors_top = ["#2C5282" if i == 0 else "#72BCD4" for i in range(len(top_5_rev))]
    sns.barplot(x="total_revenue", y="product_category_name", data=top_5_rev, palette=colors_top, ax=ax, hue="product_category_name", legend=False)
    ax.set_xlabel("Total Pendapatan (R$)")
    ax.set_ylabel("Kategori Produk")
    st.pyplot(fig)

with col2:
    st.markdown("##### ⚠️ Top 5 Kategori Pendapatan Terendah")
    fig, ax = plt.subplots(figsize=(8, 4))
    colors_bot = ["#C53030" if i == 0 else "#FEB2B2" for i in range(len(bottom_5_rev))]
    sns.barplot(x="total_revenue", y="product_category_name", data=bottom_5_rev, palette=colors_bot, ax=ax, hue="product_category_name", legend=False)
    ax.set_xlabel("Total Pendapatan (R$)")
    ax.set_ylabel("Kategori Produk")
    st.pyplot(fig)

st.info("**Insight:** Kategori produk tertinggi mendominasi pasar secara masif, sementara kategori terendah memiliki penjualan yang sangat minim dan perlu dievaluasi strategi pemasarannya.")

st.markdown("---")

# --- PERTANYAAN 2 (RFM ANALYSIS) ---
st.subheader("Pertanyaan 2: Analisis RFM (Top Pelanggan Berdasarkan Monetary)")
st.markdown("*Bagaimana performa segmentasi pelanggan berdasarkan analisis RFM dalam hal total nilai transaksi (monetary)?*")

recent_date = main_df["order_purchase_timestamp"].max() + dt.timedelta(days=1)
rfm_df = main_df.groupby("customer_id").agg({
    "order_purchase_timestamp": lambda x: (recent_date - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]
top_monetary = rfm_df.sort_values(by="monetary", ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 4))
colors_rfm = ["#2C5282" if i == 0 else "#72BCD4" for i in range(len(top_monetary))]
sns.barplot(y="monetary", x="customer_id", data=top_monetary, palette=colors_rfm, ax=ax, hue="customer_id", legend=False)
ax.set_title("Top 5 Customers by Monetary Value", fontsize=12, fontweight="bold")
ax.set_xlabel("Customer ID", fontsize=10)
ax.set_ylabel("Monetary (R$)", fontsize=10)
ax.tick_params(axis='x', rotation=15)
st.pyplot(fig)

st.info("**Insight:** Pelanggan dengan nilai monetary tertinggi memberikan kontribusi finansial yang signifikan bagi bisnis.")

st.markdown("---")
st.caption("Proyek Analisis Data Dicoding - Created with Streamlit")
