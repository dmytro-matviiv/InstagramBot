# Instagram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Telegram channel link
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK', 'https://t.me/your_channel')

# News sources - ВІЙНА В УКРАЇНІ ТА СВІТОВІ НОВИНИ
NEWS_SOURCES = [
    # ВІЙСЬКОВІ ТА ПОЛІТИЧНІ новини - ПРІОРИТЕТ
    'https://www.ukrinform.ua/rss/block-war',  # Укрінформ - військові новини з фото
    'https://armyinform.com.ua/feed/',  # АрміяInform - офіційні військові фото
    'https://tsn.ua/rss/ato.rss',  # ТСН АТО/ООС - військові новини
    'https://24tv.ua/war/',  # 24TV - новини війни
    
    # УКРАЇНСЬКІ НОВИНИ - головні події
    'https://www.ukrinform.ua/rss/block-lastnews',  # Укрінформ - останні новини
    'https://tsn.ua/rss/full.rss',  # ТСН - загальні новини
    'https://24tv.ua/rss/',  # 24 канал - новини України
    'https://www.pravda.com.ua/rss/',  # Українська правда
    
    # МІЖНАРОДНІ НОВИНИ про Україну та світ
    'https://www.dw.com/uk/rss/news',  # Deutsche Welle українською
    'https://www.bbc.com/ukrainian/rss.xml',  # BBC Україна
    'https://www.radiosvoboda.org/api/zmgqoemtkv',  # Радіо Свобода
    'https://www.eurointegration.com.ua/rss/',  # Європейська правда
    
    # АНАЛІТИКА та ПОЛІТИКА
    'https://hromadske.ua/rss',  # Громадське медіа
    'https://espreso.tv/rss',  # Еспресо ТВ
    'https://censor.net/includes/news_rss.php',  # Цензор.нет
    'https://gordonua.com/xml/rss_category/1.html',  # Гордон
    'https://zn.ua/rss/',  # Дзеркало тижня
    'https://interfax.com.ua/news/rss/',  # Інтерфакс Україна
    'https://www.obozrevatel.com/rss.xml',  # Обозреватель
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

# Call-to-action phrases for Telegram link - ВІЙСЬКОВО-ПОЛІТИЧНА ТЕМАТИКА
CTA_PHRASES = [
    "⚡ Останні новини війни та політики у нашому Telegram!",
    "🇺🇦 Стежте за подіями в Україні у нашому каналі!",
    "📢 Актуальна інформація про війну та світові новини в Telegram!",
    "🔥 Не пропустіть важливі новини - підписуйтесь на Telegram!",
    "💬 Обговорюємо головні події дня у нашому Telegram каналі!",
    "⚔️ Військові новини та аналітика у нашому Telegram!",
    "🌍 Україна та світ: головні події у нашому каналі!"
]
