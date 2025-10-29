from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import Notification
from app.serializers.notification import (
    CreateNotificationSerializer,
    NotificationSerializer,
)
from app.tasks.notification import send_notification_task


class CreateNotificationView(APIView):
    def post(self, request) -> Response:
        serializer = CreateNotificationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(username=serializer.validated_data["username"])

                notification = Notification.objects.create(
                    user=user,
                    title=serializer.validated_data["title"],
                    message=serializer.validated_data["message"],
                    channels=serializer.validated_data["channels"],
                    priority=serializer.validated_data["priority"],
                )

                send_notification_task.delay(notification.id)

                return Response({
                    "id": notification.id,
                    "status": "queued",
                    "message": "Notification queued for delivery"
                }, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class NotificationDetailView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
