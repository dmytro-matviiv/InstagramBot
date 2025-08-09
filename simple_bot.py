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
        """Створює красивий читабельний новинний банер"""
        # Параметри зображення (горизонтальне для Instagram)
        width, height = 1350, 1080
        
        # Українські патріотичні кольори
        colors = {
            'war': ('#0057B7', '#FFD700'),      # Синій + жовтий український прапор
            'news': ('#2563EB', '#FFFFFF'),     # Синій + білий
            'politics': ('#DC2626', '#FFFFFF'), # Червоний + білий  
            'technology': ('#059669', '#FFFFFF'), # Зелений + білий
            'world': ('#7C3AED', '#FFFFFF'),    # Фіолетовий + білий
            'business': ('#EA580C', '#FFFFFF')  # Помаранчевий + білий
        }
        
        bg_color, text_color = colors.get(category, colors['news'])
        
        # Створюємо красивий градієнт фон
        img = Image.new('RGB', (width, height), bg_color)
        
        # Конвертуємо hex в RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        bg_rgb = hex_to_rgb(bg_color)
        
        # Створюємо вертикальний градієнт
        for y in range(height):
            alpha = y / height
            # Робимо градієнт від світлішого до темнішого
            r = int(bg_rgb[0] * (1 - alpha * 0.3))
            g = int(bg_rgb[1] * (1 - alpha * 0.3))
            b = int(bg_rgb[2] * (1 - alpha * 0.3))
            
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Завантажуємо кращий шрифт
        try:
            # Великий читабельний шрифт
            title_font = ImageFont.truetype("arial.ttf", 58)
        except IOError:
            title_font = ImageFont.load_default()
        
        # Скорочуємо заголовок якщо занадто довгий
        if len(title) > 50:
            title = title[:47] + "..."
        
        # Розбиваємо на рядки (максимум 3 рядки)
        words = title.split()
        lines = []
        current_line = []
        max_chars_per_line = 20
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= max_chars_per_line:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
        
        # Обмежуємо до 3 рядків
        lines = lines[:3]
        
        # Центруємо текст
        line_height = 80
        total_text_height = len(lines) * line_height
        start_y = (height - total_text_height) // 2 - 50
        
        # Конвертуємо колір тексту в RGB
        text_rgb = hex_to_rgb(text_color) if text_color != '#FFFFFF' else (255, 255, 255)
        
        # Малюємо кожен рядок
        for i, line in enumerate(lines):
            # Центруємо горизонтально
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * line_height
            
            # Контрастна тінь для читабельності
            shadow_color = (0, 0, 0) if text_color == '#FFFFFF' else (255, 255, 255)
            draw.text((x+3, y+3), line, font=title_font, fill=shadow_color)
            # Основний текст
            draw.text((x, y), line, font=title_font, fill=text_rgb)
        
        # Додаємо українську символіку
        if category == 'war':
            logo_text = "🇺🇦 НОВИНИ УКРАЇНИ 🇺🇦"
        else:
            logo_text = "🇺🇦 УКРАЇНИ НОВИНИ"
        
        logo_bbox = draw.textbbox((0, 0), logo_text, font=title_font)
        logo_width = logo_bbox[2] - logo_bbox[0]
        
        # Тінь для лого
        draw.text(((width - logo_width) // 2 + 2, height - 120 + 2), logo_text, 
                 font=title_font, fill=(0, 0, 0))
        # Основний лого
        draw.text(((width - logo_width) // 2, height - 120), logo_text, 
                 font=title_font, fill=(255, 255, 255))
        
        # Додаємо рамку
        border_width = 5
        draw.rectangle([0, 0, width-1, height-1], outline='white', width=border_width)
        
        return img
    
    def create_vertical_text_image(self, title, category="news"):
        """Створює вертикальне текстове зображення для Instagram Stories"""
        # Параметри вертикального зображення для Instagram Stories (9:16)
        width, height = 1080, 1920
        
        # Українські патріотичні кольори
        colors = {
            'war': ('#0057B7', '#FFD700'),      # Синій + жовтий український прапор
            'news': ('#2563EB', '#FFFFFF'),     # Синій + білий
            'politics': ('#DC2626', '#FFFFFF'), # Червоний + білий  
            'technology': ('#059669', '#FFFFFF'), # Зелений + білий
            'world': ('#7C3AED', '#FFFFFF'),    # Фіолетовий + білий
            'business': ('#EA580C', '#FFFFFF')  # Помаранчевий + білий
        }
        
        bg_color, text_color = colors.get(category, colors['news'])
        
        # Створюємо вертикальний фон
        img = Image.new('RGB', (width, height), bg_color)
        
        # Конвертуємо hex в RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        bg_rgb = hex_to_rgb(bg_color)
        
        # Створюємо вертикальний градієнт
        for y in range(height):
            alpha = y / height
            r = int(bg_rgb[0] * (1 - alpha * 0.2))
            g = int(bg_rgb[1] * (1 - alpha * 0.2))
            b = int(bg_rgb[2] * (1 - alpha * 0.2))
            
            for x in range(width):
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Завантажуємо шрифт
        try:
            title_font = ImageFont.truetype("arial.ttf", 72)
            subtitle_font = ImageFont.truetype("arial.ttf", 48)
        except IOError:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Скорочуємо заголовок
        if len(title) > 60:
            title = title[:57] + "..."
        
        # Розбиваємо на рядки для вертикального формату
        words = title.split()
        lines = []
        current_line = []
        max_chars_per_line = 18  # Менше символів для вертикального формату
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if len(test_line) <= max_chars_per_line:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
        
        # Обмежуємо до 4 рядків для вертикального формату
        lines = lines[:4]
        
        # Центруємо текст у верхній половині
        line_height = 90
        total_text_height = len(lines) * line_height
        start_y = (height // 3) - (total_text_height // 2)
        
        # Конвертуємо колір тексту
        text_rgb = hex_to_rgb(text_color) if text_color != '#FFFFFF' else (255, 255, 255)
        
        # Малюємо кожен рядок
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = start_y + i * line_height
            
            # Контрастна тінь
            shadow_color = (0, 0, 0) if text_color == '#FFFFFF' else (255, 255, 255)
            draw.text((x+3, y+3), line, font=title_font, fill=shadow_color)
            # Основний текст
            draw.text((x, y), line, font=title_font, fill=text_rgb)
        
        # Додаємо українську символіку внизу
        if category == 'war':
            logo_text = "🇺🇦 НОВИНИ УКРАЇНИ 🇺🇦"
        else:
            logo_text = "🇺🇦 УКРАЇНА СЬОГОДНІ 🇺🇦"
        
        logo_bbox = draw.textbbox((0, 0), logo_text, font=subtitle_font)
        logo_width = logo_bbox[2] - logo_bbox[0]
        
        # Логотип внизу
        logo_y = height - 200
        draw.text(((width - logo_width) // 2 + 2, logo_y + 2), logo_text, 
                 font=subtitle_font, fill=(0, 0, 0))
        draw.text(((width - logo_width) // 2, logo_y), logo_text, 
                 font=subtitle_font, fill=(255, 255, 255))
        
        # Додаємо рамку
        border_width = 8
        draw.rectangle([0, 0, width-1, height-1], outline='white', width=border_width)
        
        return img
    
    def get_image_from_news(self, news_article):
        """Отримує реальне зображення з новини та конвертує у вертикальний формат"""
        # Спочатку пробуємо взяти реальне зображення з новини
        image_urls = []
        if news_article.get('top_image'):
            image_urls.append(news_article['top_image'])
        if news_article.get('images'):
            image_urls.extend(news_article['images'][:3])  # Перші 3 зображення
            
        for image_url in image_urls:
            try:
                logging.info(f"Завантажую реальне зображення: {image_url}")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(image_url, timeout=15, headers=headers)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    
                    # Перевіряємо якість зображення
                    width, height = img.size
                    if width < 300 or height < 300:
                        continue  # Пропускаємо маленькі зображення
                    
                    logging.info(f"Оригінальне зображення: {width}x{height}")
                    
                    # Конвертуємо у вертикальний формат для Instagram Stories (9:16)
                    target_width = 1080
                    target_height = 1920
                    
                    # Якщо зображення горизонтальне, робимо його квадратним
                    if width > height:
                        # Обрізаємо до квадрату (беремо центральну частину)
                        crop_size = min(width, height)
                        left = (width - crop_size) // 2
                        top = (height - crop_size) // 2
                        img = img.crop((left, top, left + crop_size, top + crop_size))
                        logging.info(f"Обрізано до квадрату: {crop_size}x{crop_size}")
                    
                    # Масштабуємо до вертикального формату
                    img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                    logging.info(f"Фінальний розмір: {target_width}x{target_height}")
                    return img
                    
            except Exception as e:
                logging.warning(f"Помилка завантаження {image_url}: {e}")
                continue
        
        # Якщо не знайшли жодного зображення, повертаємо None
        logging.warning("Не знайдено жодного придатного зображення в новині")
        return None
    
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
            
            # Якщо RSS не працює - припиняємо роботу (потрібні тільки реальні новини з фото)
            if not all_news:
                logging.error("RSS джерела недоступні і fallback заборонено. Неможливо знайти новини з фото.")
                return False
            
            # Фільтруємо новини пов'язані з Україною
            ukraine_news = self.translator.filter_ukraine_related(all_news)
            
            if not ukraine_news:
                logging.info("Не знайдено новин про Україну, використовую загальні новини")
                ukraine_news = all_news
            
            # Віддаємо пріоритет військовим новинам
            prioritized_news = self.translator.prioritize_war_news(ukraine_news)
            
            # Обираємо новину з фото - перевіряємо послідовно до знаходження
            selected_article = None
            for article in prioritized_news[:30]:  # Перевіряємо більше новин
                # Перевіряємо якість новини
                title = article.get('title', '')
                description = article.get('description', '')
                
                if (title and title != 'Новина з RSS' and len(title) > 20 and 
                    description and len(description) > 50 and
                    'недоступний для повного парсингу' not in description):
                    
                    # Перевіряємо чи не публікували раніше
                    article_id = hash(title + article.get('link', ''))
                    if article_id not in self.posted_articles:
                        
                        # ГОЛОВНЕ: Перевіряємо чи є фото в новині
                        logging.info(f"Перевіряю наявність фото в новині: {title[:50]}...")
                        test_image = self.get_image_from_news(article)
                        
                        if test_image is not None:
                            logging.info("✅ Знайдено новину з фото!")
                            selected_article = article
                            break
                        else:
                            logging.info("❌ Новина без фото, перевіряю наступну...")
            
            if not selected_article:
                logging.error("Не знайдено жодної новини з фото! Потрібно змінити RSS джерела")
                return False
            
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
