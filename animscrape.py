import requests
import csv
from bs4 import BeautifulSoup
import time
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def display_ascii_art():
    ascii_art = """
      ___________________________
     < Animscrape Tools! >
      ---------------------------
                       ⢀⣀⠤⠿⢤⢖⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                     ⡔⢩⠂⠀⠒⠗⠈⠀⠉⠢⠄⣀⠠⠤⠄⠒⢖⡒⢒⠂⠤⢄⠀⠀⠀⠀
                     ⠇⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠈⠀⠈⠈⡨⢀⠡⡪⠢⡀⠀
                     ⠈⠒⠀⠤⠤⣄⡆⡂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠢⠀⢕⠱⠀
⠀⠀⠀⠀⠀                     ⠈⢳⣐⡐⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠁⠇
⠀⠀⠀⠀⠀⠀⠀                     ⠑⢤⢁⠀⠆⠀⠀⠀⠀⠀⢀⢰⠀⠀⠀⡀⢄⡜⠀
⠀⠀⠀⠀⠀⠀⠀⠀                     ⠘⡦⠄⡷⠢⠤⠤⠤⠤⢬⢈⡇⢠⣈⣰⠎⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀                     ⠀⣃⢸⡇⠀⠀⠀⠀⠀⠈⢪⢀⣺⡅
                              ⠶⡿⠤⠚⠁⠀⠀⠀⢀⣠⡤⢺⣥⠟⠀⠀
    """
    print(ascii_art)

display_ascii_art()

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

def scrape_page(url, genre_name):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        anime_list = []

        anime_items = soup.find_all('div', class_='seasonal-anime')

        for anime in anime_items:
            title_tag = anime.find('h2', class_='h2_anime_title')
            title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else 'N/A'

            release_tag = anime.find('div', class_='info')
            release_date = release_tag.find('span', class_='item').get_text(strip=True).split(', ')[-1] if release_tag and release_tag.find('span', class_='item') else 'N/A'

            rating_tag = anime.find('div', class_=lambda x: x and x.startswith('scormem-item score score-label score-'))
            rating = rating_tag.get_text(strip=True) if rating_tag else 'N/A'

            studio_tag = anime.find('div', class_='property')
            studio = studio_tag.find('span', class_='item').find('a').get_text(strip=True) if studio_tag and studio_tag.find('span', class_='item') and studio_tag.find('span', class_='item').find('a') else 'N/A'

            anime_list.append({
                'title': title,
                'rating': rating,
                'release_date': release_date,
                'studio': studio,
                'genre': genre_name
            })

        return anime_list
    except Exception as e:
        print(f"❌ Error scraping {url}: {str(e)}")
        return []

def get_genres():
    # Define all genres with proper organization
    genres = {
        "Main Genres": {
            "Action": "/anime/genre/1/Action",
            "Adventure": "/anime/genre/2/Adventure",
            "Avant Garde": "/anime/genre/5/Avant_Garde",
            "Award Winning": "/anime/genre/46/Award_Winning",
            "Boys Love": "/anime/genre/28/Boys_Love",
            "Comedy": "/anime/genre/4/Comedy",
            "Drama": "/anime/genre/8/Drama",
            "Fantasy": "/anime/genre/10/Fantasy",
            "Girls Love": "/anime/genre/26/Girls_Love",
            "Gourmet": "/anime/genre/47/Gourmet",
            "Horror": "/anime/genre/14/Horror",
            "Mystery": "/anime/genre/7/Mystery",
            "Romance": "/anime/genre/22/Romance",
            "Sci-Fi": "/anime/genre/24/Sci-Fi",
            "Slice of Life": "/anime/genre/36/Slice_of_Life",
            "Sports": "/anime/genre/30/Sports",
            "Supernatural": "/anime/genre/37/Supernatural",
            "Suspense": "/anime/genre/41/Suspense"
        },
        "Explicit Genres": {
            "Ecchi": "/anime/genre/9/Ecchi",
            "Erotica": "/anime/genre/49/Erotica",
            "Hentai": "/anime/genre/12/Hentai"
        },
        "Demographics": {
            "Josei": "/anime/genre/43/Josei",
            "Kids": "/anime/genre/15/Kids",
            "Seinen": "/anime/genre/42/Seinen",
            "Shoujo": "/anime/genre/25/Shoujo",
            "Shounen": "/anime/genre/27/Shounen"
        }
    }
    return genres

def select_genres(genres):
    print("\n🎭 Pilih Kategori Genre:")
    genre_categories = list(genres.keys())
    for i, category in enumerate(genre_categories, start=1):
        print(f"{i}. {category}")
    
    print("\nPilih kategori genre yang ingin di-scrape:")
    print("1. Masukkan nomor kategori")
    print("2. Ketik 'cancel' untuk membatalkan")
    
    while True:
        choice = input("\nMasukkan pilihan Anda: ").strip().lower()
        
        if choice == 'cancel':
            return None
        try:
            category_idx = int(choice) - 1
            if 0 <= category_idx < len(genre_categories):
                selected_category = genre_categories[category_idx]
                break
            print("❌ Nomor kategori tidak valid. Silakan coba lagi.")
        except ValueError:
            print("❌ Input tidak valid. Silakan masukkan nomor kategori.")
    
    print(f"\n🎭 Daftar Genre {selected_category} yang Tersedia:")
    genre_items = genres[selected_category]
    sorted_genres = sorted(genre_items.items())
    for i, (genre_name, _) in enumerate(sorted_genres, start=1):
        print(f"{i}. {genre_name}")
    
    print("\nPilih genre yang ingin di-scrape:")
    print("1. Masukkan nomor genre (contoh: 1,3,5)")
    print("2. Ketik 'cancel' untuk membatalkan")
    
    while True:
        choice = input("\nMasukkan pilihan Anda: ").strip().lower()
        
        if choice == 'cancel':
            return None
        try:
            selected_indices = [int(idx.strip()) for idx in choice.split(',')]
            selected_genres = []
            for idx in selected_indices:
                if 1 <= idx <= len(sorted_genres):
                    genre_name, genre_url = sorted_genres[idx-1]
                    selected_genres.append((genre_name, genre_url))
                else:
                    print(f"⚠️ Peringatan: Nomor {idx} tidak valid dan akan diabaikan")
            if selected_genres:
                return selected_genres
            print("❌ Tidak ada genre yang valid dipilih. Silakan coba lagi.")
        except ValueError:
            print("❌ Input tidak valid. Silakan masukkan nomor genre yang dipisahkan koma (contoh: 1,3,5)")

def scrape_genre(genre_name, genre_url, limit):
    all_anime = []
    page = 1
    
    while len(all_anime) < limit:
        full_url = f"https://myanimelist.net{genre_url}?page={page}"
        page_data = scrape_page(full_url, genre_name)
        
        if not page_data:
            break
            
        all_anime.extend(page_data)
        page += 1
        
        if len(all_anime) >= limit:
            break
            
    return all_anime[:limit]

def scrape_selected_genres(selected_genres, limit):
    all_anime = []
    start_time = time.time()
    
    limit_per_genre = max(1, limit // len(selected_genres))
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for genre_name, genre_url in selected_genres:
            futures.append(executor.submit(scrape_genre, genre_name, genre_url, limit_per_genre))
        
        for future in as_completed(futures):
            try:
                genre_data = future.result()
                all_anime.extend(genre_data)
                print(f"✅ Selesai scraping {len(genre_data)} anime dari genre {genre_data[0]['genre'] if genre_data else 'unknown'}")
            except Exception as e:
                print(f"❌ Error saat scraping: {str(e)}")
    
    if len(all_anime) < limit:
        remaining = limit - len(all_anime)
        if selected_genres:
            genre_name, genre_url = selected_genres[0]
            extra_data = scrape_genre(genre_name, genre_url, remaining)
            all_anime.extend(extra_data)
            print(f"➕ Menambahkan {len(extra_data)} anime dari {genre_name} untuk mencapai limit")
    
    print(f"\n⏱️ Waktu scraping total: {time.time() - start_time:.2f} detik")
    return all_anime[:limit]

def save_to_csv(data, filename):
    try:
        genres_count = {}
        for anime in data:
            genre = anime['genre']
            genres_count[genre] = genres_count.get(genre, 0) + 1
        
        print("\n📊 Statistik Genre:")
        for genre, count in genres_count.items():
            print(f"- {genre}: {count} anime")
        
        missing_scores = sum(1 for anime in data if anime['rating'] == 'N/A')
        missing_studios = sum(1 for anime in data if anime['studio'] == 'N/A')
        print(f"\n⚠️ {missing_scores} anime tidak memiliki score!")
        print(f"⚠️ {missing_studios} anime tidak memiliki studio!")
        
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Judul", "Rating", "Genre", "Tahun Rilis", "Studio"])
            for item in data:
                writer.writerow([item['title'], item['rating'], item['genre'], item['release_date'], item['studio']])
        print(f"\n✅ Data berhasil disimpan di {filename}")
        print(f"📌 Total anime yang disimpan: {len(data)}")
    except Exception as e:
        print(f"❌ Gagal menyimpan data: {e}")

if __name__ == "__main__":
    try:
        limit = int(input("Masukkan jumlah anime yang ingin di-scrape (misalnya: 199 untuk 200 baris): ").strip())
        
        print("\n🔄 Memuat daftar genre...")
        genres = get_genres()
        selected_genres = select_genres(genres)
        
        if not selected_genres:
            print("❌ Scraping dibatalkan.")
        else:
            print("\n📌 Genre yang dipilih:")
            for genre_name, _ in selected_genres:
                print(f"- {genre_name}")
            
            confirm = input("\nApakah Anda yakin ingin melanjutkan? (y/n): ").lower()
            if confirm == 'y':
                hasil = scrape_selected_genres(selected_genres, limit=limit)
                
                if hasil:
                    print(f"\n🎉 Scraping selesai! Total anime yang dikumpulkan: {len(hasil)}")
                    filename = input("\nMasukkan nama file untuk menyimpan hasil (contoh: anime_data.csv): ").strip()
                    if not filename.endswith(".csv"):
                        filename += ".csv"
                    save_to_csv(hasil, filename)
            else:
                print("❌ Scraping dibatalkan.")
    except ValueError:
        print("❌ Harap masukkan angka yang valid untuk limit scraping.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan tidak terduga: {e}")
