# 📚 Homework Status Bot

Telegram-бот для автоматического отслеживания статуса проверки домашних работ на Яндекс Практикуме. Бот регулярно проверяет статус через API Практикума и отправляет уведомления в Telegram при изменении статуса работы.

---

## 📌 Функциональность

- 📡 Автоматическая проверка статуса домашней работы каждые **10 минут**
- 📲 Мгновенные уведомления в Telegram:
  - ✅ Взята в проверку
  - 🎉 Проверена и принята
  - ✏️ Возвращена на доработку
- 📝 Логирование всех действий бота
- ⚠️ Уведомления об ошибках и исключениях в Telegram

---

## 📌 Технологии

- 🐍 Python **3.9+**
- `python-telegram-bot`
- `requests`
- `dotenv`
- `logging`

---

## 📌 Установка

1. 📥 Клонируйте репозиторий:

   ```bash
   git clone git@github.com:firuz-backend/homework_bot.git
   cd homework_bot
🐍 Создайте и активируйте виртуальное окружение:

python -m venv venv
source venv/bin/activate
📦 Установите зависимости:

pip install -r requirements.txt


📌 Настройка
Создайте файл .env в корневой директории проекта.

Добавьте туда следующие переменные:

    PRACTICUM_TOKEN=<ваш_токен_практикума>
    TELEGRAM_TOKEN=<токен_вашего_бота>
    TELEGRAM_CHAT_ID=<ваш_chat_id>

Где взять токены:

    PRACTICUM_TOKEN — в профиле на Яндекс Практикуме.

    TELEGRAM_TOKEN — через @BotFather в Telegram.

    TELEGRAM_CHAT_ID — через @userinfobot в Telegram.

📌 Запуск

python homework.py


📌 Структура проекта

    homework_bot/
    ├── homework.py         # Основной файл бота
    ├── exceptions.py       # Пользовательские исключения
    ├── requirements.txt    # Список зависимостей
    ├── README.md           # Описание проекта
    └── .env                # Переменные окружения (добавляется самостоятельно)


📌 Автор

    👨‍💻 Firuz Dadabaev — Python Backend Developer
    GitHub: firuz-backend