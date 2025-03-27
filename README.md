# 🎡 Anime Scraper

## 📹 Video Demo
[![Demo Anime Scraper]](https://youtu.be/pwggTSu1P9k?si=Cs_XfA2y1L3pJvuB)

Anime Scraper adalah script Python untuk mengekstrak data anime dari **MyAnimeList** berdasarkan genre dan menyimpannya dalam file **CSV**. 

## 🚀 Instalasi & Penggunaan

### 1️⃣ **Instalasi Dependensi**
Pastikan kamu sudah menginstal **Python 3.7+**, lalu jalankan perintah berikut:
```bash
pip install requests beautifulsoup4
```

### 2️⃣ **Jalankan Script**
> 🚀 Jalankan perintah berikut di terminal atau command prompt:  
```bash
python animscrape.py
```

### 3️⃣ **Masukkan Input**
> 📝 **Masukkan jumlah anime** yang ingin diambil (contoh: `5000`).  
> 📝 **Masukkan nama file CSV** untuk menyimpan hasil (contoh: `my_anime_list.csv`).  

## 📊 Fitur
✅ Mengambil daftar anime berdasarkan genre dari **MyAnimeList**  
✅ Menyimpan data dalam format **CSV**  
✅ Informasi yang diambil meliputi **Judul, Rating, Genre, Tahun Rilis, Studio**  
✅ Menggunakan **User-Agent** agar tidak terdeteksi sebagai bot  

## 🔧 Struktur Data CSV
| Judul | Rating | Genre | Tahun Rilis | Studio |
|--------|--------|--------|------------|--------|
| Nama Anime | 8.5 | Action | 2023 | Studio XYZ |
| Nama Anime 2 | N/A | Comedy | 2022 | Studio ABC |

## 🛠 Troubleshooting
- Jika data yang dikumpulkan **kurang dari limit**, kemungkinan karena beberapa anime tidak memiliki informasi lengkap.
- Jika terjadi **403 Forbidden**, coba gunakan **VPN** atau ganti **User-Agent** pada kode.

## 🌟 Kontribusi
Pull request sangat diterima! Pastikan kode tetap rapi dan sesuai dengan standar PEP8.

## 🌐 Lisensi
Proyek ini dirilis di bawah lisensi **MIT**.

---
📚 Dibuat dengan ❤ oleh **[shitodcy]**
