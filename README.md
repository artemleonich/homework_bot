# 🤖 Homework Bot

**Telegram bot for tracking Yandex.Practicum homework review status**

[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://core.telegram.org/bots)

<div align="center">

🇬🇧 **English** | [🇷🇺 Русский](#-homework-bot-1)

</div>

---

## 📋 Overview

A Telegram bot that periodically polls the Yandex.Practicum API to check the review status of homework assignments. When the status changes (approved, rejected, or under review), the bot instantly sends a notification to your Telegram chat.

Built as a project during the Yandex.Practicum Backend Python course.

---

## ✨ Features

- **Automatic polling** of the Yandex.Practicum homework API every 10 minutes
- **Instant Telegram notifications** when homework review status changes
- **Three status types** tracked: approved, under review, and rejected
- **Environment variable validation** at startup to prevent misconfiguration
- **Comprehensive error handling** with custom exceptions and structured logging
- **Heroku-ready** deployment with Procfile included

---

## 📂 Project Structure

```
homework_bot/
├── homework.py          # Main bot logic
├── exceptions.py        # Custom exception classes
├── tests/               # Automated tests
├── requirements.txt     # Python dependencies
├── Procfile             # Heroku deployment config
├── setup.cfg            # Linter configuration
├── pytest.ini           # Pytest settings
└── .pre-commit-config.yaml
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Yandex.Practicum API Token
- Your Telegram Chat ID

### Installation

```bash
git clone https://github.com/artemleonich/homework_bot.git
cd homework_bot
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
PRACTICUM_TOKEN=your_practicum_token
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### Running

```bash
python homework.py
```

---

## ⚙️ How It Works

1. The bot validates that all required environment variables are set
2. Every 10 minutes, it sends a request to the Practicum API
3. The API response is validated for correctness
4. If the homework status has changed, a message is sent to Telegram
5. All errors are logged and forwarded to the Telegram chat

---

## 🛠️ Tech Stack

- **python-telegram-bot** — Telegram Bot API wrapper
- **requests** — HTTP client for API calls
- **python-dotenv** — environment variable management
- **flake8** — code style linting
- **pytest** — testing framework

---

---

# 🤖 Homework Bot

**Telegram-бот для отслеживания статуса проверки домашних работ на Яндекс.Практикуме**

[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://core.telegram.org/bots)

<div align="center">

[🇬🇧 English](#-homework-bot) | 🇷🇺 **Русский**

</div>

---

## 📋 Обзор

Telegram-бот, который периодически опрашивает API Яндекс.Практикума для проверки статуса ревью домашних заданий. Когда статус меняется (принято, отклонено или на проверке), бот мгновенно отправляет уведомление в ваш Telegram-чат.

Проект выполнен в рамках курса «Бэкенд-разработка на Python» в Яндекс.Практикуме.

---

## ✨ Возможности

- **Автоматический опрос** API Яндекс.Практикума каждые 10 минут
- **Мгновенные уведомления в Telegram** при изменении статуса работы
- **Три типа статусов**: принято, на проверке, отклонено
- **Проверка переменных окружения** при запуске для предотвращения ошибок конфигурации
- **Комплексная обработка ошибок** с кастомными исключениями и структурированным логированием
- **Готовность к деплою на Heroku** — Procfile в комплекте

---

## 📂 Структура проекта

```
homework_bot/
├── homework.py          # Основная логика бота
├── exceptions.py        # Кастомные классы исключений
├── tests/               # Автотесты
├── requirements.txt     # Зависимости
├── Procfile             # Конфигурация деплоя на Heroku
├── setup.cfg            # Настройки линтера
├── pytest.ini           # Настройки pytest
└── .pre-commit-config.yaml
```

---

## 🚀 Быстрый старт

### Требования

- Python 3.7+
- Токен Telegram-бота (от [@BotFather](https://t.me/BotFather))
- API-токен Яндекс.Практикума
- Ваш Telegram Chat ID

### Установка

```bash
git clone https://github.com/artemleonich/homework_bot.git
cd homework_bot
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### Настройка

Создайте файл `.env` в корне проекта:

```env
PRACTICUM_TOKEN=ваш_токен_практикума
TELEGRAM_TOKEN=токен_вашего_бота
TELEGRAM_CHAT_ID=ваш_chat_id
```

### Запуск

```bash
python homework.py
```

---

## ⚙️ Принцип работы

1. При запуске бот проверяет наличие всех необходимых переменных окружения
2. Каждые 10 минут отправляет запрос к API Практикума
3. Ответ API проверяется на корректность
4. Если статус домашней работы изменился — в Telegram отправляется сообщение
5. Все ошибки логируются и пересылаются в Telegram-чат

---

## 🛠️ Технологии

- **python-telegram-bot** — обёртка над Telegram Bot API
- **requests** — HTTP-клиент для работы с API
- **python-dotenv** — управление переменными окружения
- **flake8** — линтинг кода
- **pytest** — фреймворк для тестирования
