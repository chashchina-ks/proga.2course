"""
Модуль для получения курсов валют с API ЦБ РФ.
Полностью соответствует теоретическим требованиям.
"""

import sys
import functools
import logging
import requests
from typing import Optional, Dict, List, Union, Any


# итерация 3 (финальная) — с logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def _log_error(handle: Union[Any, logging.Logger], message: str) -> None:
    """
    Универсальная функция для логирования.
    Определяет тип handle и вызывает соответствующий метод.
    """
    if hasattr(handle, 'error') and callable(getattr(handle, 'error')):
        handle.error(message)
    elif hasattr(handle, 'write'):
        handle.write(message + "\n")
        if hasattr(handle, 'flush'):
            handle.flush()
    else:
        print(message)


def trace(handle: Union[Any, logging.Logger] = sys.stdout):
    """
    Декоратор для логирования ошибок.
    Умеет работать как с потоками (write), так и с логгерами (error/info/warning).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.RequestException as e:
                _log_error(handle, f"Ошибка при запросе к API: {e}")
                raise requests.exceptions.RequestException("Упали с исключением")
            except KeyError as e:
                _log_error(handle, f"Ошибка: в ответе API отсутствуют курсы валют - {e}")
                return None
            except Exception as e:
                _log_error(handle, f"Неожиданная ошибка: {e}")
                raise
        return wrapper
    return decorator


@trace()
def get_currencies(
        currency_codes: List[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Optional[Dict[str, Union[float, str]]]:
    """
    Получает курсы валют с API Центробанка России.
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if "Valute" not in data:
        return None

    currencies = {}
    for code in currency_codes:
        if code in data["Valute"]:
            currencies[code] = data["Valute"][code]["Value"]
        else:
            currencies[code] = f"Код валюты '{code}' не найден."

    return currencies

# итерация 1 (базовая, с явной обработкой ошибок)

def get_currencies_iter1(
        currency_codes: List[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js",
        handle=sys.stdout
) -> Optional[Dict[str, Union[float, str]]]:
    """
    Версия итерации 1.
    При ошибках API поднимает исключение.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        handle.write(f"Ошибка при запросе к API: {e}\n")
        handle.flush()
        raise requests.exceptions.RequestException("Упали с исключением")

    if "Valute" not in data:
        return None

    result = {}
    for code in currency_codes:
        if code in data["Valute"]:
            result[code] = data["Valute"][code]["Value"]
        else:
            result[code] = f"Код валюты '{code}' не найден."

    return result

# итерация 2 (с декоратором trace) - ПРАВИЛЬНАЯ ВЕРСИЯ

@trace()  # декоратор должен быть применён
def get_currencies_iter2(
        currency_codes: List[str],
        url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
) -> Optional[Dict[str, Union[float, str]]]:
    """
    Версия с декоратором trace.
    """
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    if "Valute" not in data:
        return None

    result = {}
    for code in currency_codes:
        if code in data["Valute"]:
            result[code] = data["Valute"][code]["Value"]
        else:
            result[code] = f"Код валюты '{code}' не найден."

    return result
