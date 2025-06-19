from pythonosc.udp_client import SimpleUDPClient

class OSCOutput:
    def __init__(self, target_ip, target_port):
        self.client = SimpleUDPClient(target_ip, target_port)

    def send_blob(self, blob):
        # Normalize coordinates from mm to meters (optional)
        x = blob["x"] / 1000.0
        y = blob["y"] / 1000.0
        w = blob["w"] / 1000.0
        h = blob["h"] / 1000.0
        blob_id = blob["id"]

        self.client.send_message("/person", [blob_id, x, y, w, h])
