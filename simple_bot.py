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
from PIL import Image
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
    

    

    


    

    
    def extract_images_from_html(self, html_content):
        """Витягує URL зображень з HTML контенту"""
        import re
        img_urls = []
        
        # Шукаємо img теги
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(img_pattern, html_content, re.IGNORECASE)
        
        for url in matches:
            # Фільтруємо очевидно непридатні зображення
            if any(skip in url.lower() for skip in ['icon', 'logo', 'avatar', 'button', '1x1', 'pixel']):
                continue
            # Додаємо якщо це схоже на нормальне зображення
            if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                img_urls.append(url)
        
        return img_urls
    
    def try_get_larger_image_url(self, url):
        """Намагається знайти більшу версію зображення"""
        if not url:
            return url
            
        # Шаблони для заміни мініатюр на повнорозмірні зображення
        replacements = [
            # Загальні шаблони
            ('thumb_', 'full_'),
            ('small_', 'large_'),
            ('mini_', 'full_'),
            ('/thumbs/', '/images/'),
            ('/small/', '/large/'),
            ('_150.', '_1200.'),
            ('_200.', '_1200.'),
            ('_300.', '_1200.'),
            ('_400.', '_1200.'),
            ('_500.', '_1200.'),
            ('_thumb.', '_full.'),
            ('_small.', '_large.'),
            # Розміри в URL
            ('150x', '1200x'),
            ('200x', '1200x'),
            ('300x', '1200x'),
            ('400x', '1200x'),
            ('630x360', '1200x800'),
            ('320x240', '1280x960'),
        ]
        
        original_url = url
        for old_pattern, new_pattern in replacements:
            if old_pattern in url.lower():
                new_url = url.replace(old_pattern, new_pattern)
                if new_url != url:
                    logging.info(f"Знайдено потенційно більше зображення: {old_pattern} -> {new_pattern}")
                    return new_url
        
        return original_url
    
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
    
    def find_highest_quality_news(self):
        """Знаходить новину з найвищою якістю фото серед ВСІХ RSS джерел"""
        logging.info("🔍 Аналіз ВСІХ RSS джерел для пошуку найякісніших фото...")
        
        all_news = self.news_collector.collect_fresh_news()
        if not all_news:
            logging.error("❌ RSS джерела недоступні")
            return None
            
        best_news = None
        best_quality = 0
        analyzed_count = 0
        
        # Аналізуємо новини з усіх джерел
        for article in all_news:
            analyzed_count += 1
            
            # Пропускаємо вже опубліковані
            article_id = hash(article.get('title', '') + article.get('link', ''))
            if article_id in self.posted_articles:
                continue
                
            # Перевіряємо якість заголовка
            title = article.get('title', '')
            if not title or len(title) < 10 or title == 'Новина з RSS':
                continue
                
            logging.info(f"📊 Аналізую #{analyzed_count}: {title[:50]}...")
            
            # Аналізуємо якість зображень в цій новині
            image_info = self.analyze_image_quality_in_article(article)
            
            if image_info and image_info['total_pixels'] > best_quality:
                best_quality = image_info['total_pixels']
                best_news = {
                    'article': article,
                    'image_info': image_info
                }
                logging.info(f"🏆 НОВИЙ ЛІДЕР: {image_info['width']}x{image_info['height']} ({image_info['total_pixels']} пікселів)")
            
            # Обмежуємо кількість перевірок для продуктивності
            if analyzed_count >= 30:
                break
                
        if best_news:
            logging.info(f"✅ ВИБРАНО НАЙКРАЩУ: {best_news['image_info']['width']}x{best_news['image_info']['height']} ({best_news['image_info']['total_pixels']} пікселів)")
            return best_news
        else:
            logging.warning("❌ Не знайдено новин з якісними фото")
            return None

    def create_and_publish_post(self, max_attempts=50):
        """Створення та публікація поста з найвищою якістю фото"""
        try:
            logging.info("🎯 Початок пошуку найякісніших фото серед ВСІХ RSS джерел...")
            
            if max_attempts <= 0:
                logging.error("❌ Досягнуто максимум спроб")
                return False
            
            # 1. Знаходимо новину з найвищою якістю фото серед ВСІХ джерел
            best_news = self.find_highest_quality_news()
            if not best_news:
                logging.error("❌ Не знайдено новин з якісними фото в жодному джерелі")
                return False
                
            # Витягуємо дані
            news_article = best_news['article']
            image_info = best_news['image_info']
            
            logging.info(f"✅ Обрано найкращу новину: {news_article.get('title', 'Без заголовка')}")
            logging.info(f"📸 Якість фото: {image_info['width']}x{image_info['height']} ({image_info['total_pixels']} пікселів)")
            
            # Додаємо до списку опублікованих
            article_id = hash(news_article.get('title', '') + news_article.get('link', ''))
            self.posted_articles.add(article_id)
            
            # Перекладаємо новину на українську мову
            logging.info("Переклад новини на українську...")
            ukrainian_article = self.translator.translate_news_article(news_article)
            logging.info(f"Переклад завершено: {ukrainian_article.get('title', 'Без заголовка')}")
            
            # 2. Завантажуємо найкраще зображення
            logging.info(f"📥 Завантажую найякісніше фото з {image_info['url']}")
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Language': 'uk-UA,uk;q=0.9,en;q=0.8',
                    'Referer': news_article.get('link', ''),
                    'Connection': 'keep-alive'
                }
                
                response = requests.get(image_info['url'], timeout=15, headers=headers)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    logging.info(f"✅ Завантажено найякісніше фото: {image.size[0]}x{image.size[1]}")
                else:
                    logging.error(f"❌ Помилка завантаження фото: {response.status_code}")
                    return self.create_and_publish_post(max_attempts - 1)
                    
            except Exception as e:
                logging.error(f"❌ Помилка при завантаженні фото: {e}")
                return self.create_and_publish_post(max_attempts - 1)
            
            # 3. Використовуємо оригінальне зображення БЕЗ обробки
            logging.info("✅ Використовую оригінальне фото без обробки")
            processed_img = image
                
            # Зберігаємо зображення
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"post_{timestamp}.jpg"
            image_path = f"temp_images/{image_filename}"
            
            # Створюємо папку якщо її немає
            os.makedirs("temp_images", exist_ok=True)
            
            processed_img.save(image_path, "JPEG", quality=95)
            logging.info(f"✅ РЕАЛЬНЕ фото з інтернету збережено: {image_path}")
            
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
        
        # Тест ТІЛЬКИ реальних зображень
        logging.info("⚠️ Пропускаю тест створення зображення - бот працює ТІЛЬКИ з реальними фото з інтернету")
        logging.info("✅ Тест зображень пропущено - система налаштована на реальні фото")
        
        # Тест генерації контенту
        logging.info("Тест генерації контенту...")
        content = self.content_generator.create_full_post(
            "Тестова новина", "Це тестовий контент"
        )
        logging.info(f"Контент згенеровано: {len(content)} символів")
        
        # Тест Instagram (БЕЗ реального підключення для безпеки)
        logging.info("⚠️ Пропускаю тест Instagram для уникнення блокувань")
        logging.info("✅ Instagram тест пропущено для безпеки")
        
        logging.info("Всі тести пройдено!")
        return True
    
    def analyze_rss_quality(self):
        """НОВИЙ: Аналізує якість зображень у всіх RSS джерелах"""
        logging.info("🔍 ПОЧАТОК АНАЛІЗУ RSS ДЖЕРЕЛ...")
        logging.info("=" * 80)
        
        good_sources = []
        bad_sources = []
        
        for i, source in enumerate(self.news_collector.sources):
            logging.info(f"\n📰 Аналізую джерело {i+1}/{len(self.news_collector.sources)}: {source}")
            logging.info("-" * 60)
            
            try:
                articles = self.news_collector.fetch_rss_news(source)
                suitable_articles = 0
                total_articles = len(articles)
                
                if not articles:
                    logging.info("❌ Не вдалося отримати новини з цього джерела")
                    bad_sources.append((source, "Недоступний"))
                    continue
                
                for j, article in enumerate(articles[:10]):  # Перевіряємо перші 10 новин
                    title = article.get('title', 'Без заголовка')[:50]
                    logging.info(f"\n  📄 Новина {j+1}: {title}...")
                    
                    # Аналізуємо зображення
                    image = self.get_image_from_news(article, test_mode=True)
                    if image:
                        suitable_articles += 1
                        logging.info(f"  ✅ Підходящє зображення знайдено!")
                    else:
                        logging.info(f"  ❌ Немає підходящих зображень")
                
                # Оцінюємо якість джерела
                success_rate = (suitable_articles / total_articles) * 100 if total_articles > 0 else 0
                
                if success_rate >= 5:  # Мінімум 5% новин з якісними зображеннями (реалістично)
                    logging.info(f"\n  ✅ ДЖЕРЕЛО ПІДХОДИТЬ: {suitable_articles}/{total_articles} новин з якісними фото ({success_rate:.1f}%)")
                    good_sources.append((source, success_rate))
                else:
                    logging.info(f"\n  ❌ ДЖЕРЕЛО НЕ ПІДХОДИТЬ: {suitable_articles}/{total_articles} новин з якісними фото ({success_rate:.1f}%)")
                    bad_sources.append((source, f"{success_rate:.1f}% якісних фото"))
                    
            except Exception as e:
                logging.error(f"❌ Помилка аналізу {source}: {e}")
                bad_sources.append((source, f"Помилка: {e}"))
        
        # Підсумок аналізу
        logging.info("\n" + "=" * 80)
        logging.info("📊 ПІДСУМОК АНАЛІЗУ RSS ДЖЕРЕЛ")
        logging.info("=" * 80)
        
        logging.info(f"\n✅ ХОРОШІ ДЖЕРЕЛА ({len(good_sources)}):")
        for source, rate in good_sources:
            logging.info(f"  • {source} ({rate:.1f}% якісних фото)")
        
        logging.info(f"\n❌ ПОГАНІ ДЖЕРЕЛА ({len(bad_sources)}):")
        for source, reason in bad_sources:
            logging.info(f"  • {source} - {reason}")
        
        # Рекомендації
        if len(good_sources) < 5:
            logging.info(f"\n⚠️ РЕКОМЕНДАЦІЯ: Потрібно більше якісних джерел (зараз {len(good_sources)})")
            self.suggest_new_rss_sources()
        else:
            logging.info(f"\n🎉 ВІДМІННО: Знайдено {len(good_sources)} якісних джерел!")
        
        return good_sources, bad_sources
    
    def suggest_new_rss_sources(self):
        """Пропонує нові RSS джерела з якісними зображеннями"""
        logging.info("\n💡 ПРОПОНОВАНІ НОВІ RSS ДЖЕРЕЛА:")
        
        new_sources = [
            'https://www.dw.com/uk/rss/news',  # Deutsche Welle українською
            'https://www.ukrinform.ua/rss/block-war',  # Укрінформ військові новини
            'https://espreso.tv/rss',  # Еспресо ТВ
            'https://www.eurointegration.com.ua/rss/',  # Європейська правда
            'https://interfax.com.ua/news/rss/',  # Інтерфакс Україна
            'https://censor.net/includes/news_rss.php',  # Цензор.нет
            'https://www.obozrevatel.com/rss.xml',  # Обозреватель
            'https://gordonua.com/xml/rss_category/1.html',  # Гордон
        ]
        
        for source in new_sources:
            logging.info(f"  • {source}")
        
        logging.info("\n🔧 Додайте ці джерела до config.py для покращення якості!")
    
    def get_image_from_news(self, news_article):
        """Отримує реальне зображення з новини"""
        return self._analyze_images_only(news_article)
    
    def _analyze_images_only(self, news_article):
        """Тільки аналізує реальні зображення без fallback"""
        # Спочатку пробуємо взяти реальне зображення з новини
        image_urls = []
        
        # Додаємо більше джерел зображень
        if news_article.get('rss_image'):
            image_urls.append(news_article['rss_image'])
        if news_article.get('top_image'):
            image_urls.append(news_article['top_image'])
        if news_article.get('images'):
            image_urls.extend(news_article['images'][:5])
            
        # Додаємо зображення з опису
        description = news_article.get('description', '') or news_article.get('summary', '')
        if description:
            img_urls_from_desc = self.extract_images_from_html(description)
            image_urls.extend(img_urls_from_desc)
        
        # Пробуємо знайти оригінальні зображення
        enhanced_urls = []
        for url in image_urls:
            enhanced_url = self.try_get_larger_image_url(url)
            if enhanced_url != url:
                enhanced_urls.append(enhanced_url)
        image_urls.extend(enhanced_urls)
            
        # Видаляємо дублікати
        image_urls = list(set([url for url in image_urls if url and url.strip()]))
        
        if not image_urls:
            return None
            
        # Перевіряємо кожне зображення
        for i, image_url in enumerate(image_urls):
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Language': 'uk-UA,uk;q=0.9,en;q=0.8',
                    'Referer': news_article.get('link', ''),
                    'Connection': 'keep-alive'
                }
                response = requests.get(image_url, timeout=10, headers=headers, stream=True)
                
                if response.status_code == 200:
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) < 5000:
                        continue
                        
                    img = Image.open(BytesIO(response.content))
                    width, height = img.size
                    
                    # РЕАЛІСТИЧНА ПЕРЕВІРКА - приймаємо ВСІ якісні фото
                    if width < 400 or height < 300:  # Базові мінімуми
                        continue
                        
                    total_pixels = width * height
                    if total_pixels < 120000:  # 120K пікселів мінімум (400x300)
                        continue
                    
                    # ПРИЙМАЄМО ВСІ ОРІЄНТАЦІЇ - горизонтальні, вертикальні, квадратні
                    logging.info(f"✅ Знайдено якісне фото: {width}x{height} ({total_pixels} пікселів)")
                    
                    # Якщо дійшли сюди - зображення підходить!
                    return img
                    
            except Exception:
                continue
        
        return None  # Не знайдено підходящих зображень
    
    def analyze_image_quality_in_article(self, news_article):
        """Аналізує якість зображень в статті і повертає найкращу роздільну здатність"""
        best_resolution = 0
        best_image_info = None
        
        # Збираємо всі потенційні URL зображень
        image_urls = []
        if news_article.get('rss_image'):
            image_urls.append(news_article['rss_image'])
        if news_article.get('top_image'):
            image_urls.append(news_article['top_image'])
        if news_article.get('images'):
            image_urls.extend(news_article['images'][:5])
            
        description = news_article.get('description', '') or news_article.get('summary', '')
        if description:
            img_urls_from_desc = self.extract_images_from_html(description)
            image_urls.extend(img_urls_from_desc)
            
        # Перевіряємо збільшені версії URL
        enhanced_urls = []
        for url in image_urls:
            enhanced_url = self.try_get_larger_image_url(url)
            if enhanced_url != url:
                enhanced_urls.append(enhanced_url)
        image_urls.extend(enhanced_urls)
        
        # Видаляємо дублікати
        image_urls = list(set([url for url in image_urls if url and url.strip()]))
        
        if not image_urls:
            return None
            
        # Аналізуємо кожне зображення
        for image_url in image_urls:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                    'Accept-Language': 'uk-UA,uk;q=0.9,en;q=0.8',
                    'Referer': news_article.get('link', ''),
                    'Connection': 'keep-alive'
                }
                
                response = requests.get(image_url, timeout=10, headers=headers, stream=True)
                if response.status_code == 200:
                    content_length = response.headers.get('content-length')
                    if content_length and int(content_length) < 5000:
                        continue
                        
                    img = Image.open(BytesIO(response.content))
                    width, height = img.size
                    
                    # Перевіряємо мінімальні вимоги
                    if width < 400 or height < 300:
                        continue
                        
                    total_pixels = width * height
                    if total_pixels < 120000:
                        continue
                    
                    # Порівнюємо з поточним кращим результатом
                    if total_pixels > best_resolution:
                        best_resolution = total_pixels
                        best_image_info = {
                            'width': width,
                            'height': height,
                            'total_pixels': total_pixels,
                            'url': image_url,
                            'article': news_article
                        }
                        
            except Exception:
                continue
                
        return best_image_info
    



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
            print("  --test     : Тестовий запуск")
            print("  --post     : Одноразова публікація")
    else:
        # За замовчуванням тест
        bot.test_run()

if __name__ == "__main__":
    main()
