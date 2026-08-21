import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='darkgrid')

# Judul Dashboard
st.title("📊 Dashboard Analisis E-Commerce")

# Load data (menggunakan format .gz sesuai file kamu)
df = pd.read_csv("all_data.csv.gz")

# Mengubah kolom tanggal menjadi datetime agar bisa difilter
datetime_columns = ["order_purchase_timestamp"]
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

# --- 1. MEMBUAT FILTER RENTANG WAKTU DI SIDEBAR (Interaktif) ---
st.sidebar.subheader("Filter Rentang Waktu")

min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()

start_date, end_date = st.sidebar.date_input(
    label="Pilih Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter dataframe berdasarkan tanggal yang dipilih
main_df = df[(df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
             (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]


# --- 2. VISUALISASI GRAFIK 1: PERFORMA PENJUALAN BULANAN ---
st.subheader("Tren Jumlah Order per Bulan")

monthly_orders_df = main_df.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "payment_value": "sum"
}).reset_index()
monthly_orders_df.rename(columns={
    "order_id": "order_count",
    "payment_value": "revenue"
}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    monthly_orders_df["order_purchase_timestamp"],
    monthly_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#72BCD4"
)
ax.set_title("Jumlah Order per Bulan", fontsize=16)
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total Order", fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig)


# --- 3. VISUALISASI GRAFIK 2: KATEGORI PRODUK TERBAIK/TERBURUK ---
st.subheader("Performa Kategori Produk")

sum_order_items_df = main_df.groupby("product_category_name_english")["order_id"].count().reset_index()
sum_order_items_df.rename(columns={"order_id": "product_count"}, inplace=True)
top_products = sum_order_items_df.sort_values(by="product_count", ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="product_count",
    y="product_category_name_english",
    data=top_products,
    palette="Blues_r",
    ax=ax
)
ax.set_title("Top 5 Kategori Produk dengan Penjualan Terbanyak", fontsize=16)
ax.set_xlabel("Jumlah Terjual", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig)

# Catatan kaki penutup
st.caption("Copyright © Dicoding Proyek Analisis Data 2026")
