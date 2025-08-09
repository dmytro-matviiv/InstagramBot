# Instagram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Telegram channel link
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK', 'https://t.me/your_channel')

# News sources - ДЖЕРЕЛА З ЯКІСНИМИ ВЕЛИКИМИ ФОТОГРАФІЯМИ
NEWS_SOURCES = [
    # ПРІОРИТЕТНІ джерела з великими фото
    'https://tsn.ua/rss/full.rss',  # ТСН - має високоякісні фото
    'https://24tv.ua/rss/',  # 24 канал - багато фото хорошої якості
    'https://www.ukrinform.ua/rss/block-lastnews',  # Укрінформ - офіційні фото
    'https://www.obozrevatel.com/rss.xml',  # Обозреватель - якісні зображення
    
    # Міжнародні джерела з професійними фото
    'https://www.dw.com/uk/rss/news',  # Deutsche Welle - професійна фотожурналістика
    'https://www.eurointegration.com.ua/rss/',  # Європейська правда - якісні фото
    'https://www.bbc.com/ukrainian/rss.xml',  # BBC Україна - професійні фото
    
    # Спеціалізовані джерела
    'https://armyinform.com.ua/feed/',  # АрміяInform - офіційні військові фото
    'https://www.ukrinform.ua/rss/block-war',  # Військові новини з фото
    'https://interfax.com.ua/news/rss/',  # Інтерфакс - агентські фото
    
    # Додаткові якісні джерела
    'https://espreso.tv/rss',  # Еспресо ТВ
    'https://censor.net/includes/news_rss.php',  # Цензор.нет
    'https://gordonua.com/xml/rss_category/1.html',  # Гордон
    'https://www.pravda.com.ua/rss/',  # Українська правда
    'https://hromadske.ua/rss',  # Громадське медіа
    'https://www.radiosvoboda.org/api/zmgqoemtkv',  # Радіо Свобода
    'https://zn.ua/rss/',  # Дзеркало тижня
]

# Image requirements - РЕАЛІСТИЧНІ ВИМОГИ ДО ЯКОСТІ РЕАЛЬНИХ ФОТО
IMAGE_REQUIREMENTS = {
    'min_width': 600,        # Реалістичний мінімум для новинних сайтів
    'min_height': 400,       # Реалістичний мінімум для новинних сайтів
    'preferred_min_width': 800,   # Ідеальний розмір
    'preferred_min_height': 600,  # Ідеальний розмір
    'max_scale_factor': 2.0,       # Розумне збільшення
    'aspect_ratio_range': (0.3, 3.0),  # Розумні пропорції
    'max_file_size_mb': 30,
    'min_pixels': 240000     # Мінімум 600x400 пікселів (реалістично)
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
