from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
from django.utils.timezone import now
import json
import uuid

# pylint: disable=no-member
from .models import Device, NetworkMetric, Alert, EventLog


# Function to generate 20 devices and related records
def generate_devices_with_related_data():
    devices = []
    metrics = []
    alerts = []
    events = []

    for i in range(1, 21):  # 20 devices
        ip = f"192.168.1.{i}"
        if Device.objects.filter(ip_address=ip).exists():
            continue  # Skip existing devices

        device = Device(
            name=f"Device-{i}",
            ip_address=ip,
            mac_address=f"00:1A:2B:3C:4D:{i:02X}",
            status=random.choice(["Online", "Offline", "Warning"]),
            uptime=f"{random.randint(1, 100)} hours",
            last_checked=now(),
        )
        devices.append(device)

    created_devices = Device.objects.bulk_create(devices)

    for device in created_devices:
        metrics.append(
            NetworkMetric(
                device=device,
                flow_id=uuid.uuid4(),
                protocol=random.choice(["TCP", "UDP", "ICMP"]),
                flow_duration=random.uniform(0.1, 5.0),
                bandwidth_usage=random.uniform(10.0, 500.0),
                latency=random.uniform(1.0, 100.0),
                packet_loss=random.uniform(0.0, 10.0),
                flow_bytes_per_second=random.uniform(1000, 10000),
                flow_packets_per_second=random.uniform(10, 100),
                last_updated=now(),
            )
        )

        alerts.append(
            Alert(
                device=device,
                alert_type=random.choice(
                    ["High Latency", "Packet Loss", "High Bandwidth"]
                ),
                severity=random.choice(["Info", "Warning", "Critical"]),
                description="Generated test alert",
                triggered_at=now(),
                resolved=random.choice([True, False]),
            )
        )

        events.append(
            EventLog(
                device=device,
                event_type=random.choice(
                    ["Device Rebooted", "Configuration Changed", "Connection Lost"]
                ),
                details="Auto-generated event log entry",
                timestamp=now(),
            )
        )

    # Bulk insert related records
    NetworkMetric.objects.bulk_create(metrics)
    Alert.objects.bulk_create(alerts)
    EventLog.objects.bulk_create(events)

    return len(created_devices)


@csrf_exempt
def insert_20_devices_with_related(request):
    if request.method == "POST":
        count = generate_devices_with_related_data()
        return JsonResponse(
            {
                "message": f"{count} devices and related records inserted successfully",
                "devices_created": count,
            },
            status=201,
        )

    return JsonResponse({"error": "Invalid request method"}, status=400)


def dashboard_view(request):
    return render(request, "monitoring_tmp/dashboard.html")


def device_monitoring(request):
    devices = Device.objects.all()  # Fetch all devices
    return render(
        request, "monitoring_tmp/device_monitoring.html", {"devices": devices}
    )


def device_detail(request, device_id):
    device = Device.objects.get(id=device_id)

    # Fetch related alerts and events
    alerts = device.alerts.all()  # This will fetch all related alerts for this device
    events = device.events.all()  # This will fetch all related events for this device

    return render(
        request,
        "monitoring_tmp/device_detail.html",
        {"device": device, "alerts": alerts, "events": events},
    )
