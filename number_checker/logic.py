from typing import Optional
from django.contrib.auth import get_user_model
from .models import PhoneNumber, QueryHistory
from .services import PhoneInfoService
from django.http import HttpRequest

User = get_user_model()

class PhoneNumberManager:
    @staticmethod
    def process_phone_number(
        phone_number: str,
        request: Optional[HttpRequest] = None
    ) -> Optional[PhoneNumber]:
        """
        Основной метод обработки номера:
        - проверка в кэше/БД
        - запрос к API при необходимости
        - сохранение результатов
        - запись истории
        """
        # Нормализация номера
        clean_number = PhoneInfoService.normalize_phone_number(phone_number)
        if not PhoneInfoService.validate_phone_number(clean_number):
            return None

        # Пытаемся найти в БД
        try:
            phone_obj = PhoneNumber.objects.get(full_number=clean_number[-10:])
            is_new = False
        except PhoneNumber.DoesNotExist:
            # Если нет в БД - запрашиваем API
            api_data = PhoneInfoService.get_phone_info(clean_number)
            if not api_data:
                return None

            phone_obj = PhoneNumber.objects.create(
                full_number=clean_number[-10:],
                code=api_data.get('code'),
                number=api_data.get('num'),
                operator=api_data.get('operator'),
                old_operator=api_data.get('old_operator'),
                region=api_data.get('region')
            )
            is_new = True

        # Записываем историю запроса
        if request:
            QueryHistory.objects.create(
                user=request.user if request.user.is_authenticated else None,
                phone_number=phone_obj,
                ip_address=PhoneNumberManager.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

        return phone_obj

    @staticmethod
    def get_client_ip(request: HttpRequest) -> str:
        """Получение IP клиента с учетом заголовков прокси"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', '')