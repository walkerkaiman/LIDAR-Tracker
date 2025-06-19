import open3d as o3d
import numpy as np
import time
from threading import Lock

class Visualizer:
    def __init__(self):
        self.snapshot_requested = False
        self.toggle_osc_requested = False
        self._lock = Lock()

        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.vis.create_window("LIDAR Visualizer", width=800, height=600)

        self.pcd = o3d.geometry.PointCloud()
        self.vis.add_geometry(self.pcd)

        self.text_geom = o3d.geometry.Text3D("", [0, 0, 0], font_size=20)

        self.last_blobs = []

        self.vis.register_key_callback(ord("S"), self._snapshot_callback)
        self.vis.register_key_callback(ord("O"), self._toggle_osc_callback)

    def _snapshot_callback(self, vis):
        with self._lock:
            self.snapshot_requested = True
        return False

    def _toggle_osc_callback(self, vis):
        with self._lock:
            self.toggle_osc_requested = True
        return False

    def update(self, points, blobs, osc_enabled):
        pts = np.array(points) / 1000.0  # mm to m
        self.pcd.points = o3d.utility.Vector3dVector(np.column_stack((pts, np.zeros(len(pts)))))

        # Clear geometries except points
        self.vis.clear_geometries()
        self.vis.add_geometry(self.pcd)

        # Draw bounding boxes and labels
        for blob in blobs:
            x, y = blob["x"] / 1000.0, blob["y"] / 1000.0
            w, h = blob["w"] / 1000.0, blob["h"] / 1000.0

            corners = [
                [x - w/2, y - h/2, 0],
                [x + w/2, y - h/2, 0],
                [x + w/2, y + h/2, 0],
                [x - w/2, y + h/2, 0],
                [x - w/2, y - h/2, 0],
            ]
            line = o3d.geometry.LineSet(
                points=o3d.utility.Vector3dVector(corners),
                lines=o3d.utility.Vector2iVector([[i, i+1] for i in range(len(corners)-1)])
            )
            self.vis.add_geometry(line)

            label = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.05)
            label.translate([x, y, 0])
            self.vis.add_geometry(label)

        # Add HUD text (on-screen help)
        text_lines = [
            "Controls:",
            "[S] Save Snapshot", 
            f"[O] Toggle OSC Streaming (Currently {'ON' if osc_enabled else 'OFF'})"
        ]
        self.vis.get_render_option().point_size = 3.0
        self.vis.poll_events()
        self.vis.update_renderer()

    def close(self):
        self.vis.destroy_window()
