import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime as dt

# Set konfigurasi halaman Streamlit
st.set_page_config(page_title="E-Commerce Dashboard", page_icon="📊", layout="wide")

# ==========================================
# 1. LOAD DATA DENGAN KODE PENGAMAN (.gz)
# ==========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("all_data.csv.gz")
    except FileNotFoundError:
        df = pd.read_csv("all_data.csv")
    return df

all_df = load_data()

# Mengubah kolom waktu menjadi datetime
datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
for col in datetime_columns:
    if col in all_df.columns:
        all_df[col] = pd.to_datetime(all_df[col])

all_df = all_df.sort_values(by="order_purchase_timestamp")
all_df = all_df.reset_index(drop=True)

# ==========================================
# 2. FILTER TANGGAL INTERAKTIF DI SIDEBAR
# ==========================================
st.sidebar.header("Filter Dashboard")

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

# --- PERTANYAAN 1: Kategori Produk dengan Pendapatan Tertinggi ---
st.subheader("1. Top 5 Kategori Produk dengan Pendapatan Tertinggi")

revenue_by_category = main_df.groupby("product_category_name").agg({
    "price": "sum"
}).rename(columns={"price": "total_revenue"}).sort_values(by="total_revenue", ascending=False).reset_index().head(5)

fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#2C5282" if i == 0 else "#72BCD4" for i in range(len(revenue_by_category))]

sns.barplot(
    x="total_revenue", 
    y="product_category_name", 
    data=revenue_by_category, 
    hue="product_category_name",
    palette=colors,
    legend=False,
    ax=ax
)
ax.set_title("Top 5 Kategori Produk Berdasarkan Total Pendapatan", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Pendapatan (R$)", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig)

# --- PERTANYAAN 2: Analisis RFM Pelanggan (Monetary) ---
st.subheader("2. Analisis RFM: Top Pelanggan Berdasarkan Monetary")

recent_date = main_df["order_purchase_timestamp"].max() + dt.timedelta(days=1)
rfm_df = main_df.groupby("customer_id").agg({
    "order_purchase_timestamp": lambda x: (recent_date - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]
top_monetary = rfm_df.sort_values(by="monetary", ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 5))
colors_rfm = ["#2C5282" if i == 0 else "#72BCD4" for i in range(len(top_monetary))]

sns.barplot(
    y="monetary", 
    x="customer_id", 
    data=top_monetary, 
    hue="customer_id",
    palette=colors_rfm,
    legend=False,
    ax=ax
)
ax.set_title("Top 5 Customers by Monetary Value", fontsize=14, fontweight="bold")
ax.set_xlabel("Customer ID (Top 5)", fontsize=12)
ax.set_ylabel("Monetary (R$)", fontsize=12)
ax.tick_params(axis='x', rotation=30)
st.pyplot(fig)

st.markdown("---")
st.caption("Proyek Analisis Data Dicoding - Created with Streamlit")
