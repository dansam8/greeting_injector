from typing import List

import sounddevice as sd
import numpy as np
import wave
import threading


def play_audio(file_path, devices: List[int] = []):

    def play_thread(audio_data, framerate, device):
        sd.play(audio_data, framerate, device=device)
        sd.wait()

    # Load the file
    with wave.open(file_path, 'rb') as wf:

        # Extract audio data
        data = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(data, dtype=np.int16)

    threads = []

    for device in devices:
        t = threading.Thread(target=play_thread, args=(audio_data, wf.getframerate(), device))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
