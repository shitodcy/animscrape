## 📹 Video Demo
[[Demo Anime Scraper]](https://youtu.be/pwggTSu1P9k?si=Cs_XfA2y1L3pJvuB)

Anime Scraper adalah script Python untuk mengekstrak data anime dari **MyAnimeList** berdasarkan genre dan menyimpannya dalam file **CSV**. 

## 🚀 Instalasi & Penggunaan

### 1️⃣ **Instalasi Dependensi**
Pastikan kamu sudah menginstal **Python 3.7+**, lalu jalankan perintah berikut:
```bash
git clone https://github.com/shitodcy/animscrape
cd animscrape
pip install -r requirements.txt
```

### 2️⃣ **Jalankan Script**
> 🚀 Jalankan perintah berikut di terminal atau command prompt:  
```bash
python animscrape.py
```

### 3️⃣ **Masukkan Input**
> 📝 **Masukkan jumlah anime** yang ingin diambil (contoh: `4999` untuk mendapatkan hasil data 5000 baris).  
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

## 👥 Kontributor

Terima kasih kepada semua yang telah berkontribusi pada proyek ini:

- [@shitodcy](https://github.com/shitodcy)
- [@JihanPaperwork](https://github.com/JihanPaperwork)
- [@iruru21](https://github.com/iruru21)

