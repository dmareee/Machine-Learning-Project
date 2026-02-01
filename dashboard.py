import streamlit as st
import pandas as pd

def load_data():
  df = pd.read_csv("https://github.com/dmareee/Machine-Learning-Project/blob/laporan2/amazon.csv")
  df.head(5)

st.title("Mesin Sistem Rekomendasi Produk Platform E-commerce Amazon")

with st.expander('Data'):
  st.write("Raw Data")
  load_data()
