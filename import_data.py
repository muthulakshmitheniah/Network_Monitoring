# ✅ Set up Django environment
import os
import django
import sys

# Ensure the script runs inside the Django project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set the correct Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "network_monitoring_dashboard.settings")

# Initialize Django
django.setup()

# Now import models AFTER setup
from monitoring.models import NetworkData
import json

# ✅ Load JSON data
file_path = (
    "sample_network_data.json"  # Ensure the JSON file is in the correct directory
)

with open(file_path, "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# ✅ Insert data into the database
for row in data:
    NetworkData.objects.create(
        flow_id=row["flow_id"],
        source_ip=row["source_ip"],
        source_port=row["source_port"],
        destination_ip=row["destination_ip"],
        destination_port=row["destination_port"],
        protocol=row["protocol"],
        flow_duration=row["flow_duration"],
        total_fwd_packets=row["total_fwd_packets"],
        total_bwd_packets=row["total_bwd_packets"],
        total_length_fwd=row["total_length_fwd"],
        total_length_bwd=row["total_length_bwd"],
        fwd_packet_length_max=row["fwd_packet_length_max"],
        fwd_packet_length_min=row["fwd_packet_length_min"],
        fwd_packet_length_mean=row["fwd_packet_length_mean"],
        fwd_packet_length_std=row["fwd_packet_length_std"],
        bwd_packet_length_max=row["bwd_packet_length_max"],
        bwd_packet_length_min=row["bwd_packet_length_min"],
        bwd_packet_length_mean=row["bwd_packet_length_mean"],
        bwd_packet_length_std=row["bwd_packet_length_std"],
        flow_bytes_per_second=row["flow_bytes_per_second"],
        flow_packets_per_second=row["flow_packets_per_second"],
        latency=row["latency"],
        packet_loss=row["packet_loss"],
        bandwidth=row["bandwidth"],
        uptime=row["uptime"],
        status=row["status"],
        last_checked=row["last_checked"],
    )

print("✅ Data imported successfully!")
