import schedule
import time
import random
import logging
from datetime import datetime, timedelta
from news_collector import NewsCollector
from image_handler import ImageHandler
from content_generator import ContentGenerator
from instagram_publisher import InstagramPublisher
from config import POSTING_INTERVALS

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_bot.log'),
        logging.StreamHandler()
    ]
)

class InstagramNewsBot:
    def __init__(self):
        self.news_collector = NewsCollector()
        self.image_handler = ImageHandler()
        self.content_generator = ContentGenerator()
        self.instagram_publisher = InstagramPublisher()
        self.posted_articles = set()  # Щоб не повторювати новини
        
    def create_and_publish_post(self):
        """Основний метод створення та публікації поста"""
        try:
            logging.info("🚀 Починаю створення нового поста...")
            
            # 1. Збираємо свіжі новини
            logging.info("📰 Збираю новини...")
            news_article = self.news_collector.get_random_news()
            
            if not news_article:
                logging.error("❌ Не вдалося знайти новини")
                return False
            
            # Перевіряємо чи не публікували цю новину раніше
            article_id = hash(news_article.get('title', '') + news_article.get('link', ''))
            if article_id in self.posted_articles:
                logging.info("⏭️ Ця новина вже була опублікована, шукаю іншу...")
                return self.create_and_publish_post()  # Рекурсивно шукаємо іншу
            
            logging.info(f"📄 Обрано новину: {news_article.get('title', 'Без заголовка')}")
            
            # 2. Шукаємо вертикальне зображення
            logging.info("🖼️ Шукаю підходяще вертикальне зображення...")
            image_data = self.image_handler.find_news_related_image(
                news_article.get('title', ''),
                news_article.get('text', news_article.get('summary', ''))
            )
            
            if not image_data:
                logging.error("❌ Не вдалося знайти підходяще зображення")
                return False
            
            logging.info(f"✅ Знайдено зображення: {image_data['source']} - {image_data['quality_check']}")
            
            # 3. Завантажуємо зображення
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"post_{timestamp}.jpg"
            image_path = self.image_handler.download_image(image_data['url'], image_filename)
            
            if not image_path:
                logging.error("❌ Не вдалося завантажити зображення")
                return False
            
            # 4. Генеруємо контент поста
            logging.info("✍️ Генерую контент поста...")
            post_content = self.content_generator.create_full_post(
                news_article.get('title', ''),
                news_article.get('text', news_article.get('summary', ''))
            )
            
            logging.info(f"📝 Згенеровано пост ({len(post_content)} символів)")
            
            # 5. Публікуємо в Instagram
            logging.info("📤 Публікую в Instagram...")
            success, message = self.instagram_publisher.safe_publish(
                image_path, 
                post_content,
                add_hashtags_as_comment=True
            )
            
            if success:
                logging.info(f"✅ Пост успішно опубліковано! {message}")
                self.posted_articles.add(article_id)
                
                # Отримуємо статистику аккаунту
                account_info = self.instagram_publisher.get_account_info()
                if account_info:
                    logging.info(f"📊 Статистика: {account_info['followers']} підписників, {account_info['posts']} постів")
                
                return True
            else:
                logging.error(f"❌ Помилка публікації: {message}")
                return False
            
        except Exception as e:
            logging.error(f"❌ Критична помилка: {e}")
            return False
    
    def test_run(self):
        """Тестовий запуск для перевірки всіх компонентів"""
        logging.info("🧪 Запуск тестового режиму...")
        
        # Тестуємо збір новин
        logging.info("Тестую збір новин...")
        news = self.news_collector.get_random_news()
        if news:
            logging.info(f"✅ Новини працюють: {news.get('title', 'N/A')}")
        else:
            logging.error("❌ Проблема зі збором новин")
            return False
        
        # Тестуємо генерацію контенту
        logging.info("Тестую генерацію контенту...")
        content = self.content_generator.create_full_post(
            "Тестова новина", 
            "Це тестовий контент для перевірки роботи генератора контенту."
        )
        logging.info(f"✅ Контент згенеровано: {len(content)} символів")
        
        # Тестуємо вхід в Instagram
        logging.info("Тестую вхід в Instagram...")
        if self.instagram_publisher.login():
            logging.info("✅ Вхід в Instagram успішний")
            account_info = self.instagram_publisher.get_account_info()
            if account_info:
                logging.info(f"✅ Аккаунт: @{account_info['username']}")
        else:
            logging.error("❌ Проблема з входом в Instagram")
            return False
        
        logging.info("🎉 Всі тести пройдено успішно!")
        return True
    
    def schedule_posts(self):
        """Налаштовує розклад публікацій"""
        def random_post_job():
            """Випадкова публікація з інтервалом 2-3 години"""
            self.create_and_publish_post()
            
            # Плануємо наступну публікацію через 2-3 години
            next_interval = random.choice(POSTING_INTERVALS)
            next_run = datetime.now() + timedelta(hours=next_interval)
            
            logging.info(f"⏰ Наступна публікація заплановано на: {next_run.strftime('%H:%M')}")
            
            # Очищуємо старі завдання та додаємо нове
            schedule.clear()
            schedule.every().day.at(next_run.strftime('%H:%M')).do(random_post_job)
        
        # Плануємо першу публікацію
        first_interval = random.choice(POSTING_INTERVALS)
        first_run = datetime.now() + timedelta(hours=first_interval)
        
        logging.info(f"⏰ Перша публікація заплановано на: {first_run.strftime('%H:%M')}")
        schedule.every().day.at(first_run.strftime('%H:%M')).do(random_post_job)
    
    def run_bot(self):
        """Запускає бота в постійному режимі"""
        logging.info("🤖 Запускаю Instagram News Bot...")
        
        # Спочатку тестуємо все
        if not self.test_run():
            logging.error("❌ Тести не пройдено, зупиняю бота")
            return
        
        # Налаштовуємо розклад
        self.schedule_posts()
        
        logging.info("✅ Бот запущено! Чекаю розкладу...")
        logging.info("Для зупинки натисніть Ctrl+C")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Перевіряємо кожну хвилину
                
        except KeyboardInterrupt:
            logging.info("👋 Зупинка бота...")
            self.instagram_publisher.logout()
            logging.info("✅ Бот зупинено")

def main():
    """Головна функція"""
    import sys
    
    bot = InstagramNewsBot()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # Тестовий режим
            bot.test_run()
        elif sys.argv[1] == "--post":
            # Одноразова публікація
            bot.create_and_publish_post()
        elif sys.argv[1] == "--run":
            # Постійний режим
            bot.run_bot()
        else:
            print("Доступні опції:")
            print("  --test  : Тестовий запуск")
            print("  --post  : Одноразова публікація")
            print("  --run   : Постійний режим роботи")
    else:
        # За замовчуванням запускаємо постійний режим
        bot.run_bot()

if __name__ == "__main__":
    main()
