import logging
import os
import time
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from requests import RequestException
from telebot import TeleBot

from custom_exceptions import (
    EndpointUnavailableError, HomeworksFormatError, KeysAvailibilityError,
    ResponseFormatError, TokenAvailabilityError, APIRequestException
)


logging.basicConfig(
    format='%(lineno)d, %(asctime)s, %(levelname)s, %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """The function is for checking tokens."""
    tokens = ['PRACTICUM_TOKEN', 'TELEGRAM_TOKEN', 'TELEGRAM_CHAT_ID']
    missing_tokens = [token for token in tokens if not globals().get(token)]

    missing_tokens_text = ", ".join(missing_tokens)

    if missing_tokens:
        logger.critical(f'Not found the token-vars: {missing_tokens_text}')
        raise TokenAvailabilityError(
            f'Please, first define the vars {missing_tokens_text}'
        )
    logger.debug('Token-vars was checked and was found.')


def send_message(bot, message):
    """This function is for sending notification about status."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, text=message)
        logger.debug('Message was sent')
    except Exception as error:
        logger.error(f'Error during sending message {error}', exc_info=True)


def get_api_answer(timestamp):
    """This functions is for getting answer by API."""
    try:
        response = requests.get(
            ENDPOINT, headers=HEADERS, params={'from_date': timestamp}
        )
    except RequestException as error:
        raise APIRequestException(error)

    if response.status_code != HTTPStatus.OK:
        text = f'Endpoint is not available, got {response.status_code}'
        raise EndpointUnavailableError(text)

    logger.debug('Got success response by API Practicum')
    return response.json()


def check_response(response):
    """This function is for checking answer agree with documentation."""
    if not isinstance(response, dict):
        raise ResponseFormatError(f'Expected dict, got {type(response)}')

    if 'homeworks' not in response:
        raise HomeworksFormatError(f'Expected list, got {type(response)}')

    if not isinstance(response['homeworks'], list):
        raise HomeworksFormatError(f'Expected list, got {type(response)}')

    return True


def parse_status(homework):
    """This function is for getting needed value by dict."""
    if 'status' not in homework:
        raise KeysAvailibilityError('Expected keys: status not found')

    if 'homework_name' not in homework:
        raise KeysAvailibilityError('Expected keys: homework_name not found')

    homework_status = homework['status']

    if homework_status not in HOMEWORK_VERDICTS:
        raise KeysAvailibilityError(
            f'Type of statuses, not found. Got {homework_status}')

    verdict = HOMEWORK_VERDICTS[homework_status]
    homework_name = homework['homework_name']

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()

    bot = TeleBot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())

    while True:
        try:
            response_dict = get_api_answer(timestamp)
            if check_response(response_dict):
                if response_dict.get('homeworks'):
                    text = parse_status(response_dict['homeworks'][0])
                    send_message(bot, text)
                else:
                    logger.debug('New Homeworks statuses not found')

            timestamp = response_dict.get('current_date')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
            send_message(bot, message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
