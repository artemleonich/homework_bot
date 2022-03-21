from __future__ import annotations

import logging
import os
import time
from typing import List

import requests
import telegram
from dotenv import load_dotenv
from requests import RequestException

from exceptions import MessageError
from exceptions import StatusCodeError
from exceptions import VariablesError

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.',
}


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,
)


def send_message(bot, message):
    """Метод отправки сообщения."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.info('Сообщение отправлено')
    except telegram.error.TelegramError:
        logger.error(MessageError)
        raise MessageError('Сообщение не отправлено')


def get_api_answer(current_timestamp):
    """Метод запроса к API."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except RequestException as error:
        raise ConnectionError(
            f'Ошибка доступа {error}. '
            f'Проверить API: {ENDPOINT}, '
            f'токен авторизации: {HEADERS}, '
            f'апрос с момента времени: {params}',
        )
    if response.status_code != 200:
        raise StatusCodeError(
            f'Ошибка ответа сервера. Проверить API: {ENDPOINT}, '
            f'токен авторизации: {HEADERS}, '
            f'запрос с момента времени: {params},'
            f'код возврата {response.status_code}',
        )
    return response.json()


def check_response(response) -> list:
    """Метод проверки ответа API на корректность."""
    try:
        homeworks = response['homeworks']
    except KeyError:
        logger.error('Отсутствует ключ')
        raise KeyError('Отсутствует ключ')
    if type(response['homeworks']) is not list:
        logger.error('Ответ пришел не в виде списка')
        raise TypeError('Ответ пришел не в виде списка')
    return homeworks


def parse_status(homework):
    """Метод проверки статуса домашней работы."""
    name = homework['homework_name']
    status = homework['status']
    if status not in HOMEWORK_STATUSES:
        raise ValueError(f'Неизвестный статус домашней работы {status}')
    return f'Изменился статус проверки работы "{name}". {HOMEWORK_STATUSES[status]}'


def check_tokens():
    """Метод проверки переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        return False


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Ошибка в переменных окружения')
        raise VariablesError('Проверьте значение токенов')
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if not homeworks:
                logger.info('Статус не изменился')
            else:
                send_message(bot, parse_status(homeworks[0]))
            current_timestamp = response.get('current_date', current_timestamp)
            time.sleep(RETRY_TIME)
        except Exception as error:
            logger.error(f'Сбой в работе программы: {error}')
            send_message(bot, message=f'Сбой в работе программы: {error}')
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
