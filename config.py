"""
Налаштування Instagram бота.

Опис ключових змінних:
- INSTAGRAM_USERNAME / INSTAGRAM_PASSWORD: облікові дані Instagram.
- TELEGRAM_CHANNEL_LINK: посилання на Telegram-канал для CTA у підписі.
- NEWS_SOURCES: список RSS-джерел новин (у поточній конфігурації — тільки ТСН).
- IMAGE_REQUIREMENTS: мінімальні вимоги до якості зображення для публікації.
- OPENAI_API_KEY: ключ для генерації описів через OpenAI (за відсутності — локальний режим).
- POSTING_INTERVALS: інтервали між публікаціями у годинах (рандомний вибір).
- CTA_PHRASES: пул коротких фраз-призивів до дії для посилення залучення.
"""

# Instagram Bot Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Дані авторизації Instagram
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Посилання на Telegram-канал (для CTA у підписі)
TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK', 'https://t.me/your_channel')

# Джерела новин (RSS) — у цій конфігурації підключено лише ТСН
NEWS_SOURCES = [
    'https://tsn.ua/rss/ato.rss',    # ТСН АТО/ООС - військові новини
    'https://tsn.ua/rss/full.rss',  # ТСН - загальні новини
]

# Вимоги до якості зображення — реалістичні для RSS картинок
IMAGE_REQUIREMENTS = {
    'min_width': 300,        # Знижені вимоги для RSS зображень
    'min_height': 200,       # Знижені вимоги для RSS зображень
    'preferred_min_width': 600,   # Ідеальний розмір
    'preferred_min_height': 400,  # Ідеальний розмір
    'max_scale_factor': 2.0,       # Розумне збільшення
    'aspect_ratio_range': (0.3, 3.0),  # Розумні пропорції
    'max_file_size_mb': 30,
    'min_pixels': 60000     # Мінімум 300x200 пікселів (для RSS)
}

# Мінімальний «вік» новини у годинах для публікації (щоб не брати надто свіжі)
MIN_ARTICLE_AGE_HOURS = 4

# Ключ OpenAI для генерації описів (за відсутності — локальний генератор)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Інтервали між публікаціями (у годинах), береться випадкове значення
POSTING_INTERVALS = [2, 3]  # Random between 2-3 hours

# Набір фраз (CTA) для додавання у підпис під публікацією
CTA_PHRASES = [
    "⚡ Останні новини війни та політики у нашому Telegram!",
    "🇺🇦 Стежте за подіями в Україні у нашому каналі!",
    "📢 Актуальна інформація про війну та світові новини в Telegram!",
    "🔥 Не пропустіть важливі новини - підписуйтесь на Telegram!",
    "💬 Обговорюємо головні події дня у нашому Telegram каналі!",
    "⚔️ Військові новини та аналітика у нашому Telegram!",
    "🌍 Україна та світ: головні події у нашому каналі!"
]
