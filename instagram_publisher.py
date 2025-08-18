"""
Публікатор у Instagram на базі instagrapi.

Ключові можливості:
- login: авторизація з кешем сесії.
- publish_photo_post: публікація фото у стрічку.
- publish_story: публікація історій.
- get_account_info / get_post_insights: допоміжні методи інформації/аналітики.
- schedule_optimal_time: проста евристика «гарного часу» для посту.
- add_hashtags_to_comment: додає хештеги окремим коментарем.
- safe_publish: обгортач публікації з розділенням підпису/хештегів та таймінгом.
- logout: вихід із акаунта.
"""

from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
import os
import time
import random
from datetime import datetime
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

class InstagramPublisher:
    def __init__(self):
        """Створює клієнт instagrapi та готує поля авторизації/стану."""
        self.client = Client()
        self.username = INSTAGRAM_USERNAME
        self.password = INSTAGRAM_PASSWORD
        self.is_logged_in = False
        
        # Спроба попередньо підвантажити сесію (якщо є)
        try:
            if os.path.exists("instagram_session.json"):
                self.client.load_settings("instagram_session.json")
        except Exception:
            pass
        
    def login(self):
        """Виконує вхід у Instagram; за можливості використовує збережену сесію."""
        try:
            print("Вхід в Instagram...")
            
            # 1) Спроба через збережені налаштування/сесію
            if os.path.exists("instagram_session.json"):
                try:
                    self.client.load_settings("instagram_session.json")
                    self.client.login(self.username, self.password)
                    self.is_logged_in = True
                    print("✅ Вхід через збережену сесію!")
                    # Оновимо сесію
                    self.client.dump_settings("instagram_session.json")
                    return True
                except Exception:
                    print("⚠️ Збережена сесія неактуальна, пробую звичайний вхід...")
            
            # 2) Звичайний вхід
            self.client.login(self.username, self.password)
            self.is_logged_in = True
            print("✅ Успішний вхід в Instagram!")
            
            # Збереження сесії для подальшого використання
            self.client.dump_settings("instagram_session.json")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Помилка входу в Instagram: {error_msg}")
            
            # Перевіряємо чи це challenge
            if "ChallengeResolve" in error_msg or "show_selfie_captcha" in error_msg:
                print("\n⚠️ Instagram вимагає додаткову верифікацію (Challenge)")
                print("💡 Рішення:")
                print("1. Увійдіть в аккаунт вручну через браузер або мобільний додаток")
                print("2. Пройдіть верифікацію (email/SMS/селфі)")
                print("3. Почекайте 24-48 години і спробуйте знову")
                print("4. Або використайте інший аккаунт")
                print("5. Переконайтеся що аккаунт не новий і має активність\n")
                
            return False
    
    def ensure_logged_in(self):
        """Перевіряє валідність сесії і виконує повторний вхід за потреби."""
        try:
            if not self.is_logged_in:
                return self.login()
            # Швидка перевірка сесії викликом API
            _ = self.client.account_info()
            return True
        except LoginRequired:
            print("⚠️ Сесія недійсна: потрібен повторний вхід")
            self.is_logged_in = False
            return self.login()
        except Exception:
            # На будь-яку іншу помилку — пробуємо переввійтись
            self.is_logged_in = False
            return self.login()

    def publish_photo_post(self, image_path, caption, location=None):
        """Публікує фото у стрічку з підписом; повертає (success, message)."""
        if not self.ensure_logged_in():
            return False, "Неможливо увійти в Instagram"
        
        try:
            print("📤 Публікую пост в Instagram...")
            
            # Додаємо рандомну затримку для природності
            time.sleep(random.uniform(30, 60))
            
            # Публікуємо фото
            media = self.client.photo_upload(
                image_path, 
                caption,
                location=location
            )
            
            print(f"✅ Пост успішно опубліковано! ID: {media.id}")
            
            # Видаляємо тимчасовий файл
            try:
                os.remove(image_path)
                print("🗑️ Тимчасовий файл видалено")
            except:
                pass
            
            return True, f"Пост опубліковано: {media.id}"
            
        except (LoginRequired, ChallengeRequired) as e:
            # Спроба відновлення сесії та повторного аплоаду один раз
            print(f"⚠️ Сесія втрачена/потрібен челендж: {e}. Перевхід та повтор...")
            self.is_logged_in = False
            if self.ensure_logged_in():
                try:
                    time.sleep(random.uniform(5, 10))
                    media = self.client.photo_upload(image_path, caption, location=location)
                    print(f"✅ Пост успішно опубліковано після перевходу! ID: {media.id}")
                    try:
                        os.remove(image_path)
                        print("🗑️ Тимчасовий файл видалено")
                    except:
                        pass
                    return True, f"Пост опубліковано: {media.id}"
                except Exception as e2:
                    print(f"❌ Повторна помилка публікації: {e2}")
                    return False, f"Помилка: {e2}"
            return False, "login_required"
        except PleaseWaitFewMinutes as e:
            print(f"⏳ Instagram просить зачекати: {e}")
            return False, "please_wait_few_minutes"
        except Exception as e:
            print(f"❌ Помилка публікації: {e}")
            return False, f"Помилка: {e}"
    
    def publish_story(self, image_path, text_overlay=None):
        """Публікує історію з опціональним текстом; повертає (success, message)."""
        if not self.is_logged_in:
            if not self.login():
                return False, "Неможливо увійти в Instagram"
        
        try:
            print("📤 Публікую Stories...")
            
            # Публікуємо Stories
            story = self.client.photo_upload_to_story(
                image_path,
                caption=text_overlay
            )
            
            print(f"✅ Stories опубліковано! ID: {story.id}")
            
            # Видаляємо тимчасовий файл
            try:
                os.remove(image_path)
            except:
                pass
            
            return True, f"Stories опубліковано: {story.id}"
            
        except Exception as e:
            print(f"❌ Помилка публікації Stories: {e}")
            return False, f"Помилка: {e}"
    
    def get_account_info(self):
        """Повертає базову інформацію про акаунт (username/followers/...); або None при помилці."""
        if not self.is_logged_in:
            if not self.login():
                return None
        
        try:
            user_info = self.client.account_info()
            return {
                'username': user_info.username,
                'followers': user_info.follower_count,
                'following': user_info.following_count,
                'posts': user_info.media_count,
                'is_verified': user_info.is_verified,
                'is_business': user_info.is_business
            }
        except Exception as e:
            print(f"Помилка отримання інформації про аккаунт: {e}")
            return None
    
    def get_post_insights(self, media_id):
        """Повертає статистику поста (для бізнес-акаунтів) або None при помилці."""
        try:
            insights = self.client.insights_media_v1(media_id)
            return insights
        except Exception as e:
            print(f"Помилка отримання статистики: {e}")
            return None
    
    def schedule_optimal_time(self):
        """Повертає (is_optimal, message) для поточної години за простою евристикою таймінгу."""
        current_hour = datetime.now().hour
        
        # Оптимальні години для публікації в Instagram (за українським часом)
        optimal_hours = [8, 9, 12, 13, 17, 18, 19, 20, 21]
        
        if current_hour in optimal_hours:
            return True, "Зараз гарний час для публікації"
        else:
            next_optimal = min(hour for hour in optimal_hours if hour > current_hour)
            return False, f"Краще опублікувати о {next_optimal}:00"
    
    def add_hashtags_to_comment(self, media_id, hashtags):
        """Додає хештеги як коментар під постом; повертає (success, comment_id|error)."""
        try:
            comment = self.client.media_comment(media_id, hashtags)
            print("✅ Хештеги додано як коментар")
            return True, comment.id
        except Exception as e:
            print(f"❌ Помилка додавання коментаря: {e}")
            return False, str(e)
    
    def safe_publish(self, image_path, caption, add_hashtags_as_comment=True):
        """Публікує фото безпечно: відокремлює хештеги, чекає «гарного часу», додає хештеги коментарем."""
        try:
            # Переконуємось, що сесія робоча перед будь-якими діями
            if not self.ensure_logged_in():
                return False, "Неможливо увійти в Instagram"
            
            # Перевіряємо час
            is_optimal, time_message = self.schedule_optimal_time()
            print(f"⏰ {time_message}")
            
            # Розділяємо контент та хештеги
            if add_hashtags_as_comment and '\n#' in caption:
                parts = caption.split('\n#')
                main_caption = parts[0]
                hashtags = '#' + '\n#'.join(parts[1:])
            else:
                main_caption = caption
                hashtags = ""
            
            # Публікуємо основний пост
            success, message = self.publish_photo_post(image_path, main_caption)
            
            if success and hashtags and add_hashtags_as_comment:
                # Витягуємо ID медіа з повідомлення
                media_id = message.split(": ")[-1]
                # Додаємо хештеги як коментар через кілька секунд
                time.sleep(random.uniform(10, 30))
                self.add_hashtags_to_comment(media_id, hashtags)
            
            return success, message
            
        except Exception as e:
            return False, f"Помилка безпечної публікації: {e}"
    
    def logout(self):
        """Завершує сесію instagrapi та скидає прапорець авторизації."""
        try:
            self.client.logout()
            self.is_logged_in = False
            print("👋 Вихід з Instagram")
        except:
            pass
