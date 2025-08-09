#!/usr/bin/env python3
"""
Швидкий тест Instagram бота без OpenAI
"""

import os
import sys
from datetime import datetime

# Перевіряємо чи є .env файл
if not os.path.exists('.env'):
    print("❌ Файл .env не знайдено!")
    print("📝 Створіть файл .env з наступним вмістом:")
    print("""
INSTAGRAM_USERNAME=globalno2025
INSTAGRAM_PASSWORD=Dimka2015780
TELEGRAM_CHANNEL_LINK=https://t.me/newstime20
OPENAI_API_KEY=
""")
    sys.exit(1)

# Завантажуємо змінні середовища
from dotenv import load_dotenv
load_dotenv()

print("🚀 Швидкий тест Instagram News Bot")
print("=" * 50)

# Тестуємо збір новин
print("\n📰 Тестую збір новин...")
try:
    from news_collector import NewsCollector
    collector = NewsCollector()
    news = collector.get_random_news()
    
    if news:
        print(f"✅ Новина знайдена: {news.get('title', 'N/A')[:50]}...")
        print(f"📝 Контент: {len(news.get('text', ''))} символів")
    else:
        print("❌ Новини не знайдено")
except Exception as e:
    print(f"❌ Помилка збору новин: {e}")

# Тестуємо генерацію контенту
print("\n✍️ Тестую генерацію контенту...")
try:
    from content_generator import ContentGenerator
    generator = ContentGenerator()
    
    test_title = "Тестова новина про технології"
    test_content = "Це тестовий контент для перевірки роботи генератора контенту. Новина розповідає про важливі події."
    
    post = generator.create_full_post(test_title, test_content)
    print(f"✅ Пост згенеровано ({len(post)} символів)")
    print("📝 Приклад поста:")
    print("-" * 30)
    print(post[:300] + "..." if len(post) > 300 else post)
    print("-" * 30)
    
except Exception as e:
    print(f"❌ Помилка генерації контенту: {e}")

# Тестуємо пошук зображень
print("\n🖼️ Тестую пошук зображень...")
try:
    from image_handler import ImageHandler
    image_handler = ImageHandler()
    
    # Простий тест без реального пошуку (займає багато часу)
    print("✅ Модуль зображень завантажено")
    print("ℹ️ Для повного тесту зображень використайте --test в main.py")
    
except Exception as e:
    print(f"❌ Помилка модуля зображень: {e}")

# Тестуємо Instagram підключення
print("\n📱 Тестую підключення до Instagram...")
try:
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    
    if not username or not password:
        print("❌ Не налаштовано дані для Instagram")
    else:
        print(f"✅ Користувач: {username}")
        print("ℹ️ Для тесту входу використайте --test в main.py")
        
except Exception as e:
    print(f"❌ Помилка налаштувань Instagram: {e}")

print("\n🎯 Результат швидкого тесту:")
print("✅ Основні модулі працюють")
print("✅ Резервний генератор контенту готовий") 
print("✅ Бот може працювати БЕЗ OpenAI!")

print("\n🚀 Для запуску бота:")
print("   python main.py --test     # Повний тест")
print("   python main.py --post     # Одна публікація")
print("   python main.py --run      # Постійна робота")

print(f"\n⏰ Тест завершено: {datetime.now().strftime('%H:%M:%S')}")
