#!/usr/bin/env python3
"""
Instagram Challenge Solver - допомагає вирішувати challenge для входу в Instagram
"""

import os
import time
from instagrapi import Client
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

class InstagramChallengeSolver:
    def __init__(self):
        self.client = Client()
        self.username = INSTAGRAM_USERNAME
        self.password = INSTAGRAM_PASSWORD
    
    def manual_login_guide(self):
        """Покрокова інструкція для ручного входу"""
        print("\n🔧 ПОКРОКОВА ІНСТРУКЦІЯ ВИРІШЕННЯ INSTAGRAM CHALLENGE")
        print("=" * 60)
        
        print("\n📱 Крок 1: Ручний вхід через мобільний додаток")
        print(f"   - Відкрийте Instagram на телефоні")
        print(f"   - Увійдіть з аккаунт: {self.username}")
        print(f"   - Пароль: {self.password}")
        
        print("\n🔐 Крок 2: Пройдіть верифікацію")
        print("   - Оберіть спосіб: Email або SMS")
        print("   - Введіть код підтвердження")
        print("   - Якщо потрібно - зробіть селфі")
        
        print("\n🎯 Крок 3: Активність аккаунту")
        print("   - Поставте 5-10 лайків")
        print("   - Подивіться кілька Stories")
        print("   - Підпишіться на 2-3 аккаунти")
        print("   - Зробіть один коментар")
        
        print("\n⏰ Крок 4: Очікування")
        print("   - Залиште аккаунт активним на 24 години")
        print("   - Не використовуйте VPN")
        print("   - Періодично заходьте в додаток")
        
        print("\n🤖 Крок 5: Тест бота")
        print("   - Через 24 години запустіть: python simple_bot.py --test")
        print("   - Бот має успішно авторизуватися")
        
        print("\n" + "=" * 60)
        print("✅ Після виконання всіх кроків challenge має зникнути!")
    
    def try_session_recovery(self):
        """Спроба відновлення через збережену сесію"""
        session_file = "instagram_session.json"
        
        if os.path.exists(session_file):
            try:
                print("🔄 Спроба відновлення сесії...")
                self.client.load_settings(session_file)
                
                # Спроба простого запиту для перевірки сесії
                account_info = self.client.account_info()
                print(f"✅ Сесія відновлена! Аккаунт: {account_info.username}")
                return True
                
            except Exception as e:
                print(f"❌ Сесія не працює: {e}")
                # Видаляємо неробочу сесію
                os.remove(session_file)
                print("🗑️ Видалено неробочу сесію")
        
        return False
    
    def test_challenge_status(self):
        """Перевіряє чи ще діє challenge"""
        try:
            print(f"🧪 Тестування challenge для {self.username}...")
            self.client.login(self.username, self.password)
            print("✅ Challenge вирішено! Вхід успішний!")
            return True
            
        except Exception as e:
            error_msg = str(e)
            if "ChallengeResolve" in error_msg:
                print("❌ Challenge все ще активний")
                return False
            else:
                print(f"❌ Інша помилка: {error_msg}")
                return False
    
    def create_new_account_guide(self):
        """Інструкція створення нового аккаунту"""
        print("\n🆕 СТВОРЕННЯ НОВОГО INSTAGRAM АККАУНТУ")
        print("=" * 50)
        
        suggestions = [
            "ukraine_news_bot_2025",
            "ua_military_news",
            "ukraine_war_updates", 
            "newsukraine_official",
            "ukrainian_frontline_news"
        ]
        
        print("\n📝 Рекомендовані username:")
        for i, name in enumerate(suggestions, 1):
            print(f"   {i}. {name}")
        
        print(f"\n🔐 Рекомендований пароль: UkraineNews2025!")
        print(f"📧 Email: [ваш_email]@gmail.com")
        print(f"📱 Телефон: ваш номер для верифікації")
        
        print("\n🎯 Налаштування профілю:")
        print("   - Назва: Ukraine News 2025 🇺🇦")
        print("   - Біо: Військові новини України 🇺🇦 | t.me/newstime20")
        print("   - Аватар: прапор України або військова символіка")
        
        print("\n⚠️ Важливо:")
        print("   - Не використовуйте VPN при створенні")
        print("   - Підтвердіть email і номер телефону")
        print("   - Зробіть аккаунт публічним")
        print("   - Почекайте 24 години перед використанням API")

def main():
    """Головна функція для вирішення challenge"""
    solver = InstagramChallengeSolver()
    
    print("🔧 Instagram Challenge Solver")
    print("=" * 40)
    
    # Спочатку спробуємо відновити сесію
    if solver.try_session_recovery():
        print("🎉 Проблема вирішена через відновлення сесії!")
        return
    
    # Перевіряємо статус challenge
    if solver.test_challenge_status():
        print("🎉 Challenge вже вирішено!")
        return
    
    # Показуємо інструкції
    solver.manual_login_guide()
    
    print("\n" + "=" * 60)
    choice = input("Хочете інструкцію створення нового аккаунту? (y/n): ")
    if choice.lower() in ['y', 'yes', 'так', 'т']:
        solver.create_new_account_guide()

if __name__ == "__main__":
    main()
