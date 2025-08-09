# Instagram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Telegram channel link
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK', 'https://t.me/your_channel')

# News sources - Українські та про Україну
NEWS_SOURCES = [
    'https://www.pravda.com.ua/rss/',
    'https://tsn.ua/rss/full.rss',
    'https://nv.ua/rss/all.xml',
    'https://www.radiosvoboda.org/api/zmgqoemtkv',
    'https://www.bbc.com/ukrainian/news/rss.xml',
    'https://suspilne.media/rss/',
    'https://hromadske.ua/rss',
    'https://24tv.ua/rss/',
    'https://www.unian.ua/rss/news.xml'
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
