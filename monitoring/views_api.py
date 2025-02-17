from rest_framework import generics

# pylint: disable=no-member
from .models import Device, NetworkMetric, Alert, EventLog
from .serializers import (
    DeviceSerializer,
    NetworkMetricSerializer,
    AlertSerializer,
    EventLogSerializer,
)


# Device API (List & Create)
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# Device API (Retrieve, Update, Delete)
class DeviceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# Network Metric API (List & Create)
class NetworkMetricListCreateView(generics.ListCreateAPIView):
    queryset = NetworkMetric.objects.all()
    serializer_class = NetworkMetricSerializer


# Metrics for a Specific Device
class DeviceMetricsView(generics.ListAPIView):
    serializer_class = NetworkMetricSerializer

    def get_queryset(self):
        device_id = self.kwargs["device_id"]
        return NetworkMetric.objects.filter(device_id=device_id)


# Alert API (List & Create)
class AlertListCreateView(generics.ListCreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


# Alerts for a Specific Device
class DeviceAlertsView(generics.ListAPIView):
    serializer_class = AlertSerializer

    def get_queryset(self):
        device_id = self.kwargs["device_id"]
        return Alert.objects.filter(device_id=device_id)


# Event Log API (List & Create)
class EventLogListCreateView(generics.ListCreateAPIView):
    queryset = EventLog.objects.all()
    serializer_class = EventLogSerializer
