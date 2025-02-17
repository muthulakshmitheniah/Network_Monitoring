from django.urls import path
from .views_api import (
    DeviceListCreateView,
    DeviceDetailView,
    NetworkMetricListCreateView,
    DeviceMetricsView,
    AlertListCreateView,
    DeviceAlertsView,
    EventLogListCreateView,
)

urlpatterns = [
    # Devices
    path("devices/", DeviceListCreateView.as_view(), name="device-list"),
    path("devices/<int:pk>/", DeviceDetailView.as_view(), name="device-detail"),
    path(
        "devices/add/", DeviceListCreateView.as_view(), name="device-add"
    ),  # Add device view
    # Network Metrics
    path("metrics/", NetworkMetricListCreateView.as_view(), name="metric-list"),
    path(
        "devices/<int:device_id>/metrics/",
        DeviceMetricsView.as_view(),
        name="device-metrics",
    ),
    # Alerts
    path("alerts/", AlertListCreateView.as_view(), name="alert-list"),
    path(
        "devices/<int:device_id>/alerts/",
        DeviceAlertsView.as_view(),
        name="device-alerts",
    ),
    # Event Logs
    path("eventlogs/", EventLogListCreateView.as_view(), name="eventlog-list"),
    path("devices/", DeviceListCreateView.as_view(), name="device-list"),
]
