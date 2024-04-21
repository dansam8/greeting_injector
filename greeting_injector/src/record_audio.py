import sounddevice as sd
import numpy as np
import wavio


AGGREGATE_AUDIO_DEVICE_NAME = "mycrophone"


def record_audio(outfile):
    
    assert outfile.endswith('.wav'), "Output file must be a WAV file."

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recording.append(indata.copy())

    try:
        device_index = [dev['name'] for dev in sd.query_devices()].index(AGGREGATE_AUDIO_DEVICE_NAME)
    except ValueError:
        raise ValueError("Specified device not found. Please check your device name.")

    # Parameters for recording
    fs = 44100  # Sample rate
    channels = 1  # Number of channels
    frames_per_buffer = 1024  # Buffer size for recording

    print("Press Enter to start recording...")
    input()  # Wait for Enter press to start
    print("Recording... Press Enter to stop.")

    recording = []  # List to store recorded frames

    # Start recording
    with sd.InputStream(samplerate=fs, channels=channels, callback=callback, blocksize=frames_per_buffer, device=device_index):
        input()  # Wait for Enter press to stop

    # Normalize to int16 (standard for WAV files)
    recording_normalized = np.concatenate(recording, axis=0)
    recording_normalized = (recording_normalized * np.iinfo(np.int16).max).astype(np.int16)

    # Save to WAV file
    wavio.write(outfile, recording_normalized, fs, sampwidth=2)
    print(f"Recording saved as {outfile}")