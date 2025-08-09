# 🇺🇦 Instagram Ukrainian News Bot

Автоматичний бот для публікації українських новин в Instagram з горизонтальними зображеннями та патріотичним дизайном.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Instagram](https://img.shields.io/badge/Instagram-API-purple.svg)](https://instagram.com)
[![Ukrainian](https://img.shields.io/badge/Language-Ukrainian-yellow.svg)](https://uk.wikipedia.org)

## ✨ Можливості

- 📰 **Автоматичний збір новин** з 9 українських медіа
- ⚔️ **Пріоритет військових новин** про війну в Україні
- 🖼️ **Горизонтальні зображення** (1350x1080) з українською символікою
- 🇺🇦 **Патріотичний дизайн** з кольорами українського прапора
- 🤖 **ШІ-генерація контенту** (локальна + OpenAI опційно)
- 🧹 **Автоматична фільтрація** реклами та технічної інформації
- ⏰ **Розклад публікацій** кожні 2-3 години
- 📢 **CTA з посиланням** на Telegram канал

## 📰 Джерела новин

- **Українська Правда** (pravda.com.ua)
- **ТСН** (tsn.ua)
- **НВ** (nv.ua)
- **Радіо Свобода** (radiosvoboda.org)
- **BBC Україна** (bbc.com/ukrainian)
- **Суспільне** (suspilne.media)
- **Громадське** (hromadske.ua)
- **24 канал** (24tv.ua)
- **УНІАН** (unian.ua)

## 🚀 Швидкий старт

### 1. Клонування репозиторію
```bash
git clone https://github.com/yourusername/instagram-ukrainian-news-bot.git
cd instagram-ukrainian-news-bot
```

### 2. Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 3. Налаштування змінних середовища
Створіть файл `.env` на основі `env_example.txt`:
```env
INSTAGRAM_USERNAME=ваш_інстаграм_логін
INSTAGRAM_PASSWORD=ваш_інстаграм_пароль
TELEGRAM_CHANNEL_LINK=https://t.me/ваш_канал
OPENAI_API_KEY=ваш_openai_ключ_опційно
```

### 4. Запуск

#### Тестування:
```bash
python simple_bot.py --test
```

#### Одна публікація:
```bash
python simple_bot.py --post
```

#### Постійна робота:
```bash
python run_bot.py
```

## 🎨 Приклади зображень

### Військові новини (синій фон)
![War News](https://via.placeholder.com/1350x1080/0057B7/ffffff?text=🇺🇦+НОВИНИ+УКРАЇНИ+🇺🇦)

### Загальні новини (жовтий фон)
![General News](https://via.placeholder.com/1350x1080/FFD700/000000?text=🇺🇦+УКРАЇНА+НОВИНИ)

## 🛡️ Фільтрація контенту

Бот автоматично видаляє:
- ❌ Символи `*` та `**`
- ❌ Слово "Реклама"
- ❌ Джерела фото (`© unsplash.com`, `Getty Images`)
- ❌ Технічну інформацію (`Курс валют / ©`)
- ❌ Копірайт та водяні знаки

## 📊 Статистика

- ✅ **4 пости успішно опубліковано**
- 🎯 **Фокус на українському контенті**
- 🖼️ **Горизонтальний формат зображень**
- 🇺🇦 **Патріотичний дизайн**

## ⚙️ Налаштування

### Зміна джерел новин
Відредагуйте `config.py`:
```python
NEWS_SOURCES = [
    'https://your-news-source.rss',
    # додайте свої джерела
]
```

### Налаштування зображень
```python
IMAGE_REQUIREMENTS = {
    'min_width': 1350,
    'min_height': 1080,
    'aspect_ratio_range': (1.25, 1.91),
    'max_file_size_mb': 30
}
```

## 📁 Структура проекту

```
├── simple_bot.py          # Основний бот
├── run_bot.py             # Автоматичний планувальник
├── config.py              # Конфігурація
├── news_collector.py      # Збір новин
├── content_generator.py   # Генерація контенту
├── instagram_publisher.py # Публікація в Instagram
├── translator.py          # Переклад та фільтрація
├── image_handler.py       # Робота з зображеннями (legacy)
├── requirements.txt       # Python залежності
├── .gitignore            # Git ignore правила
├── env_example.txt       # Приклад змінних середовища
└── README.md             # Документація
```

## 🔒 Безпека

- 🔐 Конфіденційні дані в `.env` файлі
- 🚫 `.env` та логи виключені з git
- ⏱️ Автоматичні затримки між діями
- 💾 Збереження сесій Instagram

## 🤝 Внесок у проект

1. Fork репозиторію
2. Створіть feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit зміни (`git commit -m 'Add AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Відкрийте Pull Request

## 📄 Ліцензія

Цей проект ліцензовано під MIT License - дивіться [LICENSE](LICENSE) файл для деталей.

## ⚠️ Відмова від відповідальності

- Використовуйте відповідально та дотримуйтесь правил Instagram
- Поважайте авторські права на контент
- Бот призначений для новинних цілей

## 🙏 Подяки

- Українським медіа за надання новин
- Спільноті за підтримку
- Всім захисникам України 🇺🇦

---

**Слава Україні!** 🇺🇦

*Зроблено з ❤️ для української спільноти*