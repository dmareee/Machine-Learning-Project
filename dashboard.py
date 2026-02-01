import streamlit as st
import pandas as pd

df = pd.read_csv('amazon.csv')

st.title("Mesin Sistem Rekomendasi Produk Platform E-commerce Amazon")

with st.expander('Data'):
  st.write("Raw Data")
  df
