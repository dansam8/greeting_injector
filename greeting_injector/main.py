import sounddevice as sd
import argh

from greeting_injector.src.default_device_monitor import DefaultDeviceMonitor
from greeting_injector.src.play_audio_threaded import play_audio
from greeting_injector.src.record_audio import record_audio


VIRTUAL_DEVICE_NAME = "BlackHole 2ch"
RECORDING_FILENAME = "../recording.wav"


def greet(mirror_audio=True):

    ddm = DefaultDeviceMonitor()

    try:
        try:
            device_index = [dev['name'] for dev in sd.query_devices()].index(VIRTUAL_DEVICE_NAME)
        except ValueError:
            raise ValueError("Specified device not found. Please check your device name.")

        while True:
            devices = [device_index]
            if mirror_audio:
                devices.append(ddm.get_default_output_device())

            input("Press Enter to play the greeting. Press Ctrl+C to exit.")  # Wait for Enter press
            play_audio('../recording.wav', devices=devices)
            print("Playback finished.")

    except KeyboardInterrupt:
        print("Stopping")
    finally:
        ddm.stop()
        print("Stopped monitoring default audio device.")


def record():
    record_audio(RECORDING_FILENAME)


def main():
    argh.dispatch_commands([greet, record])
