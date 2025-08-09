from openai import OpenAI
import random
from config import OPENAI_API_KEY, CTA_PHRASES, TELEGRAM_CHANNEL_LINK

class ContentGenerator:
    def __init__(self):
        # Ініціалізуємо OpenAI клієнт тільки якщо є API ключ
        if OPENAI_API_KEY and OPENAI_API_KEY.strip():
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        else:
            self.client = None
        self.cta_phrases = CTA_PHRASES
        self.telegram_link = TELEGRAM_CHANNEL_LINK
    
    def generate_post_description(self, news_title, news_content, max_length=2000):
        """Генерує привабливий опис поста з новини"""
        # Якщо немає OpenAI клієнта, одразу використовуємо fallback
        if not self.client:
            return self.generate_fallback_post(news_title, news_content)
        
        try:
            # Створюємо промпт для OpenAI
            prompt = f"""
            Створи привабливий пост для Instagram на основі цієї новини. Пост має бути:
            - Цікавим та зацікавлюючим
            - Емоційним та захоплюючим
            - Не більше {max_length // 2} символів (основний текст)
            - Українською мовою
            - З використанням емодзі
            - Без посилань (їх додам окремо)
            
            Заголовок новини: {news_title}
            
            Контент новини: {news_content[:500]}...
            
            Стиль: молодіжний, сучасний, з емодзі. Зроби так, щоб люди захотіли дізнатися більше.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ти експерт з створення вірусного контенту для соціальних мереж. Твоя задача - робити пosti, які залучають увагу та отримують високий engagement."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            # Очищаємо згенерований текст
            generated_text = self.clean_content(generated_text)
            
            # Додаємо call-to-action та посилання на Telegram
            cta = random.choice(self.cta_phrases)
            final_post = f"{generated_text}\n\n{cta}\n👉 {self.telegram_link}"
            
            # Перевіряємо довжину
            if len(final_post) > max_length:
                # Обрізаємо основний текст, щоб влізти в ліміт
                max_main_text = max_length - len(f"\n\n{cta}\n👉 {self.telegram_link}") - 50
                generated_text = generated_text[:max_main_text] + "..."
                final_post = f"{generated_text}\n\n{cta}\n👉 {self.telegram_link}"
            
            return final_post
            
        except Exception as e:
            print(f"Помилка генерації контенту: {e}")
            return self.generate_fallback_post(news_title, news_content)
    
    def generate_fallback_post(self, news_title, news_content):
        """Покращений резервний варіант генерації поста без OpenAI"""
        try:
            # Очищаємо заголовок від небажаних елементів
            news_title = self.clean_content(news_title)
            # Розширений список емодзі для різних типів новин
            emoji_sets = {
                'politics': ["🏛️", "⚖️", "🗳️", "📊", "🔥"],
                'economy': ["💰", "📈", "📉", "💼", "🏦"],
                'technology': ["🚀", "💻", "📱", "⚡", "🔮"],
                'sports': ["⚽", "🏆", "🥇", "⭐", "💪"],
                'entertainment': ["🎬", "🎭", "🌟", "✨", "🎯"],
                'health': ["🏥", "💊", "🔬", "❤️", "🩺"],
                'world': ["🌍", "🌎", "🗺️", "📰", "🔥"],
                'default': ["📰", "🔥", "⚡", "💥", "🌟", "💡", "📢", "🎯"]
            }
            
            # Визначаємо категорію новини за ключовими словами
            category = self.detect_news_category(news_title, news_content)
            emoji = random.choice(emoji_sets.get(category, emoji_sets['default']))
            
            # Розширене форматування контенту
            formatted_content = self.format_news_content_extended(news_content)
            
            # Додаємо цікаві фрази-зачіпки
            hooks = [
                "Це варто знати! 👇",
                "Шокуюча правда! 😱",
                "Ви не повірите! 🤯",
                "Важливо для всіх! ⚠️",
                "Тренд дня! 📈",
                "Гаряча новина! 🔥",
                "Всі говорять про це! 💬"
            ]
            
            hook = random.choice(hooks)
            
            # Створюємо структурований пост
            post_parts = [
                f"{emoji} {hook}",
                "",
                f"**{news_title}**",
                "",
                formatted_content,
                "",
                random.choice(self.cta_phrases),
                f"👉 {self.telegram_link}"
            ]
            
            post = "\n".join(post_parts)
            
            # Перевіряємо довжину та обрізаємо якщо потрібно
            if len(post) > 2000:
                # Скорочуємо контент
                max_content_length = 1500 - len(post) + len(formatted_content)
                formatted_content = formatted_content[:max_content_length] + "..."
                
                post_parts[4] = formatted_content
                post = "\n".join(post_parts)
            
            return post
            
        except Exception as e:
            print(f"Помилка fallback генерації: {e}")
            return f"📰 Важливі новини!\n\n{news_title}\n\n{random.choice(self.cta_phrases)}\n👉 {self.telegram_link}"
    
    def detect_news_category(self, title, content):
        """Визначає категорію новини за ключовими словами"""
        text = f"{title} {content}".lower()
        
        categories = {
            'politics': ['політика', 'уряд', 'президент', 'вибори', 'парламент', 'міністр'],
            'economy': ['економіка', 'гроші', 'бізнес', 'ринок', 'банк', 'інвестиції', 'цена'],
            'technology': ['технологія', 'комп\'ютер', 'інтернет', 'додаток', 'штучний інтелект'],
            'sports': ['спорт', 'футбол', 'змагання', 'чемпіонат', 'олімпіада'],
            'entertainment': ['фільм', 'музика', 'зірка', 'шоу', 'концерт'],
            'health': ['здоров\'я', 'медицина', 'лікування', 'хвороба', 'вакцина'],
            'world': ['світ', 'країна', 'міжнародний', 'війна', 'мир']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'default'
    
    def format_news_content(self, content):
        """Покращене форматування контенту новини"""
        if not content:
            return "Деталі в повному тексті новини."
        
        # Очищаємо контент від непотрібних елементів
        content = self.clean_content(content)
        
        # Розбиваємо на речення
        sentences = content.split('.')
        
        # Беремо найцікавіші речення (не більше 3-4)
        good_sentences = []
        for sentence in sentences[:6]:
            sentence = sentence.strip()
            # Додаткова фільтрація речень
            if (len(sentence) > 20 and len(sentence) < 200 and 
                not self.is_unwanted_sentence(sentence)):
                good_sentences.append(sentence)
            if len(good_sentences) >= 3:
                break
        
        if not good_sentences:
            cleaned_content = self.clean_content(content)
            return cleaned_content[:300] + "..." if len(cleaned_content) > 300 else cleaned_content
        
        # З'єднуємо з покращеним форматуванням
        formatted = '. '.join(good_sentences) + '.'
        
        # Додаємо емодзі для акцентів
        formatted = formatted.replace('!', '! 😮')
        formatted = formatted.replace('?', '? 🤔')
        
        return formatted
    
    def format_news_content_extended(self, content):
        """Розширене форматування контенту з більшою кількістю тексту"""
        if not content:
            return "Детальна інформація у повному тексті новини. Слідкуйте за оновленнями!"
        
        # Очищаємо контент
        content = self.clean_content(content)
        
        # Розбиваємо на речення
        sentences = content.split('.')
        
        # Беремо більше речень для розширеного контенту (5-6 замість 3-4)
        good_sentences = []
        for sentence in sentences[:10]:
            sentence = sentence.strip()
            if (len(sentence) > 15 and len(sentence) < 250 and 
                not self.is_unwanted_sentence(sentence)):
                good_sentences.append(sentence)
            if len(good_sentences) >= 6:
                break
        
        if not good_sentences:
            return content[:400] + "..." if len(content) > 400 else content
        
        # Форматуємо з розділювачами для кращого читання
        formatted_parts = []
        for i, sentence in enumerate(good_sentences):
            if i == 0:
                formatted_parts.append(f"🔹 {sentence}.")
            elif i < 3:
                formatted_parts.append(f"▫️ {sentence}.")
            else:
                formatted_parts.append(f"• {sentence}.")
        
        return '\n\n'.join(formatted_parts)
    
    def clean_content(self, text):
        """Очищає текст від непотрібних елементів"""
        if not text:
            return text
        
        import re
        
        # Видаляємо зірочки
        text = re.sub(r'\*+', '', text)
        
        # Видаляємо слово "Реклама" і варіації
        text = re.sub(r'\b[Рр]еклама\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b[Аа]dvertisement\b', '', text, flags=re.IGNORECASE)
        
        # Видаляємо посилання на джерела зображень
        text = re.sub(r'©\s*[^\s]+\.[a-z]{2,4}', '', text, flags=re.IGNORECASE)
        text = re.sub(r'[Кк]урс валют?\s*/\s*©.*', '', text)
        text = re.sub(r'unsplash\.com', '', text, flags=re.IGNORECASE)
        text = re.sub(r'getty\s*images?', '', text, flags=re.IGNORECASE)
        text = re.sub(r'shutterstock', '', text, flags=re.IGNORECASE)
        
        # Видаляємо технічну інформацію
        text = re.sub(r'©.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'Джерело:.*$', '', text, flags=re.MULTILINE)
        text = re.sub(r'Фото:.*$', '', text, flags=re.MULTILINE)
        
        # Видаляємо зайві пробіли
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def is_unwanted_sentence(self, sentence):
        """Перевіряє чи речення містить небажаний контент"""
        unwanted_patterns = [
            r'\*+',  # Зірочки
            r'[Рр]еклама',  # Реклама
            r'©.*',  # Копірайт
            r'unsplash',  # Unsplash
            r'getty',  # Getty Images
            r'shutterstock',  # Shutterstock
            r'[Дд]жерело:',  # Джерело
            r'[Фф]ото:',  # Фото
            r'курс валют.*©',  # Курс валют з копірайтом
        ]
        
        import re
        for pattern in unwanted_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                return True
        
        return False
    
    def generate_hashtags(self, news_title, news_content):
        """Генерує релевантні хештеги для поста"""
        try:
            # Якщо є OpenAI API ключ, використовуємо його
            if OPENAI_API_KEY and OPENAI_API_KEY.strip():
                return self.generate_ai_hashtags(news_title, news_content)
            else:
                # Інакше використовуємо локальний генератор
                return self.generate_local_hashtags(news_title, news_content)
        except Exception as e:
            print(f"Помилка генерації хештегів: {e}")
            return "#новини #україна #важливо #актуально #тренди"
    
    def generate_ai_hashtags(self, news_title, news_content):
        """Генерує хештеги через OpenAI"""
        # Якщо немає клієнта, використовуємо локальний генератор
        if not self.client:
            return self.generate_local_hashtags(news_title, news_content)
        
        prompt = f"""
        Створи 5-10 релевантних хештегів українською мовою для цієї новини:
        
        Заголовок: {news_title}
        Контент: {news_content[:300]}...
        
        Хештеги мають бути:
        - Популярними в Україні
        - Релевантними до теми
        - Без пробілів
        - Починатися з #
        
        Поверни тільки хештеги через пробіл.
        """
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти експерт з SMM та хештегів для української аудиторії."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_local_hashtags(self, news_title, news_content):
        """Генерує хештеги локально без ШІ"""
        text = f"{news_title} {news_content}".lower()
        
        # Категорії хештегів
        hashtag_categories = {
            'base': ['#новини', '#україна', '#актуально', '#важливо'],
            'politics': ['#політика', '#уряд', '#державасправа', '#вибори'],
            'economy': ['#економіка', '#бізнес', '#гроші', '#ринок', '#інвестиції'],
            'technology': ['#технології', '#інновації', '#IT', '#майбутнє'],
            'sports': ['#спорт', '#чемпіонат', '#перемога', '#змагання'],
            'entertainment': ['#розваги', '#шоубіз', '#знаменитості', '#культура'],
            'health': ['#здоровя', '#медицина', '#лікування'],
            'world': ['#світовіновини', '#міжнародне', '#геополітика'],
            'trending': ['#тренди', '#топновини', '#обговорення', '#популярне']
        }
        
        selected_hashtags = hashtag_categories['base'].copy()
        
        # Визначаємо категорію та додаємо відповідні хештеги
        category = self.detect_news_category(news_title, news_content)
        if category in hashtag_categories:
            selected_hashtags.extend(hashtag_categories[category][:3])
        
        # Додаємо трендові хештеги
        selected_hashtags.extend(random.sample(hashtag_categories['trending'], 2))
        
        # Випадковий порядок та унікальність
        hashtags = list(set(selected_hashtags))
        random.shuffle(hashtags)
        
        return ' '.join(hashtags[:8])  # Максимум 8 хештегів
    
    def create_full_post(self, news_title, news_content):
        """Створює повний пост з описом та хештегами"""
        description = self.generate_post_description(news_title, news_content)
        hashtags = self.generate_hashtags(news_title, news_content)
        
        # Об'єднуємо в фінальний пост
        full_post = f"{description}\n\n{hashtags}"
        
        # Перевіряємо ліміт Instagram (2200 символів)
        if len(full_post) > 2200:
            # Обрізаємо хештеги якщо потрібно
            max_desc_length = 2200 - len(hashtags) - 10
            if len(description) > max_desc_length:
                description = description[:max_desc_length] + "..."
            full_post = f"{description}\n\n{hashtags}"
        
        return full_post
    
    def add_story_elements(self, post_text):
        """Додає елементи для Stories (якщо потрібно)"""
        # Можна додати стікери, опитування тощо для Stories
        story_elements = {
            'text': post_text[:500],  # Stories мають обмеження
            'stickers': ['poll', 'question', 'countdown'],
            'background_color': random.choice(['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        }
        return story_elements
