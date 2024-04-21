import sounddevice as sd
import threading
import time


class DefaultDeviceMonitor:
    """Monitors the default audio output device in a thread"""

    def __init__(self):
        self._running = True
        self._thread = threading.Thread(target=self._monitor)
        self._thread.start()

    def _monitor(self):
        last_known_device = self.get_default_output_device()
        while self._running:
            current_device = self.get_default_output_device()
            if current_device != last_known_device:
                print("Output device changed to:", current_device)
                last_known_device = current_device
            time.sleep(1)

    @staticmethod
    def get_default_output_device():
        return sd.query_devices(kind='output')['name']

    def stop(self):
        self._running = False
        self._thread.join()
