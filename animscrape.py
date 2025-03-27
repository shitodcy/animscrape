import requests
import csv
from bs4 import BeautifulSoup
import time
import re

def display_ascii_art():
    ascii_art = """
      ___________________________
     < Karak Scraping Tools! >
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

def scrape_page(url, current_genre):
    try:
        print(f"🔍 Scraping URL: {url}")  
        response = session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        anime_list = []

        anime_items = soup.find_all('div', class_='seasonal-anime')

        for anime in anime_items:
            title_tag = anime.find('h2', class_='h2_anime_title')
            title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else 'N/A'

            release_tag = anime.find('div', class_='info')
            release_date = release_tag.find('span', class_='item').get_text(strip=True).split(', ')[-1] if release_tag and release_tag.find('span', class_='item') else 'N/A'

            rating_tag = anime.find('div', class_='scormem-item score score-label score-5')
            rating = rating_tag.get_text(strip=True) if rating_tag else 'N/A'

            studio_tag = anime.find('div', class_='property')
            studio = studio_tag.find('span', class_='item').find('a').get_text(strip=True) if studio_tag and studio_tag.find('span', class_='item') and studio_tag.find('span', class_='item').find('a') else 'N/A'

            anime_list.append({
                'title': title,
                'rating': rating,
                'release_date': release_date,
                'studio': studio,
                'genre': current_genre
            })

        print(f"✅ Berhasil scrape {len(anime_list)} anime dari {url}") 
        return anime_list
    except requests.exceptions.RequestException as e:
        print(f"❌ Terjadi kesalahan: {e}")
        return []

def get_genres():
    url = "https://myanimelist.net/anime.php"
    response = session.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    genre_links = soup.select('a.genre-name-link')  # Select by specific class
    
    genres = {}
    for link in genre_links:
        # Clean genre name by removing the count in parentheses
        genre_name = re.sub(r'\s*\(\d+[,\.\d]*\)', '', link.text.strip())
        genres[genre_name] = link['href']
    
    return genres

def select_genres(all_genres):
    print("\n🎭 Daftar Genre yang Tersedia:")
    sorted_genres = sorted(all_genres.items())
    for i, (genre_name, _) in enumerate(sorted_genres, start=1):
        print(f"{i}. {genre_name}")
    
    print("\nPilih genre yang ingin di-scrape:")
    print("1. Masukkan nomor genre (contoh: 1,3,5)")
    print("2. Ketik 'all' untuk memilih semua genre")
    print("3. Ketik 'cancel' untuk membatalkan")
    
    while True:
        choice = input("\nMasukkan pilihan Anda: ").strip().lower()
        
        if choice == 'all':
            return sorted_genres
        elif choice == 'cancel':
            return None
        else:
            try:
                selected_indices = [int(idx.strip()) for idx in choice.split(',')]
                selected_genres = []
                for idx in selected_indices:
                    if 1 <= idx <= len(sorted_genres):
                        selected_genres.append(sorted_genres[idx-1])
                    else:
                        print(f"⚠️ Peringatan: Nomor {idx} tidak valid dan akan diabaikan")
                if selected_genres:
                    return selected_genres
                else:
                    print("❌ Tidak ada genre yang valid dipilih. Silakan coba lagi.")
            except ValueError:
                print("❌ Input tidak valid. Silakan masukkan nomor genre yang dipisahkan koma (contoh: 1,3,5)")

def scrape_genre_pages(genre_url, genre_name, limit, collected_count):
    page = 1
    all_anime = []

    while collected_count < limit:
        full_url = f"https://myanimelist.net{genre_url}?page={page}"
        print(f"📄 Scraping {genre_name} - Halaman {page}")
        page_data = scrape_page(full_url, genre_name)

        if not page_data:
            break  

        all_anime.extend(page_data)
        collected_count += len(page_data)
        
        if collected_count >= limit:
            break
        
        page += 1
        time.sleep(2)  

    return all_anime[:limit], min(collected_count, limit)

def scrape_selected_genres(selected_genres, limit):
    all_anime = []
    collected_count = 0
    
    for genre_name, genre_url in selected_genres:
        if collected_count >= limit:
            break
        
        print(f"\n🎭 Memulai scraping genre: {genre_name}")
        genre_data, collected_count = scrape_genre_pages(genre_url, genre_name, limit, collected_count)
        all_anime.extend(genre_data)

        if len(all_anime) % 100 == 0:  # Backup every 100 records
            save_to_csv(all_anime, "backup_scraped_data.csv")
            print(f"💾 Backup sementara disimpan! Total terkumpul: {len(all_anime)} data")

        time.sleep(3)  
    
    return all_anime[:limit]

def save_to_csv(data, filename):
    try:
        # Calculate genre statistics
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
        
        limit = int(input("Masukkan jumlah anime yang ingin di-scrape (misalnya: 100): ").strip())
        
        print("\n🔄 Mengambil daftar genre dari MyAnimeList...")
        all_genres = get_genres()
        selected_genres = select_genres(all_genres)
        
        if selected_genres is None:
            print("❌ Scraping dibatalkan.")
        else:
            print("\n📌 Genre yang dipilih:")
            for genre, _ in selected_genres:
                print(f"- {genre}")
            
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
