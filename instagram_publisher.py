from instagrapi import Client
import os
import time
import random
from datetime import datetime
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

class InstagramPublisher:
    def __init__(self):
        self.client = Client()
        self.username = INSTAGRAM_USERNAME
        self.password = INSTAGRAM_PASSWORD
        self.is_logged_in = False
        
    def login(self):
        """Авторизація в Instagram"""
        try:
            print("Вхід в Instagram...")
            
            # Спроба входу
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
                
            # Спроба завантажити збережену сесію
            elif os.path.exists("instagram_session.json"):
                try:
                    print("🔄 Спроба входу через збережену сесію...")
                    self.client.load_settings("instagram_session.json")
                    self.client.login(self.username, self.password)
                    self.is_logged_in = True
                    print("✅ Вхід через збережену сесію!")
                    return True
                except:
                    print("❌ Збережена сесія не працює")
            
            return False
    
    def publish_photo_post(self, image_path, caption, location=None):
        """Публікує фото пост в Instagram"""
        if not self.is_logged_in:
            if not self.login():
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
            
        except Exception as e:
            print(f"❌ Помилка публікації: {e}")
            return False, f"Помилка: {e}"
    
    def publish_story(self, image_path, text_overlay=None):
        """Публікує Stories в Instagram"""
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
        """Отримує інформацію про аккаунт"""
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
        """Отримує статистику поста (для бізнес аккаунтів)"""
        try:
            insights = self.client.insights_media_v1(media_id)
            return insights
        except Exception as e:
            print(f"Помилка отримання статистики: {e}")
            return None
    
    def schedule_optimal_time(self):
        """Визначає оптимальний час для публікації"""
        current_hour = datetime.now().hour
        
        # Оптимальні години для публікації в Instagram (за українським часом)
        optimal_hours = [8, 9, 12, 13, 17, 18, 19, 20, 21]
        
        if current_hour in optimal_hours:
            return True, "Зараз гарний час для публікації"
        else:
            next_optimal = min(hour for hour in optimal_hours if hour > current_hour)
            return False, f"Краще опублікувати о {next_optimal}:00"
    
    def add_hashtags_to_comment(self, media_id, hashtags):
        """Додає хештеги як коментар (щоб не захаращувати основний текст)"""
        try:
            comment = self.client.media_comment(media_id, hashtags)
            print("✅ Хештеги додано як коментар")
            return True, comment.id
        except Exception as e:
            print(f"❌ Помилка додавання коментаря: {e}")
            return False, str(e)
    
    def safe_publish(self, image_path, caption, add_hashtags_as_comment=True):
        """Безпечна публікація з додатковими перевірками"""
        try:
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
        """Вихід з аккаунту"""
        try:
            self.client.logout()
            self.is_logged_in = False
            print("👋 Вихід з Instagram")
        except:
            pass
