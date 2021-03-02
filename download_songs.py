from youtube_dl import YoutubeDL
import csv
import os
import shutil
import ffmpeg
import concurrent.futures

audio_downloader = YoutubeDL({'format': 'worstaudio', 'noplaylist': 'True', 'outtmpl': './temp/%(title)s.%(ext)s', 'ratelimit': 100000, 'quiet': True})
i = 0
max = 0
def downloadSongFile(searchString, id):
    global i, max
    print(f'DOWNLOADING: ({i}/{max}) - {searchString}')
    info = audio_downloader.extract_info(f"ytsearch:{searchString}", download=False)['entries'][0]
    audio_downloader.download([info['webpage_url']])
    filename = audio_downloader.prepare_filename(info)
    if os.path.exists(filename):
        ffmpeg.input(filename).output(f'./temp/{id}.mp3').run(quiet=True)
        os.remove(filename)
        os.rename(f'./temp/{id}.mp3', f'./songs/{id}.mp3') 
    else:
        print(f'ERROR: {info["webpage_url"]}')
        os.remove(f'{filename}.part')
    i += 1

with concurrent.futures.ThreadPoolExecutor() as executor:
    with open('music.csv', encoding='utf-8') as csvFile:
        reader = csv.reader(csvFile)
        header = True
        lines = list(reader)
        max = len(lines)
        for row in lines:
            if header:
                header = False
                continue;
            try:
                if not os.path.exists(f'./songs/{row[0]}.mp3'):
                    # id	title	band	score	content
                    searchString = f'{row[1]} {row[2]}'
                    
                    executor.submit(downloadSongFile, searchString = searchString, id=row[0])
                else:
                    i += 1
            except Exception as e:
                print(f'ERROR IN {row[0]}: {e}')

print('done!')