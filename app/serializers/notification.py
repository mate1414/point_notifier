from rest_framework import serializers

from app.models import Notification, NotificationChannel, NotificationPriority


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id", "user", "title", "message",
            "channels", "priority", "status",
            "created_at", "sent_at", "delivery_channel"
        ]
        read_only_fields = ["status", "created_at", "sent_at", "delivery_channel"]


class CreateNotificationSerializer(serializers.Serializer):
    username = serializers.CharField()
    title = serializers.CharField(max_length=200)
    message = serializers.CharField()
    channels = serializers.ListField(
        child=serializers.ChoiceField(choices=NotificationChannel.choices)
    )
    priority = serializers.ChoiceField(
        choices=NotificationPriority.choices,
        default=NotificationPriority.MEDIUM
    )
