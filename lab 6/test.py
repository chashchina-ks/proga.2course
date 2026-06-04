"""
Модуль с тестами для функции get_currencies.
"""

import unittest
import io
import logging
import requests
from unittest.mock import patch, MagicMock

from currencies import (
    get_currencies,
    get_currencies_iter1,
    get_currencies_iter2
)


class TestGetCurrencies(unittest.TestCase):
    """Тесты для функции get_currencies (итерация 3)"""

    def setUp(self):
        self.valid_codes = ['USD', 'EUR']

    @patch('currencies.requests.get')
    def test_successful_response(self, mock_get):
        """Успешное получение курсов валют"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5},
                "EUR": {"Value": 99.2}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies(self.valid_codes)

        self.assertIsNotNone(result)
        self.assertEqual(result['USD'], 90.5)
        self.assertEqual(result['EUR'], 99.2)

    @patch('currencies.requests.get')
    def test_missing_currency_code(self, mock_get):
        """Запрос несуществующей валюты"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies(['XYZ'])

        self.assertIsNotNone(result)
        self.assertEqual(result['XYZ'], "Код валюты 'XYZ' не найден.")

    @patch('currencies.requests.get')
    def test_api_request_error_raises_exception(self, mock_get):
        """Ошибка API — поднимается исключение"""
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        with self.assertRaises(requests.exceptions.RequestException) as context:
            get_currencies(self.valid_codes)

        self.assertEqual("Упали с исключением", str(context.exception))

    @patch('currencies.requests.get')
    def test_missing_valute_key_returns_none(self, mock_get):
        """Отсутствует ключ Valute"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"other_key": "value"}
        mock_get.return_value = mock_response

        result = get_currencies(self.valid_codes)

        self.assertIsNone(result)


class TestGetCurrenciesIter1(unittest.TestCase):
    """Тесты для итерации 1"""

    def setUp(self):
        self.captured_output = io.StringIO()

    @patch('currencies.requests.get')
    def test_successful_response(self, mock_get):
        """Успешное получение курсов"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies_iter1(['USD'], handle=self.captured_output)

        self.assertIsNotNone(result)
        self.assertEqual(result['USD'], 90.5)

    @patch('currencies.requests.get')
    def test_missing_currency_code_no_exception(self, mock_get):
        """Несуществующий код валюты"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies_iter1(['XYZ'], handle=self.captured_output)

        self.assertIsNotNone(result)
        self.assertEqual(result['XYZ'], "Код валюты 'XYZ' не найден.")

    @patch('currencies.requests.get')
    def test_api_error_raises_exception_and_logs(self, mock_get):
        """Ошибка API — исключение и запись в handle"""
        mock_get.side_effect = requests.exceptions.RequestException("Connection refused")

        with self.assertRaises(requests.exceptions.RequestException) as context:
            get_currencies_iter1(['USD'], handle=self.captured_output)

        self.assertEqual("Упали с исключением", str(context.exception))

        output = self.captured_output.getvalue()
        self.assertIn("Ошибка при запросе к API", output)
        self.assertIn("Connection refused", output)

    @patch('currencies.requests.get')
    def test_missing_valute_key_returns_none(self, mock_get):
        """Отсутствие ключа Valute"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"wrong": "structure"}
        mock_get.return_value = mock_response

        result = get_currencies_iter1(['USD'], handle=self.captured_output)

        self.assertIsNone(result)


class TestGetCurrenciesIter2(unittest.TestCase):
    """Тесты для итерации 2 (с декоратором trace)"""

    @patch('currencies.requests.get')
    def test_successful_response(self, mock_get):
        """Успешное получение курсов"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies_iter2(['USD'])

        self.assertIsNotNone(result)
        self.assertEqual(result['USD'], 90.5)

    @patch('currencies.requests.get')
    def test_missing_currency_code_no_exception(self, mock_get):
        """Несуществующий код валюты"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 90.5}
            }
        }
        mock_get.return_value = mock_response

        result = get_currencies_iter2(['XYZ'])

        self.assertIsNotNone(result)
        self.assertEqual(result['XYZ'], "Код валюты 'XYZ' не найден.")

    @patch('currencies.requests.get')
    def test_api_error_raises_exception(self, mock_get):
        """Ошибка API — исключение (без проверки лога)"""
        mock_get.side_effect = requests.exceptions.RequestException("API timeout")

        with self.assertRaises(requests.exceptions.RequestException) as context:
            get_currencies_iter2(['USD'])

        self.assertEqual("Упали с исключением", str(context.exception))

    @patch('currencies.requests.get')
    def test_missing_valute_key_returns_none(self, mock_get):
        """Отсутствие ключа Valute"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"wrong": "structure"}
        mock_get.return_value = mock_response

        result = get_currencies_iter2(['USD'])

        self.assertIsNone(result)

    @patch('currencies.requests.get')
    def test_invalid_url_raises_exception(self, mock_get):
        """Неверный URL — исключение"""
        mock_get.side_effect = requests.exceptions.InvalidURL("Invalid URL")

        with self.assertRaises(requests.exceptions.RequestException) as context:
            get_currencies_iter2(['USD'], url="https://wrong-url")

        self.assertEqual("Упали с исключением", str(context.exception))


class TestTraceDecoratorWithDifferentHandles(unittest.TestCase):
    """Тесты для декоратора trace с разными типами handle"""

    def test_trace_with_stringio_handle(self):
        """Декоратор пишет в StringIO"""
        from currencies import trace

        buffer = io.StringIO()

        @trace(handle=buffer)
        def test_func():
            raise requests.exceptions.RequestException("Test error")

        with self.assertRaises(requests.exceptions.RequestException) as context:
            test_func()

        self.assertEqual("Упали с исключением", str(context.exception))

        log_content = buffer.getvalue()
        self.assertIn("Ошибка при запросе к API", log_content)
        self.assertIn("Test error", log_content)

    def test_trace_with_logger_handle(self):
        """Декоратор работает с логгером"""
        from currencies import trace

        # Создаём логгер
        test_logger = logging.getLogger("test_logger_trace")
        test_logger.handlers.clear()
        log_buffer = io.StringIO()
        handler = logging.StreamHandler(log_buffer)
        test_logger.addHandler(handler)
        test_logger.setLevel(logging.ERROR)

        @trace(handle=test_logger)
        def test_func():
            raise requests.exceptions.RequestException("Logger test error")

        with self.assertRaises(requests.exceptions.RequestException) as context:
            test_func()

        self.assertEqual("Упали с исключением", str(context.exception))

        log_content = log_buffer.getvalue()
        self.assertIn("Ошибка при запросе к API", log_content)
        self.assertIn("Logger test error", log_content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
