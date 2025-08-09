#!/usr/bin/env python3
"""
Постійний запуск Instagram бота
"""

import time
import random
import schedule
from datetime import datetime
from simple_bot import SimpleInstagramBot

def run_posting_job():
    """Функція для публікації постів"""
    bot = SimpleInstagramBot()
    
    print(f"\n🚀 {datetime.now().strftime('%H:%M:%S')} - Створюю новий пост...")
    
    success = bot.create_and_publish_post()
    
    if success:
        print("✅ Пост успішно опубліковано!")
    else:
        print("❌ Помилка публікації")
    
    # Плануємо наступну публікацію через 2-3 години
    next_hours = random.choice([2, 3])
    next_time = datetime.now().hour + next_hours
    if next_time >= 24:
        next_time -= 24
    
    print(f"⏰ Наступна публікація о {next_time:02d}:00")

def main():
    print("🤖 Instagram News Bot - Постійна робота")
    print("=" * 50)
    print("Публікація кожні 2-3 години")
    print("Для зупинки натисніть Ctrl+C")
    print("=" * 50)
    
    # Перший пост через 5 хвилин після запуску
    print("⏰ Перший пост через 5 хвилин...")
    schedule.every(5).minutes.do(run_posting_job)
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Перевіряємо кожну хвилину
            
    except KeyboardInterrupt:
        print("\n👋 Зупинка бота...")
        print("✅ Бот зупинено")

if __name__ == "__main__":
    main()
