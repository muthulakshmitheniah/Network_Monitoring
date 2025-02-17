from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid


class User(AbstractUser):
    # Add related_name to prevent conflicts with Django's default User model
    groups = models.ManyToManyField(
        "auth.Group", related_name="monitoring_users", blank=True  # Custom related name
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="monitoring_users_permissions",  # Custom related name
        blank=True,
    )

    # pylint: disable=invalid-str-returned
    def __str__(self):
        return self.username


# Device Model (Stores Network Devices and Their Status)
class Device(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(unique=True)
    mac_address = models.CharField(max_length=50, unique=True, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("Online", "Online"), ("Offline", "Offline"), ("Warning", "Warning")],
        default="Online",
    )
    uptime = models.CharField(max_length=50, null=True, blank=True)
    last_checked = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"

    def __str__(self):
        return f"{self.name} - {self.ip_address} ({self.status})"


# Network Metrics Model (Stores Real-Time Network Statistics)
class NetworkMetric(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="metrics")
    flow_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    protocol = models.CharField(max_length=20)
    flow_duration = models.FloatField(null=True, blank=True)
    bandwidth_usage = models.FloatField(null=True, blank=True)  # Mbps
    latency = models.FloatField(null=True, blank=True)  # ms
    packet_loss = models.FloatField(null=True, blank=True)  # %
    flow_bytes_per_second = models.FloatField(null=True, blank=True)
    flow_packets_per_second = models.FloatField(null=True, blank=True)
    last_updated = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Network Metric"
        verbose_name_plural = "Network Metrics"

    def __str__(self):
        return f"{self.device.name} - {self.protocol} - {self.bandwidth_usage} Mbps"


# Alert Model (Triggers Alerts for Anomalies)
class Alert(models.Model):
    SEVERITY_LEVELS = [
        ("Info", "Info"),
        ("Warning", "Warning"),
        ("Critical", "Critical"),
    ]

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="alerts")
    alert_type = models.CharField(max_length=100)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS, default="Info")
    description = models.TextField()
    triggered_at = models.DateTimeField(default=now)
    resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"

    def __str__(self):
        return f"{self.device.name} - {self.alert_type} ({self.severity})"


# Event Log Model (Stores Network Events for Historical Analysis)
class EventLog(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=100)
    details = models.TextField()
    timestamp = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Event Log"
        verbose_name_plural = "Event Logs"

    def __str__(self):
        return f"{self.device.name} - {self.event_type} - {self.timestamp}"
