import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import concurrent.futures
import csv

def fetch_and_parse(year):
    url = f"https://www.economist.com/weeklyedition/archive?year={year}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        figures = soup.find_all('figure', class_='css-j0a8mg e1197rjj0')
        image_urls_and_dates = []
        for figure in figures:
            img = figure.find('img')
            if img and 'src' in img.attrs:
                img_url = img['src']
                a_tag = figure.find_parent('div').find_next('div').find('a')
                if a_tag and 'href' in a_tag.attrs:
                    href = a_tag['href']
                    match = re.search(r'(\d{4}-\d{2}-\d{2})', href)
                    if match:
                        date_str = match.group(1)
                        img_url = re.sub(r'width=\d+,quality=\d+', 'width=,quality=', img_url)
                        image_urls_and_dates.append((date_str, img_url))
        return image_urls_and_dates
    return []

def save_to_csv(image_urls_and_dates):
    image_urls_and_dates.sort(key=lambda x: x[0])
    with open('image_urls.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'img_url'])
        for date, img_url in image_urls_and_dates:
            writer.writerow([date, img_url])

def main():
    years = list(range(2024, 2006, -1))
    all_image_urls_and_dates = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_and_parse, year) for year in years]
        for future in concurrent.futures.as_completed(futures):
            image_urls_and_dates = future.result()
            all_image_urls_and_dates.extend(image_urls_and_dates)
    save_to_csv(all_image_urls_and_dates)
    print("Image URLs have been saved to 'image_urls.csv'")

if __name__ == "__main__":
    main()
