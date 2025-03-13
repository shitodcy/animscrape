import requests
import csv
from bs4 import BeautifulSoup
import time

def scrape_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        anime_list = []

        anime_items = soup.find_all('tr', class_='ranking-list')

        for anime in anime_items:
            # Judul anime
            title_tag = anime.find('h3', class_='anime_ranking_h3')
            title = title_tag.a.get_text(strip=True) if title_tag and title_tag.a else 'N/A'

            # Skor anime
            rating_tag = anime.find('span', class_=lambda c: c and 'score-label' in c.split())
            rating = rating_tag.get_text(strip=True) if rating_tag else 'N/A'

            anime_list.append({'title': title, 'rating': rating})

        return anime_list
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan: {e}")
        return []

def scrape_multiple_pages(start=50, end=200, step=50):
    base_url = "https://myanimelist.net/topanime.php?limit="
    all_anime = []

    for limit in range(start, end + 1, step):
        print(f"🦊 -> {base_url}{limit}")
        page_data = scrape_page(base_url + str(limit))
        all_anime.extend(page_data)

        time.sleep(2)

    return all_anime

def save_to_csv(data, filename):
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Judul", "Rating"])
            for item in data:
                writer.writerow([item['title'], item['rating']])
        print(f"Data berhasil disimpan di {filename}")
    except Exception as e:
        print(f"Gagal menyimpan data: {e}")

if __name__ == "__main__":
    hasil = scrape_multiple_pages(start=50, end=200, step=50)
    
    if hasil:
        print(f"\nTotal anime yang dikumpulkan: {len(hasil)}")
        filename = input("Masukkan nama file untuk menyimpan hasil (contoh: my_anime_list.csv): ").strip()
        if not filename.endswith(".csv"):
            filename += ".csv"
        save_to_csv(hasil, filename)
