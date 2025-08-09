import requests
from PIL import Image
import io
import os
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from config import IMAGE_REQUIREMENTS

class ImageHandler:
    def __init__(self):
        self.requirements = IMAGE_REQUIREMENTS
        self.temp_dir = "temp_images"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
    
    def is_vertical_image(self, image_url):
        """Перевіряє чи є зображення вертикальним та відповідає вимогам"""
        try:
            response = requests.get(image_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Відкриваємо зображення
            img = Image.open(io.BytesIO(response.content))
            width, height = img.size
            
            # Перевіряємо мінімальні розміри
            if width < self.requirements['min_width'] or height < self.requirements['min_height']:
                return False, "Розмір занадто малий"
            
            # Перевіряємо aspect ratio (для вертикальних зображень висота > ширини)
            aspect_ratio = height / width
            min_ratio, max_ratio = self.requirements['aspect_ratio_range']
            
            if aspect_ratio < min_ratio or aspect_ratio > max_ratio:
                return False, f"Неправильне співвідношення сторін: {aspect_ratio:.2f}"
            
            # Перевіряємо розмір файлу
            if len(response.content) > self.requirements['max_file_size_mb'] * 1024 * 1024:
                return False, "Файл занадто великий"
            
            return True, f"Відмінно! {width}x{height}, ratio: {aspect_ratio:.2f}"
            
        except Exception as e:
            return False, f"Помилка: {e}"
    
    def search_unsplash_images(self, query, count=10):
        """Шукає вертикальні зображення на Unsplash"""
        try:
            # Налаштування Chrome для Selenium
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Шукаємо зображення з вертикальною орієнтацією
            search_url = f"https://unsplash.com/s/photos/{query}?orientation=portrait"
            driver.get(search_url)
            time.sleep(3)
            
            # Парсимо сторінку
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            image_elements = soup.find_all('img')
            
            valid_images = []
            for img in image_elements[:count * 2]:  # Беремо більше для фільтрації
                img_url = img.get('src')
                if img_url and 'images.unsplash.com' in img_url:
                    # Модифікуємо URL для отримання високоякісного зображення
                    high_quality_url = img_url.replace('?', '?w=1080&h=1350&')
                    
                    is_valid, message = self.is_vertical_image(high_quality_url)
                    if is_valid:
                        valid_images.append({
                            'url': high_quality_url,
                            'source': 'Unsplash',
                            'quality_check': message
                        })
                    
                    if len(valid_images) >= count:
                        break
            
            driver.quit()
            return valid_images
            
        except Exception as e:
            print(f"Помилка при пошуку на Unsplash: {e}")
            return []
    
    def search_pexels_images(self, query, count=10):
        """Шукає вертикальні зображення на Pexels"""
        try:
            # Пошук через Pexels API можна реалізувати з API ключем
            # Для демонстрації використовуємо веб-скрапінг
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            search_url = f"https://www.pexels.com/search/{query}/?orientation=portrait"
            driver.get(search_url)
            time.sleep(3)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            image_elements = soup.find_all('img')
            
            valid_images = []
            for img in image_elements[:count * 2]:
                img_url = img.get('src')
                if img_url and 'images.pexels.com' in img_url:
                    # Модифікуємо для високої якості
                    high_quality_url = img_url.replace('?', '?w=1080&h=1350&')
                    
                    is_valid, message = self.is_vertical_image(high_quality_url)
                    if is_valid:
                        valid_images.append({
                            'url': high_quality_url,
                            'source': 'Pexels',
                            'quality_check': message
                        })
                    
                    if len(valid_images) >= count:
                        break
            
            driver.quit()
            return valid_images
            
        except Exception as e:
            print(f"Помилка при пошуку на Pexels: {e}")
            return []
    
    def find_news_related_image(self, news_title, news_content):
        """Знаходить вертикальне зображення, пов'язане з новиною"""
        # Витягуємо ключові слова з заголовка новини
        keywords = self.extract_keywords(news_title, news_content)
        
        all_images = []
        
        # Шукаємо на різних платформах
        for keyword in keywords[:3]:  # Беремо топ-3 ключових слова
            print(f"Пошук зображень для: {keyword}")
            
            unsplash_images = self.search_unsplash_images(keyword, 3)
            pexels_images = self.search_pexels_images(keyword, 3)
            
            all_images.extend(unsplash_images)
            all_images.extend(pexels_images)
            
            if len(all_images) >= 5:  # Достатньо варіантів
                break
        
        # Повертаємо випадкове якісне зображення
        if all_images:
            return random.choice(all_images)
        
        return None
    
    def extract_keywords(self, title, content):
        """Витягує ключові слова з новини для пошуку зображень"""
        # Простий алгоритм витягування ключових слів
        import re
        
        text = f"{title} {content}"
        
        # Видаляємо стоп-слова та отримуємо важливі слова
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'що', 'та', 'в', 'на', 'з', 'за', 'для', 'про', 'як', 'це'}
        
        words = re.findall(r'\b[a-zA-Zа-яА-Я]{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        # Повертаємо найчастіші слова
        word_freq = {}
        for word in keywords:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_keywords[:5]]
    
    def download_image(self, image_url, filename):
        """Завантажує зображення локально"""
        try:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
            
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
        except Exception as e:
            print(f"Помилка завантаження зображення: {e}")
            return None
