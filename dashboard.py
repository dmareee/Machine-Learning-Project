import streamlit as st
import pandas as pd

df = pd.read_csv('amazon.csv')

st.title("Mesin Sistem Rekomendasi Produk Platform E-commerce Amazon")

with st.expander('Data'):
  st.write("Amazon items Raw Data")
  amazon_items = df[["product_name", "category", "actual_price","discount_percentage","rating","rating_count"]]
  amazon_items