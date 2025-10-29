import logging


from celery import shared_task

from app.models import Notification, NotificationChannel, NotificationStatus
from app.notifier.notifier import Notifier
from app.notifier.strategy import DeliveryStrategy

logger = logging.getLogger(__name__)


CHANNEL_TYPE_METHOD_MAP = {
    NotificationChannel.EMAIL: Notifier.send_email,
    NotificationChannel.TELEGRAM: Notifier.send_telegram,
    NotificationChannel.SMS: Notifier.send_sms,
}


@shared_task(bind=True, max_retries=3)
def send_notification_task(self, notification_id: int):
    try:
        notification = Notification.objects.get(id=notification_id)
        strategy = DeliveryStrategy(notification.channels)

        while strategy.has_next():
            channel = strategy.get_next_channel()
            success = False

            try:
                if channel.type in CHANNEL_TYPE_METHOD_MAP:
                    success = CHANNEL_TYPE_METHOD_MAP[channel.type](notification)

                if success:
                    notification.status = NotificationStatus.SENT
                    notification.delivery_channel = channel
                    notification.save()

                    logger.info(f"Notification {notification_id} delivered via {channel}")
                    return f"Delivered via {channel}"

            except Exception as exc:
                logger.warning(f"Channel {channel} failed for notification {notification_id}: {exc}")
                continue

        # Если все каналы не сработали
        notification.status = NotificationStatus.FAILED
        notification.save()

        logger.error(f"All delivery channels failed for notification {notification_id}")

        raise self.retry(countdown=60)

    except Notification.DoesNotExist:
        logger.error(f"Notification {notification_id} not found")

    except Exception as exc:
        logger.error(f"Unexpected error for notification {notification_id}: {exc}")
        raise self.retry(countdown=60, exc=exc)
