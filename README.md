# Homework Bot

<img src=".github/assets/stack.svg" height="28" alt="Python · Telegram · Learning" />

Статусы ревью домашних заданий Яндекс Практикума в Telegram.

**Учебный проект**  
[Русский](#about) · [English](#english) · [Профиль](https://github.com/artemleonich)

<a id="about"></a>

## О проекте

Бот опрашивает API [Яндекс Практикума](https://practicum.yandex.ru/) с интервалом 10 минут и отправляет в Telegram статус первой работы из полученного списка: принято, на проверке или есть замечания. Проект выполнен в рамках курса бэкенд-разработки на Python.

- Проверяет наличие токенов и идентификатора чата при запуске.
- Разбирает ответы API и проверяет известные статусы.
- Ведёт журнал работы и отправляет сообщения об ошибках.
- Содержит тесты и `Procfile` с командой запуска фонового процесса.

## Стек

Python · python-telegram-bot 13.7 · requests 2.26.0 · python-dotenv 0.19.0 · pytest 6.2.5. Версии закреплены в [requirements.txt](requirements.txt).

## Запуск

```bash
git clone https://github.com/artemleonich/homework_bot.git
cd homework_bot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

В Windows PowerShell: `.venv\Scripts\Activate.ps1`.

Создайте `.env` в корне проекта:

```dotenv
PRACTICUM_TOKEN=your_practicum_token
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

Токен Telegram-бота можно получить у [@BotFather](https://t.me/BotFather); API-токен Практикума и идентификатор чата нужно указать для своей учётной записи.

```bash
python homework.py
```

Остановить процесс можно сочетанием Ctrl+C. Для работы нужны действующие токены и доступ к обоим API.

## Проверка

Из корня репозитория:

```bash
python -m pytest
```

## Навигация по коду

| Файл | Назначение |
| --- | --- |
| [homework.py](homework.py) | Опрос API, обработка ответа, уведомления |
| [exceptions.py](exceptions.py) | Исключения приложения |
| [tests/](tests/) | Проверки поведения бота |
| [Procfile](Procfile) | Команда `worker: python homework.py` |

Здесь сохранён учебный стек. Интервал опроса составляет 10 минут, поэтому уведомления зависят от следующего запроса к API.

<a id="english"></a>

<details>
<summary>English overview</summary>

A learning project from the Yandex Practicum backend Python course. The bot polls the homework API every ten minutes and sends the status of the first returned homework to Telegram. It validates configuration, checks API responses and logs errors.

Install `requirements.txt`, create the root `.env` file with `PRACTICUM_TOKEN`, `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`, then run `python homework.py`. Obtain the Telegram token from [@BotFather](https://t.me/BotFather). Run `python -m pytest` from the repository root for tests. The code uses the original pinned dependencies and requires working API credentials.

</details>

---

Автор: [Артём Леонов](https://github.com/artemleonich).

