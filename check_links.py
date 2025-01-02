import datetime
import csv
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

def is_first_saturday_in_august(date): 
    return (date.year == 2022 or date.year == 2023) and date.month == 8 and date.weekday() == 5 and 1 <= date.day <= 7

def check_url_accessibility(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def check_url_and_modify(date, issue, url):
    modified_url = url.replace('zip', 'm4a')
    is_zip_accessible = check_url_accessibility(url)
    is_m4a_accessible = check_url_accessibility(modified_url)
    return [date, issue, url, is_zip_accessible, is_m4a_accessible]

start_date = datetime.date(2007, 5, 26)
end_date = datetime.date(2024, 12, 7)
schedule_day = []

current_date = start_date
while current_date <= end_date:
    if current_date.weekday() == 5:
        schedule_day.append(current_date)
    current_date += datetime.timedelta(days=1)

urls = []
weeks = 0

for i in schedule_day:
    year = i.strftime('%Y')
    month = i.strftime('%m')
    day = i.strftime('%d')
    date_str = i.strftime('%Y%m%d')
    issue = 8796 - 265 + weeks

    if date_str == '20111224':
        continue    
    if (month != '12' or int(day) < 25) and not is_first_saturday_in_august(i):
        if date_str == '20190330': 
            url = f"https://audiocdn.economist.com/sites/default/files/AudioArchive/{year}/{date_str}/Issue_{issue}_{date_str}_The_Economist_Full_Edition.zip"
        elif date_str == '20210123': 
            url = f"https://audiocdn.economist.com/sites/default/files/AudioArchive/{year}/{date_str}/Issue_{issue + 1}_{date_str}_The_Economist_Full_edition.zip"
        elif date_str <= '20120728': 
            url = f"https://audiocdn.economist.com/sites/default/files/AudioArchive/{year}/{date_str}/{date_str}_TheEconomist_Full_Edition.zip"
        else: 
            url = f"https://audiocdn.economist.com/sites/default/files/AudioArchive/{year}/{date_str}/Issue_{issue}_{date_str}_The_Economist_Full_edition.zip"
        
        urls.append([i.strftime('%Y-%m-%d'), issue, url])
        weeks += 1

script_directory = os.path.dirname(os.path.realpath(__file__))
output_file_csv = os.path.join(script_directory, 'economist_urls_check.csv')

max_workers = 10
results = []

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(check_url_and_modify, date, issue, url): (date, issue, url) for date, issue, url in urls}
    
    with tqdm(total=len(futures), desc="Processing URLs", unit="URL") as pbar:
        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing URL {futures[future]}: {e}")
            pbar.update(1)

results.sort(key=lambda x: x[0])

with open(output_file_csv, 'w', newline='') as file_csv:
    writer = csv.writer(file_csv)
    writer.writerow(['Date', 'Issue', 'Zip URL (M4A URL: replace zip with m4a in links)', 'Zip Accessible', 'M4A Accessible'])
    for row in results:
        writer.writerow(row)

print(f"Results have been written to {output_file_csv}")
