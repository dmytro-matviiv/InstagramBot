#!/usr/bin/env python3
"""
Тест створення поста
"""

from simple_bot import SimpleInstagramBot
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_post_creation():
    print("=== ТЕСТ СТВОРЕННЯ ПОСТА ===")
    
    bot = SimpleInstagramBot()
    
    # Знаходимо новину з фото
    news_data = bot.find_news_with_image()
    if news_data:
        article = news_data['article'] 
        print(f"\n📄 ЗАГОЛОВОК: {article.get('title', 'N/A')}")
        print(f"📸 ФОТО: {news_data['image'].size[0]}x{news_data['image'].size[1]}")
        print(f"🔗 ДЖЕРЕЛО: {news_data.get('source_url', 'N/A')[:60]}...")
        
        # Генеруємо контент
        print("\n🔄 Генерую контент...")
        ukrainian_article = bot.translator.translate_news_article(article)
        post_content = bot.content_generator.create_full_post(
            ukrainian_article.get('title', ''),
            ukrainian_article.get('text', ukrainian_article.get('summary', ''))
        )
        
        print(f"\n📝 ЗГЕНЕРОВАНИЙ ПОСТ ({len(post_content)} символів):")
        print("=" * 60)
        print(post_content)
        print("=" * 60)
        
        print("\n✅ ТЕСТ УСПІШНИЙ! Пост готовий до публікації.")
    else:
        print("❌ Не знайдено новин з фото")

if __name__ == "__main__":
    test_post_creation()



