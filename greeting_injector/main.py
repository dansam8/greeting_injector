import time

import sounddevice as sd
import argh

from greeting_injector.src.default_device_monitor import DefaultDeviceMonitor
from greeting_injector.src.record_audio import record_audio
from greeting_injector.src.fast_audio_player import FastAudioPlayer


VIRTUAL_DEVICE_NAME = "BlackHole 2ch"
RECORDING_FILENAME = "recording.wav"


def greet(mirror_audio=True):

    try:
        device_index = [dev['name'] for dev in sd.query_devices()].index(VIRTUAL_DEVICE_NAME)
    except ValueError:
        raise ValueError("Specified device not found. Please check your device name.")

    ddm = DefaultDeviceMonitor()
    fap_mirror = FastAudioPlayer(RECORDING_FILENAME, ddm.get_default_output_device())  # todo no updateing device but luss for now
    fap_in = FastAudioPlayer(RECORDING_FILENAME, device_index)

    try:
        while True:
            input("Press Enter to play the greeting. Press Ctrl+C to exit.")  # Wait for Enter press
            fap_in.play()
            fap_mirror.play()
            time.sleep(3)

    except KeyboardInterrupt:
        print("Stopping")
    finally:
        ddm.stop()
        print("Stopped monitoring default audio device.")


def record():
    record_audio(RECORDING_FILENAME)


def main():
    argh.dispatch_commands([greet, record])
