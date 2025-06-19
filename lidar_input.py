from pyrplidar import PyRPlidar
import math

class LidarInput:
    def __init__(self, port, baudrate):
        self.lidar = PyRPlidar()
        self.lidar.connect(port, baudrate=baudrate, timeout=3)
        self.lidar.start_motor()
        self.iterator = self.lidar.iter_scans()

    def scan_generator(self):
        for scan in self.iterator:
            points = []
            for (_, angle, distance) in scan:
                if distance > 0:
                    rad = math.radians(angle)
                    x = distance * math.cos(rad)
                    y = distance * math.sin(rad)
                    points.append((x, y))
            yield points

    def disconnect(self):
        self.lidar.stop_motor()
        self.lidar.disconnect()
