import open3d as o3d
import numpy as np
import os
from datetime import datetime

class SnapshotExporter:
    def __init__(self, directory):
        self.directory = directory

    def save_snapshot(self, points, blobs):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.directory, f"snapshot_{timestamp}.ply")

        cloud = o3d.geometry.PointCloud()
        pts = np.array(points) / 1000.0
        cloud.points = o3d.utility.Vector3dVector(np.column_stack((pts, np.zeros(len(pts)))))

        o3d.io.write_point_cloud(file_path, cloud)
        print(f"📸 Snapshot saved to {file_path}")
