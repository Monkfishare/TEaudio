import os
import pandas as pd
import openpyxl
from datetime import date

def is_first_saturday_in_august(date):
    return date.year >= 2022 and date.month == 8 and date.weekday() == 5 and 1 <= date.day <= 7

# Prompt the user to enter the year
year_input = input("Enter the year (or press Enter for the current year): ")

if year_input.strip() == "":
    year = date.today().year  # Use the current year
else:
    year = int(year_input)

# Calculate the last day of the entered year
last_day = pd.Timestamp(year, 12, 31)

schedule_day = pd.date_range('20070526', last_day, freq='W-SAT')
weeks = 0
urls = []

for i in schedule_day:
    year = i.strftime('%Y')
    month = i.strftime('%m')
    day = i.strftime('%d')
    date_str = i.strftime('%Y%m%d')  # Format date as "YYYYMMDD"
    issue = 8796 - 266 + weeks
    if (month != '12' or day < '25') and not is_first_saturday_in_august(i):
        if date_str == '20190330':
            url = "https://audiocdn.economist.com/sites/default/files/AudioArchive/{0}/{2}/Issue_{1}_{2}_The_Economist_Full_Edition.zip".format(year, issue, date_str)
        elif date_str == '20210123':
            url = "https://audiocdn.economist.com/sites/default/files/AudioArchive/{0}/{2}/Issue_{1}_{2}_The_Economist_Full_edition.zip".format(year, issue+1, date_str)
        elif date_str == '20111224':
            new_date = str(int(date_str) + 7)
            url = "https://audiocdn.economist.com/sites/default/files/AudioArchive/{0}/{2}/{2}_TheEconomist_Full_Edition.zip".format(year, issue, new_date)
        elif date_str <= '20120728':
            url = "https://audiocdn.economist.com/sites/default/files/AudioArchive/{0}/{2}/{2}_TheEconomist_Full_Edition.zip".format(year, issue, date_str)
        else:
            url = "https://audiocdn.economist.com/sites/default/files/AudioArchive/{0}/{2}/Issue_{1}_{2}_The_Economist_Full_edition.zip".format(year, issue, date_str)
        urls.append((i, issue, url))  # Append tuple with date, issue, and URL
        weeks += 1

df = pd.DataFrame(urls, columns=['Date', 'Issue', 'URL'])  # Add 'Issue' column
df['Date'] = pd.to_datetime(df['Date'])  # Convert 'Date' column to datetime type
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')  # Format date column as "YYYY-MM-DD"

# Create the output folder if it does not exist
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Save the DataFrame to an Excel file inside the 'output' folder
excel_filename = os.path.join(output_folder, 'economist_audio_urls.xlsx')
df.to_excel(excel_filename, index=False)

# Save the URLs to a TXT file inside the 'output' folder
txt_filename = os.path.join(output_folder, 'economist_audio_urls.txt')
with open(txt_filename, 'w') as txt_file:
    txt_file.write("Date\tIssue\tURL\n")  # Write the title line first
    for _, row in df.iterrows():
        txt_file.write(f"{row['Date']}\t{row['Issue']}\t{row['URL']}\n")

# Adjust column widths in the resulting Excel file
workbook = openpyxl.load_workbook(excel_filename)
worksheet = workbook.active

# Set column widths for all columns
for column_letter in worksheet.columns:
    max_length = 0
    column_index = column_letter[0].column  # Get the index of the column
    for cell in column_letter:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(str(cell.value))
        except TypeError:
            pass
    adjusted_width = (max_length + 2) * 1  # Adjust the width slightly for better visibility
    worksheet.column_dimensions[openpyxl.utils.get_column_letter(column_index)].width = adjusted_width

# Add filters to all columns
last_column_index = worksheet.max_column
last_column_letter = openpyxl.utils.get_column_letter(last_column_index)
worksheet.auto_filter.ref = f"A1:{last_column_letter}1"

# Save the workbook with adjusted column widths
workbook.save(excel_filename)
