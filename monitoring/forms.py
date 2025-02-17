from django import forms
from .models import Device, NetworkMetric, Alert, EventLog


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = [
            "name",
            "ip_address",
            "mac_address",
            "status",
            "uptime",
            "last_checked",
        ]

    # Add custom validation if needed for fields like IP Address format, etc.


class NetworkMetricForm(forms.ModelForm):
    class Meta:
        model = NetworkMetric
        fields = [
            "protocol",
            "flow_duration",
            "bandwidth_usage",
            "latency",
            "packet_loss",
        ]

    # Custom form logic can be added here if needed.


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ["alert_type", "severity", "description"]


class EventLogForm(forms.ModelForm):
    class Meta:
        model = EventLog
        fields = ["event_type", "details"]
