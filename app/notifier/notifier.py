from django.core.mail import send_mail
from django.conf import settings

import requests
import logging


logger = logging.getLogger(__name__)


class Notifier:
    @staticmethod
    def send_email(notification):
        """Отправка email через Django email backend"""
        try:
            send_mail(
                subject=notification.title,
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Email sending failed: {e}")
            return False

    @staticmethod
    def send_sms(notification):
        """Заглушка для SMS сервиса"""
        try:
            # Интеграция с SMS провайдером
            # response = requests.post(...)
            logger.info(f"SMS sent to {notification.user.username}")
            return True  # Заглушка
        except Exception as e:
            logger.error(f"SMS sending failed: {e}")
            return False

    @staticmethod
    def send_telegram(notification):
        """Заглушка для Telegram бота"""
        try:
            # Интеграция с Telegram Bot API
            # response = requests.post(...)
            logger.info(f"Telegram message sent to {notification.user.username}")
            return True  # Заглушка
        except Exception as e:
            logger.error(f"Telegram sending failed: {e}")
            return False
