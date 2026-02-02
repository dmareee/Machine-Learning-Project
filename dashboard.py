import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Add a title
st.set_page_config(page_title="Amazon E-commerce Product Recommendation System",
                    page_icon=":shopping:",
                    initial_sidebar_state="expanded")

#Load data
@st.cache_data
def load_data(nrows):
    data = pd.read_csv('clean_df.csv', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

st.title("Mesin Sistem Rekomendasi Produk Platform E-commerce Amazon")

with st.expander('Data'):
  st.markdown("""
              Dataset Amazon Sales yang diambil dari Kaggle berisi informasi lengkap terkait produk dan ulasan pengguna, dengan struktur variabel sebagai berikut:
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
              - product_link: Link resmi produk di website Amazon""")
  st.write("Amazon items Raw Data")
  data = load_data(1000)
  amazon_items = data[["product_name", "category", "actual_price","discounted_price","rating","rating_count"]]
  amazon_items = amazon_items.drop_duplicates().reset_index(drop=True)
  st.dataframe(amazon_items)

def view_average_discount(data):
    category_disc = data.groupby('category')['discounted_price'].mean().reset_index()
    category_disc= category_disc.sort_values(by='discounted_price', ascending=False)
    # category_disc
    st.header(f'Rata-rata Harga Diskon Setiap Kategori Produk')
    st.bar_chart(category_disc, x='category', y='discounted_price', color='category')
view_average_discount(data)


#Feature Engineering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder


def compute_tfidf_matrix(data):
    # Dropping irrelevant Features
    drop_col = ['discounted_price', 'actual_price', 'discount_percentage', 'review_id', 'review_title',
                    'user_name', 'img_link', 'product_link']
    drop_df = data.drop(columns=drop_col)

    #Instantiate TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()

    # Melakukan perhitungan idf pada data cuisine
    tfidf_matrix = vectorizer.fit_transform(drop_df['category'])
    return drop_df, tfidf_matrix
drop_df, tfidf_matrix = compute_tfidf_matrix(data)

def cosine_similarity(tfidf_matrix):
    from sklearn.metrics.pairwise import cosine_similarity
    cosine_sim = cosine_similarity(tfidf_matrix)
    return cosine_sim
cosine_sim = cosine_similarity(tfidf_matrix)
# Membuat dataframe dari variabel cosine_sim dengan baris dan kolom berupa nama resto
cosine_sim_df = pd.DataFrame(cosine_sim, index=drop_df['product_name'], columns=drop_df['product_name'])
print('Shape:', cosine_sim_df.shape)

# Melihat similarity matrix pada setiap resto
cosine_sim_df.sample(5, axis=1).sample(10, axis=0)

def view_recommendation(model, product_name, num_recommendations):
    try:
        recommendations = model.get_recommendations(product_name, num_recommendations)
        st.write(f"Rekomendasi produk serupa untuk '{product_name}':")
        for i, rec in enumerate(recommendations):
            st.write(f"{i+1}. {rec}")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")