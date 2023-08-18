data_filename = "datas.txt"
output_filename = "playlist (open with potplayer).m3u"

# Define a list of month names
month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Read data from the file
with open(data_filename, "r") as file:
    lines = file.readlines()

# Initialize the playlist content
playlist_content = "#EXTM3U\n"

# Iterate through the lines and process the data
for line in lines[1:]:  # Skip the header line
    date, audio_url = line.strip().split("\t")
    year, month, day = date.split("-")
    month_name = month_names[int(month) - 1]
    playlist_content += f'#EXTINF:-1 tvg-logo="https://logosdownload.com/logo/The-Economist-logo-512.png" group-title="{month_name} {year}", {date}\n'
    playlist_content += f"{audio_url}\n"

# Write the playlist content to the output file
with open(output_filename, "w") as file:
    file.write(playlist_content)

print(f"Playlist generated and saved as '{output_filename}'.")
