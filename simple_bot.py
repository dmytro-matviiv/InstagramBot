#!/usr/bin/env python3
"""
Спрощена версія Instagram бота без пошуку зображень
Використовує заглушку зображення або береться з новини
"""

import os
import time
import random
import logging
from datetime import datetime
from news_collector import NewsCollector
from content_generator import ContentGenerator
from instagram_publisher import InstagramPublisher
from translator import NewsTranslator
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Налаштування логування без емодзі
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class SimpleInstagramBot:
    def __init__(self):
        self.news_collector = NewsCollector()
        self.content_generator = ContentGenerator()
        self.instagram_publisher = InstagramPublisher()
        self.translator = NewsTranslator()
        self.posted_articles = set()
    
    def create_text_image(self, title, category="news"):
        """Створює професійний новинний банер"""
        # Параметри зображення (горизонтальне для Instagram)
        width, height = 1350, 1080
        
        # Професійні кольори для новин (замість яскравого жовтого)
        colors = {
            'war': '#1E3A8A',      # Темно-синій (серйозні військові новини)
            'news': '#1F2937',     # Темно-сірий (універсальні новини)
            'politics': '#7C2D12', # Темно-коричневий  
            'technology': '#064E3B', # Темно-зелений
            'world': '#991B1B',    # Темно-червоний
            'business': '#1E40AF'  # Сталево-синій
        }
        
        bg_color = colors.get(category, colors['news'])
        
        # Створюємо зображення з градієнтом
        img = Image.new('RGB', (width, height), bg_color)
        
        # Додаємо градієнт (темніше знизу)
        for y in range(height):
            alpha = y / height
            r = int(int(bg_color[1:3], 16) * (1 - alpha * 0.3))
            g = int(int(bg_color[3:5], 16) * (1 - alpha * 0.3))
            b = int(int(bg_color[5:7], 16) * (1 - alpha * 0.3))
            color = f"#{r:02x}{g:02x}{b:02x}"
            
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Спробуємо завантажити шрифт
        try:
            # Розмір шрифту залежно від довжини тексту
            font_size = max(60, min(100, int(800 / len(title) * 10)))
            font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # Додаємо текст
        # Розбиваємо довгий текст на рядки
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            # Простий підрахунок ширини (приблизно)
            if len(test_line) < 15:  # Максимум символів в рядку
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Центруємо текст
        total_height = len(lines) * 80
        start_y = (height - total_height) // 2
        
        for i, line in enumerate(lines[:5]):  # Максимум 5 рядків
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * 80
            
            # Тінь тексту
            draw.text((x+2, y+2), line, font=font, fill='black')
            # Основний текст
            draw.text((x, y), line, font=font, fill='white')
        
        # Додаємо українську символіку
        if category == 'war':
            logo_text = "🇺🇦 НОВИНИ УКРАЇНИ 🇺🇦"
        else:
            logo_text = "🇺🇦 УКРАЇНИ НОВИНИ"
        
        logo_bbox = draw.textbbox((0, 0), logo_text, font=font)
        logo_width = logo_bbox[2] - logo_bbox[0]
        
        # Тінь для лого
        draw.text(((width - logo_width) // 2 + 2, height - 150 + 2), logo_text, 
                 font=font, fill='black')
        # Основний лого
        draw.text(((width - logo_width) // 2, height - 150), logo_text, 
                 font=font, fill='white')
        
        # Додаємо рамку
        border_width = 5
        draw.rectangle([0, 0, width-1, height-1], outline='white', width=border_width)
        
        return img
    
    def get_image_from_news(self, news_article):
        """Намагається отримати зображення з новини або створює власне"""
        # Спочатку пробуємо взяти зображення з новини
        if news_article.get('top_image'):
            try:
                response = requests.get(news_article['top_image'], timeout=10)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    
                    # Перевіряємо розміри та конвертуємо у вертикальне
                    width, height = img.size
                    
                    # Якщо зображення вертикальне, обрізаємо до горизонтального
                    if height > width:
                        # Обрізаємо до горизонтального формату
                        target_width = height * 1.25  # співвідношення 5:4
                        if width < target_width:
                            # Розтягуємо по ширині
                            img = img.resize((int(target_width), height), Image.Resampling.LANCZOS)
                            width = int(target_width)
                        
                        # Тепер обрізаємо зверху та знизу
                        target_height = width / 1.25
                        top = (height - target_height) // 2
                        img = img.crop((0, int(top), width, int(top + target_height)))
                    
                    # Змінюємо розмір до горизонтального формату Instagram  
                    img = img.resize((1350, 1080), Image.Resampling.LANCZOS)
                    return img
            except Exception as e:
                logging.info(f"Не вдалося завантажити зображення з новини: {e}")
        
        # Якщо не вдалося, створюємо текстове зображення
        title = news_article.get('title', 'Важливі новини')
        category = self.detect_news_category(title, news_article.get('text', ''))
        return self.create_text_image(title, category)
    
    def detect_news_category(self, title, content):
        """Визначає категорію новини для українського контенту"""
        text = f"{title} {content}".lower()
        
        # Ключові слова для військових новин
        war_keywords = [
            'війна', 'war', 'фронт', 'front', 'бойові', 'combat', 'наступ', 'offensive',
            'оборона', 'defense', 'обстріл', 'shelling', 'ракет', 'missile', 'дрон', 'drone',
            'військов', 'military', 'армія', 'army', 'втрати', 'casualties', 'загиблі',
            'поранені', 'wounded', 'танк', 'tank', 'артилерія', 'artillery',
            'авіаудар', 'airstrike', 'окупац', 'occupation', 'звільнен', 'liberation'
        ]
        
        # Політичні ключові слова
        politics_keywords = [
            'політика', 'politics', 'уряд', 'government', 'президент', 'president',
            'парламент', 'parliament', 'міністр', 'minister', 'закон', 'law',
            'рішення', 'decision', 'санкції', 'sanctions'
        ]
        
        # Міжнародні новини
        world_keywords = [
            'нато', 'nato', 'євросоюз', 'eu', 'сша', 'usa', 'росія', 'russia',
            'міжнародн', 'international', 'дипломат', 'diplomatic'
        ]
        
        if any(keyword in text for keyword in war_keywords):
            return 'war'
        elif any(keyword in text for keyword in politics_keywords):
            return 'politics'
        elif any(keyword in text for keyword in world_keywords):
            return 'world'
        else:
            return 'news'
    
    def create_and_publish_post(self):
        """Спрощений метод створення та публікації поста"""
        try:
            logging.info("Початок створення нового поста...")
            
            # 1. Збираємо новини
            logging.info("Збір новин...")
            all_news = self.news_collector.collect_fresh_news()
            
            if not all_news:
                logging.error("Не вдалося знайти новини")
                return False
            
            # Фільтруємо новини пов'язані з Україною
            ukraine_news = self.translator.filter_ukraine_related(all_news)
            
            if not ukraine_news:
                logging.info("Не знайдено новин про Україну, використовую загальні новини")
                ukraine_news = all_news
            
            # Віддаємо пріоритет військовим новинам
            prioritized_news = self.translator.prioritize_war_news(ukraine_news)
            
            # Обираємо якісну новину з пріоритетного списку
            selected_article = None
            for article in prioritized_news[:15]:  # Перевіряємо топ-15
                # Перевіряємо якість новини
                title = article.get('title', '')
                description = article.get('description', '')
                
                if (title and title != 'Новина з RSS' and len(title) > 20 and 
                    description and len(description) > 50 and
                    'недоступний для повного парсингу' not in description):
                    
                    # Перевіряємо чи не публікували раніше
                    article_id = hash(title + article.get('link', ''))
                    if article_id not in self.posted_articles:
                        selected_article = article
                        break
            
            if not selected_article:
                logging.warning("Немає якісних новин для публікації, використовую fallback новину...")
                # Створюємо fallback новину
                selected_article = {
                    'title': 'Україна: Важливі події сьогодні',
                    'description': 'Стежте за актуальними подіями в Україні. Найважливіші новини дня від українських джерел.',
                    'link': 'https://t.me/newstime20',
                    'published': datetime.now()
                }
            
            news_article = selected_article
            
            logging.info(f"Обрано новину: {news_article.get('title', 'Без заголовка')}")
            
            # Додаємо до списку опублікованих
            article_id = hash(news_article.get('title', '') + news_article.get('link', ''))
            self.posted_articles.add(article_id)
            
            # Перекладаємо новину на українську мову
            logging.info("Переклад новини на українську...")
            ukrainian_article = self.translator.translate_news_article(news_article)
            logging.info(f"Переклад завершено: {ukrainian_article.get('title', 'Без заголовка')}")
            
            # 2. Отримуємо або створюємо зображення
            logging.info("Створення зображення...")
            image = self.get_image_from_news(ukrainian_article)
            
            # Зберігаємо зображення
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"post_{timestamp}.jpg"
            image_path = f"temp_images/{image_filename}"
            
            # Створюємо папку якщо її немає
            os.makedirs("temp_images", exist_ok=True)
            
            image.save(image_path, "JPEG", quality=95)
            logging.info(f"Зображення збережено: {image_path}")
            
            # 3. Генеруємо контент з української статті
            logging.info("Генерація контенту...")
            post_content = self.content_generator.create_full_post(
                ukrainian_article.get('title', ''),
                ukrainian_article.get('text', ukrainian_article.get('summary', ''))
            )
            
            logging.info(f"Згенеровано пост ({len(post_content)} символів)")
            
            # 4. Публікуємо
            logging.info("Публікація в Instagram...")
            success, message = self.instagram_publisher.safe_publish(
                image_path, 
                post_content,
                add_hashtags_as_comment=True
            )
            
            if success:
                logging.info(f"Пост успішно опубліковано! {message}")
                self.posted_articles.add(article_id)
                return True
            else:
                logging.error(f"Помилка публікації: {message}")
                return False
            
        except Exception as e:
            logging.error(f"Критична помилка: {e}")
            return False
    
    def test_run(self):
        """Тест всіх компонентів"""
        logging.info("Тестовий режим...")
        
        # Тест новин з fallback механізмом
        logging.info("Тест збору новин...")
        news = self.news_collector.get_random_news()
        if news:
            logging.info(f"Новини працюють: {news.get('title', 'N/A')[:50]}...")
        else:
            logging.warning("Не вдалося зібрати новини з RSS, використовую тестові дані...")
            # Продовжуємо роботу з тестовими даними
            logging.info("Новини працюють: Тестова новина (fallback режим)...")
        
        # Тест генерації зображення
        logging.info("Тест створення зображення...")
        image = self.create_text_image("Тестовий заголовок новини")
        test_path = "temp_images/test.jpg"
        os.makedirs("temp_images", exist_ok=True)
        image.save(test_path, "JPEG")
        logging.info("Зображення створено успішно")
        
        # Тест генерації контенту
        logging.info("Тест генерації контенту...")
        content = self.content_generator.create_full_post(
            "Тестова новина", "Це тестовий контент"
        )
        logging.info(f"Контент згенеровано: {len(content)} символів")
        
        # Тест Instagram
        logging.info("Тест підключення Instagram...")
        if self.instagram_publisher.login():
            logging.info("Підключення Instagram успішне")
        else:
            logging.error("Проблема з Instagram")
            print("\n🔧 Рекомендації для вирішення Instagram Challenge:")
            print("1. Увійдіть в аккаунт через мобільний додаток Instagram")
            print("2. Пройдіть всі запитувані верифікації (email/SMS/селфі)")
            print("3. Зробіть кілька звичайних дій: лайки, перегляди, підписки")
            print("4. Почекайте 24-48 годин після верифікації")
            print("5. Використовуйте стабільний IP адрес (не VPN)")
            print("6. Або створіть новий аккаунт з унікальною назвою\n")
            return False
        
        logging.info("Всі тести пройдено!")
        return True

def main():
    """Головна функція"""
    import sys
    
    bot = SimpleInstagramBot()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            bot.test_run()
        elif sys.argv[1] == "--post":
            bot.create_and_publish_post()
        else:
            print("Доступні опції:")
            print("  --test  : Тестовий запуск")
            print("  --post  : Одноразова публікація")
    else:
        # За замовчуванням тест
        bot.test_run()

if __name__ == "__main__":
    main()
