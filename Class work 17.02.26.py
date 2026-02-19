import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import execute_values
from database.PostgreSQLHandler import save_articles
from database.PostgreSQLHandler import setup_database
# Настройки подключения к базе данных
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'



import requests
from bs4 import BeautifulSoup
import sqlite3
from dataclasses import dataclass, asdict

# URL блога
BLOG_URL = 'https://msk.top-academy.ru/blog'

@dataclass
class BlogArticle:
    title: str
    text: str

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return BlogArticle(title=data['title'], text=data['text'])

class BlogParser:
    def __init__(self, url):
        self.url = url

    def fetch_html(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text

    def parse_articles(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        articles = []

        # Находим все блоки с классом styles_cardBody__qP0jN
        blocks = soup.find_all('div', class_='styles_cardBody__qP0jN')
        for block in blocks:
            # Извлекаем заголовки (h1)
            h1 = block.find('h1')
            title = h1.get_text(strip=True) if h1 else 'Без заголовка'

            # Извлекаем текст (p)
            p = block.find('p')
            text = p.get_text(strip=True) if p else ''

            articles.append(BlogArticle(title=title, text=text))
        return articles

def create_database(db_name='top_academy_blog.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            text TEXT
        )
    ''')
    conn.commit()
    return conn



def print_first_five_articles(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, text FROM articles ORDER BY id LIMIT 5')
    rows = cursor.fetchall()
    print("\nПервые 5 статей из базы данных:")
    for row in rows:
        print(f"\nID: {row[0]}\nЗаголовок: {row[1]}\nТекст: {row[2]}")

def main():
    print("Запуск парсинга блога Top Academy...")
    setup_database()
    parser = BlogParser(BLOG_URL)
    try:
        html = parser.fetch_html()
        articles = parser.parse_articles(html)
        print(f"Найдено статей: {len(articles)}")
    except Exception as e:
        print(f"Ошибка при парсинге: {e}")
        return

    saved_count = save_articles(articles)
    print(f"Сохранено новых статей: {saved_count}")

if __name__ == '__main__':
    main()