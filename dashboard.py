import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur tema seaborn
sns.set(style='darkgrid')

# Judul Dashboard
st.title("📊 Dashboard Analisis E-Commerce")

# Load data
df = pd.read_csv("all_data.csv.gz")

# Mengubah kolom tanggal
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# --- FILTER RENTANG WAKTU ---
st.sidebar.subheader("Filter Rentang Waktu")
min_date = df["order_purchase_timestamp"].min()
max_date = df["order_purchase_timestamp"].max()

start_date, end_date = st.sidebar.date_input(
    label="Pilih Rentang Waktu",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

main_df = df[(df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
             (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# --- VISUALISASI GRAFIK 1 (Versi groupby yang stabil) ---
st.subheader("Tren Jumlah Order per Bulan")

# Menggunakan groupby agar tidak error di Pandas versi baru
main_df["order_month"] = main_df["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
monthly_orders_df = main_df.groupby("order_month").agg({
    "order_id": "nunique"
}).reset_index()

monthly_orders_df.rename(columns={"order_month": "order_purchase_timestamp", "order_id": "order_count"}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_orders_df["order_purchase_timestamp"], monthly_orders_df["order_count"], marker='o', linewidth=2, color="#72BCD4")
ax.set_title("Jumlah Order per Bulan", fontsize=16)
plt.xticks(rotation=45)
st.pyplot(fig)

# --- VISUALISASI GRAFIK 2 ---
st.subheader("Top 5 Kategori Produk")
sum_order_items_df = main_df.groupby("product_category_name_english")["order_id"].count().reset_index()
sum_order_items_df.rename(columns={"order_id": "product_count"}, inplace=True)
top_products = sum_order_items_df.sort_values(by="product_count", ascending=False).head(5)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="product_count", y="product_category_name_english", data=top_products, palette="Blues_r", ax=ax)
st.pyplot(fig)

st.caption("Copyright © Dicoding Proyek Analisis Data 2026")
