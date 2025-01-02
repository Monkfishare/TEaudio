import datetime
import csv
import os

def is_first_saturday_in_august(date):
    return (date.year == 2022 or date.year == 2023) and date.month == 8 and date.weekday() == 5 and 1 <= date.day <= 7

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
output_file = os.path.join(script_directory, 'economist_urls.csv')

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Issue', 'Zip URL (M4A URL: replace zip with m4a in links)'])
    for row in urls:
        writer.writerow(row)

print(f"URLs have been written to {output_file}")
