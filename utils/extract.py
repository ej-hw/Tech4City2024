# utils/extract.py

import sqlite3

def FetchRecords():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, url, sentiment, published_at FROM news_sentiments")
    records = cursor.fetchall()
    conn.close()

    formatted_records = []
    for record in records:
        formatted_records.append({
            "title": record[0],
            "url": record[1],
            "sentiment": record[2],
            "publishedAt": record[3]
        })

    return formatted_records
