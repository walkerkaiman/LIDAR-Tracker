# LIDAR Blob Tracker & OSC Emitter

This project reads live 2D point cloud data from an **RPLIDAR S2**, detects blobs (clusters of points), assigns persistent IDs to them, and streams their position and size over **OSC** to tools like Unity. It also includes a real-time visualizer and snapshot feature.

---

## 🧰 Features

- Real-time LIDAR data capture from **RPLIDAR S2**
- Clustering using **DBSCAN** to detect blobs
- Persistent blob IDs (up to 5 at a time)
- OSC messages in the format:
  ```
  /person [id, x, y, width, height]
  ```
- Coordinates are normalized to **meters**
- Open3D visualization with HUD & controls
- Press `S` to save a point cloud snapshot (.ply)
- Press `O` to toggle OSC output

---

## 📦 Setup

### 1. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Plug in your RPLIDAR S2

The port is typically `/dev/ttyUSB0` on Linux.

### 3. Edit `config.json`

```json
{
  "lidar_port": "/dev/ttyUSB0",
  "baud_rate": 256000,
  "osc_target_ip": "192.168.1.100",
  "osc_target_port": 9000,
  "osc_enabled": true,
  "frame_rate_limit": 10,
  "cluster_eps": 300.0,
  "cluster_min_samples": 5,
  "snapshot_dir": "snapshots"
}
```

Make sure `osc_target_ip` is the IP of the machine receiving the OSC messages (e.g. your Unity computer).

### 4. Run the program

```bash
python3 main.py
```

---

## 👁️ Controls (Open3D Visualizer)

- `S` – Save snapshot of current point cloud to `/snapshots`
- `O` – Toggle OSC streaming on/off

---

## 📁 Project Structure

```bash
├── main.py                # Runs everything
├── lidar_input.py         # Grabs live LIDAR data
├── blob_tracker.py        # Clusters and assigns IDs
├── osc_output.py          # Sends OSC messages
├── visualizer.py          # Open3D viewer and key handling
├── snapshot_exporter.py   # Saves point cloud to .ply
├── config.json            # All settings in one place
├── requirements.txt       # Python dependencies
└── snapshots/             # Saved 3D frames (.ply)
```

---

## 💡 Tips

- For best results, mount the LIDAR flat and free of obstructions.
- This system does **not** determine if a blob is human — it tracks all valid clusters.
- You can test OSC messages with tools like [OSC Monitor](https://hexler.net/products/osc) or Unity scripts.

---

## 🛠️ Troubleshooting

- 🔌 **LIDAR not detected?** Check `lidar_port` in `config.json`
- ❌ **Permission denied?** Add user to `dialout` group:
  ```bash
  sudo usermod -aG dialout $USER
  ```
- 🕳 **No blobs?** Adjust `cluster_eps` and `cluster_min_samples`

---

## 📜 License

MIT — Use freely, modify as needed.

---

## ✨ Credits

Built with ❤️ by Kaiman Walker, designed for real-time interactive installations.
