import sounddevice as sd
import numpy as np

class AudioEngine:
    """
    Core audio capture and playback engine for ClearCon.
    """

    def __init__(self, samplerate=48000, channels=2):
        self.samplerate = samplerate
        self.channels = channels
        self.buffer_size = 1024
        self.input_buffer = b""
        self.output_buffer = b""

    def capture_desktop_audio(self) -> bytes:
        """
        Capture a short chunk of desktop (loopback) audio.
        Works on Windows (WASAPI loopback) and macOS (requires Loopback or BlackHole).
        """
        try:
            data = sd.rec(
                self.buffer_size,
                samplerate=self.samplerate,
                channels=self.channels,
                dtype="float32",
            )
            sd.wait()
            return data.tobytes()
        except Exception as e:
            print(f"[AudioEngine] Desktop capture failed: {e}")
            return b""

    def play_audio(self, audio_data: bytes):
        """
        Play received audio to monitoring output.
        """
        try:
            np_data = np.frombuffer(audio_data, dtype="float32")
            np_data = np_data.reshape(-1, self.channels)
            sd.play(np_data, samplerate=self.samplerate)
            sd.wait()
        except Exception as e:
            print(f"[AudioEngine] Playback failed: {e}")
