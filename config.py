# Instagram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Telegram channel link
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK', 'https://t.me/your_channel')

# News sources - Українські джерела З ФОТОГРАФІЯМИ
NEWS_SOURCES = [
    'https://www.bbc.com/ukrainian/news/rss.xml',  # BBC завжди має фото
    'https://www.ukrinform.ua/rss/block-lastnews',  # Укрінформ має фото в більшості новин
    'https://suspilne.media/rss/',  # Суспільне має якісні фото
    'https://24tv.ua/rss/',  # 24tv має фото
    'https://www.pravda.com.ua/rss/',  # Правда часто має фото
    'https://hromadske.ua/rss',  # Громадське має фото
    'https://www.radiosvoboda.org/api/zmgqoemtkv',  # Радіо Свобода має фото
    'https://www.unn.com.ua/rss/news_uk.xml',  # УНН з фото
    'https://www.rbc.ua/static/rss/ukr/all.xml',  # RBC України з фото
    'https://zn.ua/rss/'  # Дзеркало тижня з фото
]

# Image requirements for horizontal posts
IMAGE_REQUIREMENTS = {
    'min_width': 1350,
    'min_height': 1080,  # Instagram horizontal ratio
    'aspect_ratio_range': (1.25, 1.91),  # 5:4 to 16:9 for horizontal
    'max_file_size_mb': 30
}

# OpenAI for content generation
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Posting schedule (hours)
POSTING_INTERVALS = [2, 3]  # Random between 2-3 hours

# Call-to-action phrases for Telegram link
CTA_PHRASES = [
    "🔥 Більше цікавих новин у нашому Telegram каналі!",
    "📢 Приєднуйтесь до нашої спільноти в Telegram!",
    "💡 Не пропустіть ексклюзивний контент в Telegram!",
    "⚡ Свіжі новини щодня в нашому каналі!",
    "🎯 Підписуйтесь на наш Telegram для актуальних новин!"
]
