#!/usr/bin/env python3
"""
Простий скрипт для запуску Instagram News Bot
"""

import os
import sys
from main import InstagramNewsBot

def check_environment():
    """Перевіряє чи налаштовано всі необхідні змінні середовища"""
    required_vars = [
        'INSTAGRAM_USERNAME',
        'INSTAGRAM_PASSWORD', 
        'TELEGRAM_CHANNEL_LINK',
        'OPENAI_API_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Відсутні необхідні змінні середовища:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Створіть файл .env та додайте всі необхідні змінні")
        print("   (дивіться env_example.txt для прикладу)")
        return False
    
    print("✅ Всі змінні середовища налаштовано!")
    return True

def main():
    print("🤖 Instagram News Bot - Запуск")
    print("=" * 40)
    
    # Перевіряємо середовище
    if not check_environment():
        sys.exit(1)
    
    # Створюємо та запускаємо бота
    bot = InstagramNewsBot()
    
    print("\n🚀 Запускаю бота...")
    print("   (Для зупинки натисніть Ctrl+C)")
    
    try:
        bot.run_bot()
    except KeyboardInterrupt:
        print("\n👋 Бота зупинено користувачем")
    except Exception as e:
        print(f"\n❌ Критична помилка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
