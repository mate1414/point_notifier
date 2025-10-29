from django.contrib.auth.models import User
from django.db import models


class NotificationChannel(models.TextChoices):
    EMAIL = "email", "Email"
    SMS = "sms", "SMS"
    TELEGRAM = "telegram", "Telegram"


class NotificationPriority(models.TextChoices):
    HIGH = "high", "High"
    MEDIUM = "medium", "Medium"


class NotificationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    FAILED = "failed", "Failed"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    channels = models.JSONField()
    priority = models.CharField(
        max_length=10,
        choices=NotificationPriority.choices,
        default=NotificationPriority.MEDIUM
    )
    status = models.CharField(max_length=20, default=NotificationStatus.PENDING, choices=NotificationPriority.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivery_channel = models.CharField(
        max_length=10,
        choices=NotificationChannel.choices,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Notification for {self.user.username} - {self.status}"