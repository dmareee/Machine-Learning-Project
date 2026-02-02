import streamlit as st
import pickle
import pandas as pd
import numpy as np

df = pd.read_csv('amazon.csv')

st.title("Mesin Sistem Rekomendasi Produk Platform E-commerce Amazon")

with st.expander('Data'):
  st.info("""Dataset Amazon Sales yang diambil dari Kaggle berisi informasi lengkap terkait produk dan ulasan pengguna, dengan struktur variabel sebagai berikut:
          - product_id: ID unik produk
          - product_name: Nama produk
          - category: Kategori produk
          - discounted_price: Harga produk setelah diskon
          - actual_price: Harga asli produk sebelum diskon
          - discount_percentage: Persentase diskon produk
          - rating: Rating rata-rata produk
          - rating_count: Jumlah pengguna yang memberikan rating
          - about_product: Deskripsi produk
          - user_id: ID pengguna yang memberikan review
          - user_name: Nama pengguna yang memberikan review
          - review_id: ID review pengguna
          - review_title: Judul singkat review
          - review_content: Isi review panjang
          - img_link: Link gambar produk
          - product_link: Link resmi produk di website Amazon
          """)
  st.write("Amazon items Raw Data")
  amazon_items = df[["product_name", "category", "actual_price","discount_percentage","rating","rating_count"]]
  amazon_items