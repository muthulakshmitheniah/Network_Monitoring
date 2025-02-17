from django.urls import path


from .views import (
    dashboard_view,
    insert_20_devices_with_related,
    device_monitoring,
    device_detail,
)

urlpatterns = [
    path("", dashboard_view, name="dashboard"),  # Dashboard Page
    path("insert-all/", insert_20_devices_with_related, name="insert_20_devices"),
    path("devices-monitoring/", device_monitoring, name="device-monitoring"),
    path("device/<int:device_id>/", device_detail, name="device-detail"),
]
