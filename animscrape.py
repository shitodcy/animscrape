import requests
import csv
from bs4 import BeautifulSoup
import time
import re

def scrape_page(url):
    try:
        print(f"\U0001F50D Scraping URL: {url}")  # Debugging
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        anime_list = []

        anime_items = soup.find_all('div', class_='seasonal-anime')

        for anime in anime_items:
            title_tag = anime.find('h2', class_='h2_anime_title')
            title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else 'N/A'

            release_tag = anime.find('div', class_='info').find('span', class_='item')
            release_date = release_tag.get_text(strip=True).split(', ')[-1] if release_tag else 'N/A'

            rating_tag = anime.find('div', class_='scormem-item score score-label score-5')
            rating = rating_tag.get_text(strip=True) if rating_tag else 'N/A'

            studio_tag = anime.find('div', class_='property').find('span', class_='item').find('a')
            studio = studio_tag.get_text(strip=True) if studio_tag else 'N/A'

            anime_list.append({'title': title, 'rating': rating, 'release_date': release_date, 'studio': studio})

        print(f"✅ Berhasil scrape {len(anime_list)} anime dari {url}") 
        return anime_list
    except requests.exceptions.RequestException as e:
        print(f"❌ Terjadi kesalahan: {e}")
        return []

def get_genres():
    url = "https://myanimelist.net/anime.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    genre_links = soup.select('div.genre-list a')
    
    genres = {link.text.strip(): link['href'] for link in genre_links}
    return genres

def scrape_all_genres(limit):
    genres = get_genres()
    all_anime = []
    
    for genre_name, genre_url in genres.items():
        if len(all_anime) >= limit:
            break
        print(f"\U0001F3AD Scraping genre: {genre_name}")
        
        full_url = f"https://myanimelist.net{genre_url}"
        page_data = scrape_page(full_url)

        for anime in page_data:
            clean_genre = re.sub(r'\s*\(\d+[,.\d]*\)', '', genre_name)
            anime['genre'] = clean_genre
            all_anime.append(anime)
            
            if len(all_anime) >= limit:
                return all_anime
        
        time.sleep(2)  
    
    return all_anime

def save_to_csv(data, filename):
    try:
        missing_scores = [anime['title'] for anime in data if anime['rating'] == 'N/A']
        missing_studios = [anime['title'] for anime in data if anime['studio'] == 'N/A']

        print(f"⚠️ {len(missing_scores)} anime tidak memiliki score!")
        print(f"⚠️ {len(missing_studios)} anime tidak memiliki studio!")
        
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Judul", "Rating", "Genre", "Tahun Rilis", "Studio"])
            for item in data:
                writer.writerow([item['title'], item['rating'], item['genre'], item['release_date'], item['studio']])
        print(f"✅ Data berhasil disimpan di {filename}")
    except Exception as e:
        print(f"❌ Gagal menyimpan data: {e}")

if __name__ == "__main__":
    try:
        limit = int(input("Masukkan jumlah anime yang ingin di-scrape (misalnya: 300): ").strip())
        hasil = scrape_all_genres(limit=limit)
        
        if hasil:
            print(f"\nTotal anime yang dikumpulkan: {len(hasil)}")
            filename = input("Masukkan nama file untuk menyimpan hasil (contoh: my_anime_list.csv): ").strip()
            if not filename.endswith(".csv"):
                filename += ".csv"
            save_to_csv(hasil, filename)
    except ValueError:
        print("❌ Harap masukkan angka yang valid untuk limit scraping.")
