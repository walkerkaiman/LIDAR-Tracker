import os
import json
import time
from lidar_input import LidarInput
from blob_tracker import BlobTracker
from osc_output import OSCOutput
from visualizer import Visualizer
from snapshot_exporter import SnapshotExporter

CONFIG_PATH = "config.json"

# Load configuration
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

# Ensure snapshot directory exists
os.makedirs(config["snapshot_dir"], exist_ok=True)

# Initialize modules
lidar = LidarInput(config["lidar_port"], config["baud_rate"])
tracker = BlobTracker(config["cluster_eps"], config["cluster_min_samples"])
osc = OSCOutput(config["osc_target_ip"], config["osc_target_port"])
exporter = SnapshotExporter(config["snapshot_dir"])
visualizer = Visualizer()

osc_enabled = config.get("osc_enabled", True)
frame_delay = 1.0 / config.get("frame_rate_limit", 10)

print("Starting LIDAR tracker...")

try:
    for points in lidar.scan_generator():
        blobs = tracker.update(points)

        if osc_enabled:
            for blob in blobs:
                osc.send_blob(blob)

        visualizer.update(points, blobs, osc_enabled)

        if visualizer.snapshot_requested:
            exporter.save_snapshot(points, blobs)
            visualizer.snapshot_requested = False

        if visualizer.toggle_osc_requested:
            osc_enabled = not osc_enabled
            visualizer.toggle_osc_requested = False

        time.sleep(frame_delay)

except KeyboardInterrupt:
    print("\nExiting LIDAR tracker...")
    lidar.disconnect()
    visualizer.close()
    exit(0)