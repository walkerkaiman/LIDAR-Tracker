from sklearn.cluster import DBSCAN
import numpy as np
import time

class BlobTracker:
    def __init__(self, eps, min_samples):
        self.dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        self.next_id = 0
        self.tracks = []  # [{id, x, y, w, h, last_seen}]
        self.max_inactive_time = 2.0  # seconds

    def update(self, points):
        result = []
        if len(points) == 0:
            return result

        data = np.array(points)
        labels = self.dbscan.fit_predict(data)
        now = time.time()

        new_blobs = []
        for label in set(labels):
            if label == -1:
                continue  # skip noise
            cluster = data[labels == label]
            x_min, y_min = cluster.min(axis=0)
            x_max, y_max = cluster.max(axis=0)
            cx = (x_min + x_max) / 2
            cy = (y_min + y_max) / 2
            w = x_max - x_min
            h = y_max - y_min
            new_blobs.append({"cx": cx, "cy": cy, "w": w, "h": h})

        # Match new blobs to existing tracks by nearest distance
        updated_tracks = []
        for blob in new_blobs:
            best_match = None
            best_dist = float("inf")
            for track in self.tracks:
                dist = np.hypot(blob["cx"] - track["x"], blob["cy"] - track["y"])
                if dist < 300 and dist < best_dist:
                    best_dist = dist
                    best_match = track

            if best_match:
                best_match["x"] = blob["cx"]
                best_match["y"] = blob["cy"]
                best_match["w"] = blob["w"]
                best_match["h"] = blob["h"]
                best_match["last_seen"] = now
                updated_tracks.append(best_match)
            else:
                new_id = self.next_id
                self.next_id += 1
                updated_tracks.append({
                    "id": new_id,
                    "x": blob["cx"],
                    "y": blob["cy"],
                    "w": blob["w"],
                    "h": blob["h"],
                    "last_seen": now
                })

        # Remove old tracks
        self.tracks = [t for t in updated_tracks if now - t["last_seen"] < self.max_inactive_time]

        return self.tracks