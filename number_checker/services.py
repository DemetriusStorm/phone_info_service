import requests
from django.conf import settings
from django.core.cache import caches
from urllib.parse import quote
import logging
from typing import Optional, Dict, Union
from datetime import datetime

logger = logging.getLogger(__name__)
cache = caches['default']


class PhoneInfoService:
    """
    Сервис для получения информации о номере телефона через внешнее API
    с кэшированием результатов и обработкой ошибок.
    """
    BASE_URL = settings.PHONE_API_URL
    CACHE_TIMEOUT = 86400  # 24 часа в секундах

    @classmethod
    def _make_request(cls, params: Dict[str, str]) -> Optional[Union[Dict, str]]:
        """
        Базовый метод для выполнения HTTP-запроса к API
        """
        try:
            response = requests.get(
                cls.BASE_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            if 'field' in params:
                return response.text.strip()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(
                f"API request failed for params {params}. Error: {str(e)}",
                exc_info=True
            )
            return None

    @classmethod
    def get_phone_info(cls, phone_number: str) -> Optional[Dict]:
        """
        Получить полную информацию о номере телефона в формате JSON
        
        Args:
            phone_number: Номер телефона в любом формате (+7, 8, 7)
        
        Returns:
            Словарь с информацией о номере или None при ошибке
        """
        cache_key = f'phone_info_full_{phone_number}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.debug(f"Returning cached data for {phone_number}")
            return cached_data

        # Нормализация номера (удаляем все кроме цифр)
        clean_number = ''.join(c for c in phone_number if c.isdigit())
        if not clean_number:
            return None

        params = {'num': clean_number}
        data = cls._make_request(params)
        
        if data:
            # Добавляем timestamp получения данных
            data['timestamp'] = datetime.now().isoformat()
            cache.set(cache_key, data, cls.CACHE_TIMEOUT)
        
        return data

    @classmethod
    def get_specific_field(
        cls,
        phone_number: str,
        field: str,
        translit: bool = False
    ) -> Optional[str]:
        """
        Получить конкретное поле информации о номере
        
        Args:
            phone_number: Номер телефона
            field: Поле для получения (operator, region и т.д.)
            translit: Транслитерировать ли результат
        
        Returns:
            Значение поля или None при ошибке
        """
        if not field or not phone_number:
            return None

        cache_key = f'phone_field_{phone_number}_{field}_{translit}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data

        params = {
            'num': phone_number,
            'field': field
        }
        if translit:
            params['translit'] = '1'

        result = cls._make_request(params)
        if result:
            cache.set(cache_key, result, cls.CACHE_TIMEOUT)
        
        return result

    @classmethod
    def normalize_phone_number(cls, phone_number: str) -> str:
        """
        Нормализация номера телефона (только цифры)
        
        Args:
            phone_number: Номер в любом формате
        
        Returns:
            Номер, содержащий только цифры
        """
        return ''.join(c for c in phone_number if c.isdigit())

    @classmethod
    def validate_phone_number(cls, phone_number: str) -> bool:
        """
        Простая валидация номера телефона
        
        Args:
            phone_number: Номер для проверки
        
        Returns:
            True если номер выглядит валидным
        """
        clean_number = cls.normalize_phone_number(phone_number)
        return len(clean_number) in (10, 11)  # Для российских номеров