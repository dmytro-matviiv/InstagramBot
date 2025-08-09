# Instagram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Telegram channel link
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK', 'https://t.me/your_channel')

# News sources - ПЕРЕВІРЕНІ українські джерела з фотографіями
NEWS_SOURCES = [
    # Основні робочі джерела
    'https://www.ukrinform.ua/rss/block-lastnews',  # Укрінформ - працює, має фото
    'https://24tv.ua/rss/',  # 24 канал - працює, має фото
    'https://tsn.ua/rss/full.rss',  # ТСН - працює, має фото
    'https://armyinform.com.ua/feed/',  # АрміяInform - працює, військові фото
    
    # Додаткові рекомендовані джерела з фото
    'https://www.dw.com/uk/rss/news',  # Deutsche Welle українською
    'https://www.ukrinform.ua/rss/block-war',  # Укрінформ військові новини
    'https://espreso.tv/rss',  # Еспресо ТВ
    'https://www.eurointegration.com.ua/rss/',  # Європейська правда
    'https://interfax.com.ua/news/rss/',  # Інтерфакс Україна
    'https://censor.net/includes/news_rss.php',  # Цензор.нет
    'https://www.obozrevatel.com/rss.xml',  # Обозреватель
    'https://gordonua.com/xml/rss_category/1.html',  # Гордон
    
    # Резервні джерела
    'https://www.pravda.com.ua/rss/',  # Українська правда
    'https://hromadske.ua/rss',  # Громадське медіа
    'https://www.radiosvoboda.org/api/zmgqoemtkv',  # Радіо Свобода
    'https://zn.ua/rss/',  # Дзеркало тижня
]

# Image requirements - ПРИЙМАЄМО ВСІ ЯКІСНІ ФОТО
IMAGE_REQUIREMENTS = {
    'min_width': 400,        # Мінімум для реальних зображень
    'min_height': 300,       # Мінімум для реальних зображень
    'preferred_min_width': 600,   # Знижений бажаний мінімум
    'preferred_min_height': 400,  # Знижений бажаний мінімум
    'max_scale_factor': 3.0,      # Розумне збільшення для якості
    'aspect_ratio_range': (0.2, 5.0),  # ПРИЙМАЄМО ВСІ ОРІЄНТАЦІЇ
    'max_file_size_mb': 30,
    'min_pixels': 120000     # Мінімум 400x300 пікселів
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
