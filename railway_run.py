#!/usr/bin/env python3
"""
Railway deployment runner для Instagram Ukrainian News Bot
"""

import os
import sys
import time
import logging
from datetime import datetime

# Налаштування логування для Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)  # Логи в консоль для Railway
    ]
)

def check_environment():
    """Перевіряє наявність змінних середовища"""
    required_vars = [
        'INSTAGRAM_USERNAME',
        'INSTAGRAM_PASSWORD', 
        'TELEGRAM_CHANNEL_LINK'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logging.error(f"Відсутні змінні середовища: {missing_vars}")
        logging.error("Налаштуйте змінні середовища в Railway Dashboard")
        return False
    
    logging.info("✅ Всі змінні середовища налаштовано!")
    return True

def main():
    """Головна функція для Railway"""
    logging.info("🚀 Запуск Instagram Ukrainian News Bot на Railway")
    logging.info("=" * 60)
    
    # Перевіряємо середовище
    if not check_environment():
        sys.exit(1)
    
    # Імпортуємо та запускаємо бота
    try:
        from simple_bot import SimpleInstagramBot
        
        bot = SimpleInstagramBot()
        
        # Спочатку тест
        logging.info("🧪 Тестування компонентів...")
        if not bot.test_run():
            logging.error("❌ Тести не пройдено")
            sys.exit(1)
        
        # Запускаємо постійний режим
        logging.info("✅ Тести пройдено, запускаю постійний режим...")
        
        import schedule
        import random
        
        def post_job():
            logging.info(f"📝 {datetime.now().strftime('%H:%M:%S')} - Створюю новий пост...")
            success = bot.create_and_publish_post()
            
            if success:
                logging.info("✅ Пост успішно опубліковано!")
            else:
                logging.error("❌ Помилка публікації")
            
            # Плануємо наступний пост
            next_hours = random.choice([2, 3])
            next_time = datetime.now().hour + next_hours
            if next_time >= 24:
                next_time -= 24
            
            logging.info(f"⏰ Наступна публікація о {next_time:02d}:00")
        
        # Перша публікація через 5 хвилин
        schedule.every(5).minutes.do(post_job)
        
        logging.info("🤖 Бот запущено на Railway!")
        logging.info("⏰ Перша публікація через 5 хвилин...")
        
        # Основний цикл
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except KeyboardInterrupt:
        logging.info("👋 Отримано сигнал зупинки...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"❌ Критична помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
