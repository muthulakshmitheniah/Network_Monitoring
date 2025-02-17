from rest_framework import serializers

# pylint: disable=no-member
from .models import Device, NetworkMetric, Alert, EventLog


class NetworkMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkMetric
        fields = [
            "protocol",
            "flow_duration",
            "bandwidth_usage",
            "latency",
            "packet_loss",
        ]


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ["alert_type", "severity", "description"]


class EventLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLog
        fields = ["event_type", "details"]


class DeviceSerializer(serializers.ModelSerializer):
    metrics = NetworkMetricSerializer(many=True, required=False)
    alerts = AlertSerializer(many=True, required=False)
    events = EventLogSerializer(many=True, required=False)

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "ip_address",
            "mac_address",
            "status",
            "uptime",
            "last_checked",
            "metrics",
            "alerts",
            "events",
        ]

    def create(self, validated_data):
        # Extract related data before creating the device
        metrics_data = validated_data.pop("metrics", [])
        alerts_data = validated_data.pop("alerts", [])
        events_data = validated_data.pop("events", [])

        # Create the Device first
        device = Device.objects.create(**validated_data)

        # Assign related objects to this device
        NetworkMetric.objects.bulk_create(
            [
                NetworkMetric(device=device, **metric_data)
                for metric_data in metrics_data
            ]
        )

        Alert.objects.bulk_create(
            [Alert(device=device, **alert_data) for alert_data in alerts_data]
        )

        EventLog.objects.bulk_create(
            [EventLog(device=device, **event_data) for event_data in events_data]
        )

        return device

    def update(self, instance, validated_data):
        """Handles updating a device and its related metrics, alerts, and events"""
        # Update Device Fields
        instance.name = validated_data.get("name", instance.name)
        instance.ip_address = validated_data.get("ip_address", instance.ip_address)
        instance.mac_address = validated_data.get("mac_address", instance.mac_address)
        instance.status = validated_data.get("status", instance.status)
        instance.uptime = validated_data.get("uptime", instance.uptime)
        instance.last_checked = validated_data.get(
            "last_checked", instance.last_checked
        )
        instance.save()

        # Handle Related Metrics
        metrics_data = validated_data.pop("metrics", [])
        instance.metrics.all().delete()  # Delete existing metrics
        NetworkMetric.objects.bulk_create(
            [
                NetworkMetric(device=instance, **metric_data)
                for metric_data in metrics_data
            ]
        )

        # Handle Related Alerts
        alerts_data = validated_data.pop("alerts", [])
        instance.alerts.all().delete()  # Delete existing alerts
        Alert.objects.bulk_create(
            [Alert(device=instance, **alert_data) for alert_data in alerts_data]
        )

        # Handle Related Events
        events_data = validated_data.pop("events", [])
        instance.events.all().delete()  # Delete existing events
        EventLog.objects.bulk_create(
            [EventLog(device=instance, **event_data) for event_data in events_data]
        )

        return instance

    def get_bandwidth(self, obj):
        latest_metric = (
            NetworkMetric.objects.filter(device=obj).order_by("-last_updated").first()
        )
        return (
            round(latest_metric.bandwidth_usage, 2)
            if latest_metric and latest_metric.bandwidth_usage is not None
            else None
        )

    def get_latency(self, obj):
        latest_metric = (
            NetworkMetric.objects.filter(device=obj).order_by("-last_updated").first()
        )
        return (
            round(latest_metric.latency, 2)
            if latest_metric and latest_metric.latency is not None
            else None
        )
