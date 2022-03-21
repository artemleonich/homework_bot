import logging
import os
import time
from http import HTTPStatus
from json import JSONDecodeError
from typing import List

import requests
from dotenv import load_dotenv
from requests import RequestException
import telegram

from exceptions import MessageError, VariablesError

load_dotenv()


PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


RETRY_TIME = 600
ENDPOINT = "https://practicum.yandex.ru/api/user_api/homework_statuses/"
HEADERS = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}


HOMEWORK_STATUSES = {
    "approved": "Работа проверена: ревьюеру всё понравилось. Ура!",
    "reviewing": "Работа взята на проверку ревьюером.",
    "rejected": "Работа проверена: у ревьюера есть замечания.",
}


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)


def send_message(bot, message):
    """Метод отправки сообщения."""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        logger.info("Сообщение отправлено")
    except telegram.error.TelegramError:
        logger.error(MessageError)
        raise MessageError("Сообщение не отправлено")


def get_api_answer(current_timestamp):
    """Метод запроса к API."""
    timestamp = current_timestamp or int(time.time())
    params = {"from_date": timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except RequestException as error:
        logger.error("В данный момент ресурс недоступен")
        raise RequestException("В данный момент ресурс недоступен")
    if response.status_code == HTTPStatus.OK:
        try:
            return response.json()
        except JSONDecodeError:
            logger.error("Ответ API не преобразуется в json")
    else:
        logger.error("Ошибка запроса")
        raise ConnectionError(
            f"Ошибка доступа {error}. "
            f"Проверить API: {ENDPOINT}, "
            f"токен авторизации: {HEADERS}, "
            f"запрос с момента времени: {params}"
        )


def check_response(response) -> List:
    """Метод проверки ответа API на корректность."""
    try:
        homeworks = response["homeworks"]
    except KeyError:
        logger.error("Отсутствует ключ")
        raise KeyError("Отсутствует ключ")
    if type(response["homeworks"]) is not list:
        logger.error("Ответ пришел не в виде списка")
        raise TypeError("Ответ пришел не в виде списка")
    return homeworks


def parse_status(homework):
    """Метод проверки статуса домашней работы."""
    homework_name = homework.get("homework_name")
    homework_status = homework.get("status")
    if len(homework) == 0:
        logger.error("Домашняя работа отсутствует")
        raise KeyError("Домашняя работа отсутствует")
    if homework_name is None:
        logger.error("Отсутствует название")
        raise KeyError("Отсутствует название")
    if homework_status is None:
        logger.error("Отсутствует статус")
        raise KeyError("Отсутствует статус")
    verdict = HOMEWORK_STATUSES[homework_status]
    if homework_status not in verdict:
        raise ValueError(
            f"Неизвестный статус домашней работы {homework_status}"
        )
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Метод проверки переменных окружения."""
    if PRACTICUM_TOKEN and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        return True
    else:
        return False


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical("Ошибка в переменных окружения")
        raise VariablesError("Проверьте значение токенов")
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    logger = logging.getLogger(__name__)
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if not homeworks:
                logger.info("Статус не изменился")
            else:
                send_message(bot, parse_status(homeworks[0]))
            current_timestamp = response.get("current_date", current_timestamp)
            time.sleep(RETRY_TIME)
        except Exception as error:
            logger.error(f"Сбой в работе программы: {error}")
            send_message(bot, message=f"Сбой в работе программы: {error}")
            time.sleep(RETRY_TIME)


if __name__ == "__main__":
    main()
