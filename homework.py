import logging
import os
import time
from http import HTTPStatus
from json import JSONDecodeError
from typing import List


import requests
from dotenv import load_dotenv
from requests import RequestException
from telegram import Bot, TelegramError

from exceptions import EnvironmentVariablesException

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

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(funcName)s -  %(message)s",
    filename="homework.log",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def send_message(bot, message):
    """Отправка сообщения в чат."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
        logger.info("Сообщение отправлено")
    except TelegramError as error:
        logger.info(f"Ошибка {error} при отправке сообщения")


def get_api_answer(current_timestamp):
    """Запрос к серверу."""
    timestamp = current_timestamp or int(time.time())
    params = {"from_date": timestamp}
    headers = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}
    try:
        homework_statuses = requests.get(
            ENDPOINT, headers=headers, params=params
        )
    except RequestException:
        logger.error("Yandex URL недоступен")
        raise RequestException("Yandex URL недоступен")
    if homework_statuses.status_code == HTTPStatus.OK:
        try:
            return homework_statuses.json()
        except JSONDecodeError:
            logger.error("Не удалось преобразовать в json-ответ")
    else:
        logger.error("Ошибка при запросе к основному API")
        raise ConnectionError


def check_response(response) -> List:
    """Валидация ответов API."""
    try:
        homeworks = response["homeworks"]
    except KeyError:
        logger.error("В ответе отсутсвуют ключ homeworks")
        raise KeyError("В ответе отсутсвуют ключ homeworks")
    if type(response["homeworks"]) is not list:
        logger.error("API вернул не список")
        raise TypeError("API вернул не список")
    if "current_date" not in response:
        logger.error("В ответе отсутсвуют ключ current_date")
        raise KeyError("В ответе отсутсвуют ключ current_date")
    return homeworks


def parse_status(homework):
    """Извлекает информацию о статусе конкретной работы."""
    if len(homework) == 0:
        logger.error("Нет информации о домашней работе. Словарь пуст.")
        raise KeyError("Нет словаря домашней работы")
    if homework.get("homework_name") is None:
        logger.error("Нет наименования домашней работы")
        raise KeyError("Нет наименования домашней работы")
    homework_name = homework.get("homework_name")
    if homework.get("status") is None:
        logger.error("Нет статуса домашней работы")
        raise KeyError("Нет статуса домашней работы")
    homework_status = homework.get("status")
    if homework_status not in HOMEWORK_STATUSES:
        logger.error("Нет статуса в словаре ")
        raise KeyError("Нет такого статуса")
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка сетевого окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical("Отсутствуют переменные окружения!")
        raise EnvironmentVariablesException()
    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    error_message = None

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homework = check_response(response)[0]
            if homework:
                status_message = parse_status(homework)
                send_message(bot, status_message)
            else:
                logging.debug(
                    "Статус задания не изменился с последней проверки"
                )
            current_timestamp = response.get("currrent_date")
            time.sleep(RETRY_TIME)
        except Exception as error:
            message = f"Сбой в работе программы: {error}"
            if error_message != message:
                error_message = message
                send_message(bot, message)
            time.sleep(RETRY_TIME)


if __name__ == "__main__":
    main()
