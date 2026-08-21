import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load dataset (pastikan file all_data.csv ada di satu folder yang sama)
df = pd.read_csv("all_data.csv")

# Mengubah tipe data kolom tanggal agar bisa difilter
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# --- SIDEBAR (FILTER TANGGAL) ---
st.sidebar.header("Filter Data")

min_date = df['order_purchase_timestamp'].min()
max_date = df['order_purchase_timestamp'].max()

# Widget rentang tanggal
start_date, end_date = st.sidebar.date_input(
    label="Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter dataframe berdasarkan tanggal yang dipilih
main_df = df[
    (df['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & 
    (df['order_purchase_timestamp'] <= pd.to_datetime(end_date))
]

# --- HALAMAN UTAMA DASHBOARD ---
st.title("📊 E-Commerce Public Dataset Dashboard")
st.markdown("Dashboard ini menampilkan analisis performa penjualan kategori produk serta segmentasi pelanggan.")

# 1. Grafik Kategori Produk dengan Pendapatan Tertinggi
st.subheader("Top Kategori Produk Berdasarkan Pendapatan")
top_categories = main_df.groupby('product_category_name')['price'].sum().reset_index()
top_categories = top_categories.sort_values(by='price', ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='price', 
    y='product_category_name', 
    data=top_categories, 
    palette='Blues_r', 
    ax=ax
)
ax.set_title("5 Kategori Produk dengan Pendapatan Tertinggi")
ax.set_xlabel("Total Pendapatan")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

# 2. Grafik RFM Analysis (Contoh: Berdasarkan Monetary / Pelanggan Terbaik)
st.subheader("Top 5 Pelanggan Terbaik (RFM Analysis)")
top_customers = main_df.groupby('customer_id')['price'].sum().reset_index()
top_customers = top_customers.sort_values(by='price', ascending=False).head(5)

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(
    x='price', 
    y='customer_id', 
    data=top_customers, 
    palette='Greens_r', 
    ax=ax2
)
ax2.set_title("Top 5 Pelanggan Berdasarkan Nilai Belanja (Monetary)")
ax2.set_xlabel("Total Belanja")
ax2.set_ylabel("Customer ID")
st.pyplot(fig2)
