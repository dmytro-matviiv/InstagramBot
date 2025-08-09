import requests
import feedparser
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
import random
import time
from datetime import datetime, timedelta
from config import NEWS_SOURCES

class NewsCollector:
    def __init__(self):
        self.sources = NEWS_SOURCES
        self.collected_articles = []
    
    def fetch_rss_news(self, rss_url):
        """Збирає новини з RSS каналів"""
        try:
            feed = feedparser.parse(rss_url)
            articles = []
            
            for entry in feed.entries[:10]:  # Беремо останні 10 новин
                article_data = {
                    'title': entry.title,
                    'link': entry.link,
                    'published': entry.get('published', ''),
                    'summary': entry.get('summary', ''),
                    'source': rss_url
                }
                articles.append(article_data)
            
            return articles
        except Exception as e:
            print(f"Помилка при зборі з RSS {rss_url}: {e}")
            return []
    
    def get_article_content(self, url):
        """Отримує повний контент статті"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            return {
                'title': article.title,
                'text': article.text,
                'authors': article.authors,
                'publish_date': article.publish_date,
                'top_image': article.top_image,
                'images': list(article.images)
            }
        except Exception as e:
            print(f"Помилка при парсингу статті {url}: {e}")
            # Повертаємо базову інформацію якщо повний парсинг не вдався
            return {
                'title': 'Новина з RSS',
                'text': 'Контент новини недоступний для повного парсингу.',
                'authors': [],
                'publish_date': None,
                'top_image': None,
                'images': []
            }
    
    def collect_fresh_news(self):
        """Збирає свіжі новини з усіх джерел"""
        all_news = []
        
        for source in self.sources:
            print(f"Збираю новини з {source}")
            rss_articles = self.fetch_rss_news(source)
            
            for article in rss_articles:
                # Отримуємо повний контент
                full_content = self.get_article_content(article['link'])
                if full_content:
                    article.update(full_content)
                
                all_news.append(article)
            
            time.sleep(1)  # Пауза між запитами
        
        # Фільтруємо та сортуємо за актуальністю
        fresh_news = self.filter_recent_news(all_news)
        return fresh_news
    
    def filter_recent_news(self, articles, hours_ago=6):
        """Фільтрує новини за останні N годин"""
        cutoff_time = datetime.now() - timedelta(hours=hours_ago)
        recent_articles = []
        
        for article in articles:
            try:
                if article.get('publish_date'):
                    if isinstance(article['publish_date'], str):
                        # Якщо дата в строковому форматі, спробуємо парсити
                        continue
                    elif article['publish_date'] > cutoff_time:
                        recent_articles.append(article)
                else:
                    # Якщо немає дати, вважаємо новину свіжою
                    recent_articles.append(article)
            except:
                recent_articles.append(article)
        
        # Сортуємо за релевантністю (можна додати більше критеріїв)
        return sorted(recent_articles, key=lambda x: len(x.get('text', '')), reverse=True)
    
    def get_random_news(self):
        """Повертає випадкову актуальну новину"""
        fresh_news = self.collect_fresh_news()
        if fresh_news:
            return random.choice(fresh_news)
        return None
