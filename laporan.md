# Laporan Proyek Machine Learning - Damar Syarafi Ramadhan
### Latar Belakang
Industri ritel menghadapi tantangan besar dalam perencanaan stok dan pengelolaan inventori akibat dinamika tren musiman, perilaku konsumen, serta pengaruh promosi dan strategi pemasaran. Kemampuan memprediksi penjualan (sales forecasting) sangat penting untuk pengambilan keputusan bisnis yang efektif, seperti pengadaan barang, penentuan strategi promosi, dan manajemen rantai pasok. Penelitian Fildes et al. (2019) menunjukkan bahwa prediksi penjualan yang akurat dapat meningkatkan profitabilitas dan menurunkan biaya operasional. Integrasi data musiman dan pemasaran ke dalam model prediksi terbukti meningkatkan akurasi dibandingkan hanya menggunakan data historis penjualan.

Dataset yang digunakan, "Retail Sales Data with Seasonal Trends & Marketing" dari Kaggle, menyediakan data penjualan harian, tren musiman, dan aktivitas pemasaran—sangat relevan untuk membangun model time series forecasting yang mempertimbangkan faktor musiman dan promosi.

### Referensi:
1. R. Fildes, P. Goodwin, M. Lawrence, and K. Nikolopoulos, "Effective forecasting and judgmental adjustments: An empirical evaluation and strategies for improvement in supply-chain planning," International Journal of Forecasting, vol. 35, no. 1, pp. 227–237, 2019.
2. S. Makridakis, E. Spiliotis, and V. Assimakopoulos, "Statistical and Machine Learning forecasting methods: Concerns and ways forward," PLOS ONE, vol. 13, no. 3, p. e0194889, 2018.

## Business Understanding
Dataset yang digunakan dalam proyek ini adalah "Retail Sales Data with Seasonal Trends & Marketing" yang tersedia di Kaggle abdullah0a/retail-sales-data-with-seasonal-trends-and-marketing. Dataset ini menyediakan data penjualan harian, tren musiman, serta aktivitas pemasaran, sehingga sangat relevan untuk membangun model time series forecasting yang mempertimbangkan faktor-faktor musiman dan promosi.

### Problem Statements
1. Bagaimana memprediksi penjualan harian di masa depan dengan mempertimbangkan tren musiman dan aktivitas pemasaran?
2. Sejauh mana pengaruh fitur musiman dan pemasaran terhadap akurasi prediksi penjualan?

### Goals
1. Menghasilkan model time series forecasting yang mampu memprediksi penjualan harian secara akurat.
2. Mengidentifikasi fitur-fitur yang paling berpengaruh dalam meningkatkan akurasi prediksi penjualan.

### Solution statements
- Menggunakan berbagai algoritma regresi yang diaplikasikan untuk melakukan time series forecasting: Linear Regresi, Ridge, Lasso, ElasticNet, XGB Regressor, untuk membandingkan performa prediksi penjualan harian menggunakan metrik evaluasi RMSE (Root Mean Squared Error) dan MAE (Mean Absolute Error).

## Data Understanding
[Retail Sales Data with Seasonal Trends & Marketing](https://www.kaggle.com/datasets/abdullah0a/retail-sales-data-with-seasonal-trends-and-marketing).

Kumpulan data ini memberikan wawasan terperinci tentang penjualan eceran, yang menampilkan berbagai faktor yang memengaruhi kinerja penjualan. Kumpulan data ini mencakup catatan tentang pendapatan penjualan, unit yang terjual, persentase diskon, pengeluaran pemasaran, dan dampak tren musiman dan hari libur.

    Jumlah baris dan kolom dalam dataset : 30000 baris dan 11 kolom (fitur).

### Variabel-variabel pada Retail Sales Data with Seasonal Trends & Marketing dataset adalah sebagai berikut:
**Isi Dataset berisikan** :
- Store ID: Identifier toko jual.
- Product ID: Identifier per product.
- Sales Revenue (USD): Jumlah pendapatan yang didapat dari penjualan.
- Units Sold: Jumlah item produk terjual.
- Discount Percentage: Persentase Diskon yang dipasang pada produk tertentu.
- Marketing Spend (USD): Budget yang dikerahkan untuk promo marketing.
- Product Category: Kategori produk yang dijual (e.g., Electronics, Clothing).
- Date: Tanggal ketika penjualan terjadi.
- Store Location: Lokasi Geografis Toko.
- Day of the Week: Hari ketika penjualan terjadi.
- Holiday Effect: Indikator apakah penjualan terjadi selama periode liburan.

### Cek Nilai Null dan Duplicate
![Null Values](img/isna.png)
Dengan kode tersebut kita dapat menjumlahkan data null dan duplikat yang ada dalam data.
1. Duplicate() = Jumlah duplikat sebanyak 0 baris.
2. Isna() = Jumlah nilai null sebanyak 0 baris.

**Exploratory Data Analysis**:
- Visualisasi tren penjualan harian untuk mengidentifikasi pola musiman.

![Sales Trend](img/plot_eda1.png)

- Rata-rata Marketing untuk Masing Product

![Marketing Spends on Products](img/plot_eda2.png)

- Penjualan Produk Per Bulan (Berdasarkan Katalog Produk)

![Sales Revenue](img/plot_eda3A.png)

![Items Sold](img/plot_eda3B.png)

- Analisis korelasi antara fitur marketing_spend, promotion, season, dan sales.
![Feature Correlation](img/featurecorr.png)

## Data Preparation
1. Handling Missing Values dan Duplikat: Mengisi nilai kosong atau menghapus baris nilai kosong dan duplikat.
2. Label Encoding: Menerapkan Labelisasi pada feature categorical sebagai representasi numerik.
![Label Encoding](img/labelingb.png)

3. Scaling: Melakukan normalisasi pada fitur marketing_spend.
![Standardization](img/scaling.png)

4. Remove Outlier: 

5. Feature Engineering:
  - Ekstraksi fitur 'Date' yang memisahkan format date menjadi fitur : ['Day', 'Month','Year'].
  ![Month Sparsing](img/month.png)
  - Membuat fitur lag sales:
  ![Lag Sales](img/lagsales.png)
  *Lag* merupakan hal mendasar dalam pemodelan deret waktu karena banyak pola bergantung pada pengamatan sebelumnya. Misalnya, model autoregresif (AR) memprediksi nilai masa depan menggunakan kombinasi linier dari nilai masa lalu, di mana setiap suku dalam model sesuai dengan lag.

6. Train-Test Split: Membagi data menjadi data train dan test secara time series (Bagian data yang lebih awal digunakan untuk pelatihan, dan bagian data yang lebih akhir digunakan untuk pengujian).

### Variabel Utama:  
- **Target**: `Sales Revenue (USD)`  
- **Fitur**:  
  - `Units Sold`, `Discount Percentage`, `Marketing Spend (USD)`  
  - `Product Category` (kategori produk), `Date` (tanggal penjualan)  
  - `Holiday Effect` (indikator liburan), `Day of the Week` (hari dalam minggu) 

![Data Split](img/split.png)

## Modeling
![Models](img/models.png)
Setelah melakukan Train-Test Split, melakukan pendekatan dengan mencoba beberapa algoritma regresi yang berbeda untuk melihat mana yang berkinerja terbaik pada data.
Algoritma yang diimplementasikan untuk dievaluasi meliputi:
- **Linear Regression** : Dasar regresi yang menghubungkan fitur mempengaruhi target menggunakan persamaan linier, output seiring dengan perubahan input seperti hubungan jam belajar dengan hasil ujian.
- **Ridge Regression** : pengembangan dari linear regression dengan menambahkan regularisasi L2 pada fungsi loss-nya. Tujuannya untuk mengatasi masalah overfitting dan multikolinearitas dengan menambahkan penalti berupa kuadrat dari besaran koefisien regresi.
- **Lasso Regression** : Lasso Regression (Least Absolute Shrinkage and Selection Operator) juga merupakan pengembangan dari linear regression, tetapi menggunakan regularisasi L1. Lasso dapat mengecilkan beberapa koefisien regresi hingga nol, sehingga secara otomatis melakukan seleksi fitur.
- **ElasticNet Regression** : ElasticNet Regression menggabungkan regularisasi L1 (Lasso) dan L2 (Ridge) dalam satu model. Algoritma ini efektif untuk menangani dataset berdimensi tinggi, multikolinearitas, dan juga melakukan seleksi fitur. ElasticNet memungkinkan penyesuaian antara efek L1 dan L2 melalui parameter alpha, sehingga bisa menangani kasus di mana Lasso atau Ridge saja tidak optimal.
- **XGBRegressor** : XGBRegressor adalah algoritma regresi berbasis XGBoost (Extreme Gradient Boosting), yaitu teknik ensemble yang menggabungkan banyak pohon keputusan (decision tree) secara bertahap untuk meminimalkan error.



### Evaluation
### Mendefinisikan fungsi evaluate_model yang:
![Evaluation Metrics](img/evaluateFucntion.png)
- Menerima model, data pelatihan, dan data pengujian.
- Melatih model menggunakan data pelatihan (model.fit(X_train, y_train)).
- Melakukan prediksi pada data pengujian (model.predict(X_test)).
- Menghitung metrik evaluasi (r2_score dan mean_squared_error untuk mendapatkan RMSE).
- Mencetak hasilnya.
- Menyimpan hasilnya ke dalam daftar results.

Mengevaluasi setiap model menggunakan metrik R² dan RMSE.
R² mengukur seberapa baik model menjelaskan varians dalam data target (semakin dekat ke 1, semakin baik).
RMSE (Root Mean Squared Error) mengukur rata-rata besar kesalahan prediksi model dalam unit yang sama dengan target (semakin rendah, semakin baik).
Mencetak hasil evaluasi untuk setiap model.
Mengumpulkan hasil evaluasi dalam DataFrame results_df untuk perbandingan yang lebih mudah.


**---Ini adalah bagian akhir laporan---**