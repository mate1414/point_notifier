from django.contrib import admin

from app.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "priority",
        "status",
        "delivery_channel",
        "created_at",
        "sent_at",
    ]

    list_filter = [
        "status",
        "priority",
        "delivery_channel",
        "created_at"
    ]

    readonly_fields = [
        "created_at",
        "sent_at",
        "status",
        "delivery_channel"
    ]


admin.site.register(Notification, NotificationAdmin)
