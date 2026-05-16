# 🛒 Brazilian E-Commerce Analytics Dashboard

Proyek analisis data untuk submission Belajar Fundamental Analisis Data — Dicoding.

## 📂 Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv          # Dataset bersih untuk dashboard
│   ├── rfm_data.csv           # Data hasil RFM Analysis
│   └── dashboard.py           # Aplikasi Streamlit
├── data/
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_customers_dataset.csv
│   ├── olist_sellers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   └── product_category_name_translation.csv
├── notebook.ipynb             # Notebook analisis lengkap
├── requirements.txt           # Daftar library
├── README.md                  # File ini
└── url.txt                    # URL Streamlit Cloud (setelah deploy)
```

## 🗂️ Dataset

Dataset yang digunakan adalah **Brazilian E-Commerce Public Dataset by Olist** yang dapat diunduh dari:
- [Google Drive (Dicoding)](https://drive.google.com/file/d/1MsAjPM7oKtVfJL_wRp1qmCajtSG1mdcK/view?usp=sharing)
- [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

Setelah mengunduh, ekstrak semua file `.csv` ke dalam folder `data/`.

## 🔧 Setup Environment

### Menggunakan pip (Virtual Environment)

```bash
# 1. Clone atau ekstrak folder submission
cd submission

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Menggunakan Conda

```bash
conda create --name olist-dashboard python=3.9
conda activate olist-dashboard
pip install -r requirements.txt
```

## ▶️ Menjalankan Dashboard

Pastikan Anda sudah berada di folder `submission/` dan virtual environment sudah aktif.

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka di browser pada alamat:
```
http://localhost:8501
```

## 📊 Menjalankan Notebook

Pastikan Jupyter sudah terinstall, lalu jalankan:

```bash
jupyter notebook notebook.ipynb
```

Atau buka di Google Colab dan upload file dataset-nya.

> ⚠️ **Penting**: Jalankan seluruh cell notebook dari atas ke bawah secara berurutan. Pastikan semua file CSV sudah ada di folder `data/` sebelum menjalankan.

## ❓ Pertanyaan Bisnis yang Dijawab

1. **Kategori produk terlaris** — Kategori mana yang menghasilkan revenue dan volume order tertinggi? Bagaimana tren penjualannya?

2. **Delivery time & kepuasan pelanggan** — Bagaimana pengaruh lama pengiriman terhadap review score pelanggan? Kategori mana yang paling berisiko?

3. **Segmentasi pelanggan (RFM)** — Bagaimana profil pelanggan berdasarkan Recency, Frequency, dan Monetary? Segmen mana yang paling bernilai?

## 🌐 Streamlit Cloud Deployment

URL Dashboard (setelah deploy): lihat file `url.txt`

Langkah deploy ke Streamlit Community Cloud:
1. Push proyek ke GitHub repository
2. Login ke [share.streamlit.io](https://share.streamlit.io)
3. Pilih repository dan set main file: `dashboard/dashboard.py`
4. Klik **Deploy**

---

**Nama:** [Nama Anda]  
**Email Dicoding:** [Email Anda]  
**Kelas:** Belajar Fundamental Analisis Data — Dicoding
