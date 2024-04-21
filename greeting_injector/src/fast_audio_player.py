import numpy as np
import sounddevice as sd
import wave


class FastAudioPlayer:
    def __init__(self, file_path, device: int=None):
        self.file_path = file_path  # Store file path
        self.device = device
        self.audio_data = None  # Array to hold preloaded audio data
        self.current_frame = 0  # Index to keep track of playback position
        self.is_playing = False  # Playback state flag
        self.stream = None      # Placeholder for the audio stream
        self.load_audio(file_path)  # Load audio data from file and setup stream

    def load_audio(self, file_path):
        """ Preload audio data from a WAV file and setup the stream according to the audio file specs. """
        with wave.open(file_path, 'rb') as wf:
            self.samplerate = wf.getframerate()  # Get the sample rate from the file
            data = wf.readframes(wf.getnframes())
            self.audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768  # Normalize audio data
            self.setup_stream(self.samplerate, wf.getnchannels())  # Setup the stream

    def setup_stream(self, samplerate, channels):
        """ Set up the audio stream with the callback. """
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
        self.stream = sd.OutputStream(callback=self.audio_callback,
                                      samplerate=samplerate,
                                      channels=channels,
                                      device=self.device,
                                      dtype='float32')
        self.stream.start()

    def audio_callback(self, outdata, frames, time, status):
        """ Fill the output buffer with audio data if playback is triggered. """
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        if self.is_playing and self.audio_data is not None:
            end_index = self.current_frame + frames
            if end_index < len(self.audio_data):
                outdata[:, 0] = self.audio_data[self.current_frame:end_index]
                self.current_frame = end_index
            else:
                remaining_frames = len(self.audio_data) - self.current_frame
                outdata[:remaining_frames, 0] = self.audio_data[self.current_frame:]
                outdata[remaining_frames:] = 0
                self.is_playing = False  # Stop playback after data ends
        else:
            outdata.fill(0)  # Fill buffer with zeros if not playing

    def play(self):
        """ Trigger playback of the preloaded audio. """
        self.is_playing = True
        self.current_frame = 0  # Reset playback to start

    def stop(self):
        """ Stop the playback. """
        self.is_playing = False

    def close_stream(self):
        """ Properly close the audio stream. """
        if self.stream:
            self.stream.stop()
            self.stream.close()

# Example usage
if __name__ == "__main__":
    import time
    player = FastAudioPlayer("../../recording.wav")  # Provide a valid WAV file path
    print("System ready. Press Enter to start playback...")
    input()  # Wait for user input to start playback
    player.play()

    print("System ready. Press Enter to start playback...")
    input()  # Wait for user input to start playback
    player.play()
    time.sleep(5)  # Allow some time for playback
    player.stop()
    player.close_stream()