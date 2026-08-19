
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("📊 Dashboard Analisis E-Commerce")

# Load data
df = pd.read_csv("all_data.csv.gz")
st.subheader("Data Keseluruhan")
st.write(df.head())

# Contoh visualisasi sederhana
st.subheader("Visualisasi")
# Tambahkan grafik sesuai hasil analisis di notebook kamu
