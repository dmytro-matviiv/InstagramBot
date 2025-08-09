import requests
import re
# from googletrans import Translator

class NewsTranslator:
    def __init__(self):
        # self.translator = Translator()
        pass
    
    def detect_language(self, text):
        """Визначає мову тексту (спрощена версія)"""
        # Простий детектор на основі українських символів
        ukrainian_chars = set('абвгґдеєжзиіїйклмнопрстуфхцчшщьюя')
        text_chars = set(text.lower())
        
        if len(text_chars & ukrainian_chars) > len(text) * 0.1:
            return 'uk'
        else:
            return 'en'  # припускаємо англійську
    
    def translate_to_ukrainian(self, text):
        """Спрощений переклад - якщо новина вже українська, залишаємо як є"""
        if not text or len(text.strip()) < 3:
            return text
        
        # Якщо текст містить українські символи, залишаємо як є
        lang = self.detect_language(text)
        if lang == 'uk':
            return text
        
        # Для англійських новин повертаємо як є (оригінальні новини будуть з українських джерел)
        return text
    
    def translate_news_article(self, article):
        """Перекладає статтю новини на українську"""
        translated_article = article.copy()
        
        # Перекладаємо заголовок
        if article.get('title'):
            translated_title = self.translate_to_ukrainian(article['title'])
            translated_article['title'] = translated_title
        
        # Перекладаємо короткий опис
        if article.get('summary'):
            translated_summary = self.translate_to_ukrainian(article['summary'])
            translated_article['summary'] = translated_summary
        
        # Перекладаємо повний текст
        if article.get('text'):
            # Для довгих текстів розбиваємо на частини
            text = article['text']
            if len(text) > 1000:
                # Розбиваємо на речення
                sentences = re.split(r'[.!?]+', text)
                translated_sentences = []
                
                for sentence in sentences:
                    if sentence.strip():
                        translated_sentence = self.translate_to_ukrainian(sentence.strip())
                        translated_sentences.append(translated_sentence)
                
                translated_text = '. '.join(translated_sentences)
            else:
                translated_text = self.translate_to_ukrainian(text)
            
            translated_article['text'] = translated_text
        
        return translated_article
    
    def filter_ukraine_related(self, articles):
        """Фільтрує новини пов'язані з Україною"""
        ukraine_keywords = [
            'україн', 'ukraine', 'київ', 'kyiv', 'київський', 'харків', 'kharkiv',
            'одеса', 'odesa', 'львів', 'lviv', 'дніпро', 'dnipro', 'запоріжжя',
            'війна', 'war', 'конфлікт', 'conflict', 'росія', 'russia', 'путін', 'putin',
            'зеленський', 'zelensky', 'нато', 'nato', 'євросоюз', 'eu', 'european union',
            'санкції', 'sanctions', 'мобілізація', 'mobilization', 'фронт', 'front',
            'окупац', 'occupation', 'звільнен', 'liberation', 'донбас', 'donbas',
            'луганськ', 'luhansk', 'донецьк', 'donetsk', 'крим', 'crimea', 'херсон',
            'миколаїв', 'refugee', 'біженц', 'гуманітар', 'humanitarian', 'обстріл',
            'ракет', 'missile', 'дрон', 'drone', 'авіаудар', 'airstrike'
        ]
        
        filtered_articles = []
        
        for article in articles:
            # Перевіряємо заголовок та текст на наявність ключових слів
            title = (article.get('title', '') or '').lower()
            text = (article.get('text', '') or article.get('summary', '') or '').lower()
            full_text = title + ' ' + text
            
            # Якщо знайшли ключове слово, додаємо статтю
            if any(keyword in full_text for keyword in ukraine_keywords):
                filtered_articles.append(article)
        
        return filtered_articles
    
    def prioritize_war_news(self, articles):
        """Віддає пріоритет новинам про війну"""
        war_keywords = [
            'війна', 'war', 'бойові дії', 'combat', 'фронт', 'front', 'наступ', 'offensive',
            'оборона', 'defense', 'обстріл', 'shelling', 'ракет', 'missile', 'авіаудар',
            'втрати', 'casualties', 'загиблі', 'killed', 'поранені', 'wounded',
            'військов', 'military', 'армія', 'army', 'техніка', 'equipment',
            'танк', 'tank', 'артилерія', 'artillery', 'дрон', 'drone'
        ]
        
        war_articles = []
        other_articles = []
        
        for article in articles:
            title = (article.get('title', '') or '').lower()
            text = (article.get('text', '') or article.get('summary', '') or '').lower()
            full_text = title + ' ' + text
            
            if any(keyword in full_text for keyword in war_keywords):
                war_articles.append(article)
            else:
                other_articles.append(article)
        
        # Повертаємо спочатку військові новини, потім інші
        return war_articles + other_articles
