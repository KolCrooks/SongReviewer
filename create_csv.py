import sqlite3
import csv
  
conn = sqlite3.connect('./music.sqlite')

cur = conn.cursor()
cur.execute("SELECT reviewid, title, artist, score FROM reviews")

reviews = cur.fetchall()
reviews_dict = {}

for r in reviews:
    (id, title, band, score) = r
    reviews_dict[id] = {'title': title, 'band': band, 'score':score, 'content': None}

cur.execute("SELECT reviewid, content FROM content")

content = cur.fetchall()

for c in content:
    (id, text) = c
    if reviews_dict[id]['content'] == None:
        reviews_dict[id]['content'] = text
    else:
        reviews_dict[id]

with open('music.csv', 'w', encoding="utf-8", newline='') as csvfile:
    fieldnames = ['id', 'title', 'band', 'score', 'content']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for (k, v) in reviews_dict.items():
        v['id'] = k
