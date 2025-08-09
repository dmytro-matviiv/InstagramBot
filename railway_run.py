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
    # Спочатку перевіряємо звичайні змінні
    required_vars = {
        'INSTAGRAM_USERNAME': 'globalno2025',
        'INSTAGRAM_PASSWORD': 'Dimka2015780',
        'TELEGRAM_CHANNEL_LINK': 'https://t.me/newstime20'
    }
    
    # Встановлюємо змінні якщо їх немає
    for var, default_value in required_vars.items():
        if not os.getenv(var):
            os.environ[var] = default_value
            logging.info(f"🔧 Встановлено змінну {var}")
    
    # Встановлюємо порожній OPENAI_API_KEY якщо його немає
    if not os.getenv('OPENAI_API_KEY'):
        os.environ['OPENAI_API_KEY'] = ''
        logging.info("🔧 Встановлено порожню змінну OPENAI_API_KEY (використовуємо локальний генератор)")
    
    # Перевіряємо ще раз
    missing_vars = []
    for var in required_vars.keys():
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logging.error(f"Відсутні змінні середовища: {missing_vars}")
        return False
    
    logging.info("✅ Всі змінні середовища налаштовано!")
    logging.info(f"Instagram: {os.getenv('INSTAGRAM_USERNAME')}")
    logging.info(f"Telegram: {os.getenv('TELEGRAM_CHANNEL_LINK')}")
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
        # Спробуємо виправити проблему з lxml
        try:
            import lxml_html_clean
            logging.info("✅ lxml_html_clean завантажено")
        except ImportError:
            logging.warning("⚠️ lxml_html_clean не знайдено, але це не критично")
        
        from simple_bot import SimpleInstagramBot
        
        bot = SimpleInstagramBot()
        
        # Спочатку тест
        logging.info("🧪 Тестування компонентів...")
        if not bot.test_run():
            logging.error("❌ Тести не пройдено")
            sys.exit(1)
        
        # Запускаємо постійний режим
        logging.info("✅ Тести пройдено, запускаю постійний режим...")
        
        logging.info("🤖 Бот запущено на Railway!")
        logging.info("🚀 Перша публікація зараз...")
        
        # Перша публікація одразу
        success = bot.create_and_publish_post()
        if success:
            logging.info("✅ Перший пост успішно опубліковано!")
        else:
            logging.error("❌ Помилка першої публікації")
        
        # Основний цикл з інтервалом 3000 секунд (50 хвилин)
        while True:
            logging.info("⏰ Наступна публікація через 50 хвилин (3000 секунд)...")
            time.sleep(3000)  # 50 хвилин = 3000 секунд
            
            logging.info(f"📝 {datetime.now().strftime('%H:%M:%S')} - Створюю новий пост...")
            success = bot.create_and_publish_post()
            
            if success:
                logging.info("✅ Пост успішно опубліковано!")
            else:
                logging.error("❌ Помилка публікації")
            
    except KeyboardInterrupt:
        logging.info("👋 Отримано сигнал зупинки...")
        sys.exit(0)
    except Exception as e:
        logging.error(f"❌ Критична помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
