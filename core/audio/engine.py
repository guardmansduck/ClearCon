import numpy as np
import sounddevice as sd

class AudioEngine:
    """
    Handles real base audio per user, per-channel volume, auto-limiter, and levels.
    """

    def __init__(self):
        self.user_channels = {}        # user_id -> channel
        self.muted_users = set()
        self.user_volumes = {}         # user_id -> 0.0-1.0
        self.channel_levels = {}       # user_id -> 0.0-1.0
        self.buffers = {}              # user_id -> list of numpy arrays

        self.playback_stream = sd.OutputStream(channels=2, samplerate=48000)
        self.playback_stream.start()

    def set_user_volume(self, user_id, volume: float):
        self.user_volumes[user_id] = np.clip(volume, 0.0, 1.0)

    def push_audio(self, user_id, pcm_bytes):
        if user_id in self.muted_users:
            return

        data = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0

        # Apply per-user volume
        vol = self.user_volumes.get(user_id, 1.0)
        data *= vol

        # Auto-limiter
        data = np.clip(data, -0.8, 0.8)

        self.buffers.setdefault(user_id, []).append(data)

        # Update UI meter RMS
        level = np.sqrt(np.mean(data**2))
        self.channel_levels[user_id] = float(np.clip(level, 0, 1))

        self.mix_and_play()

    def mix_and_play(self):
        if not self.buffers:
            return
        mix = None
        for user_id, buf_list in self.buffers.items():
            if buf_list:
                data = buf_list.pop(0)
                if mix is None:
                    mix = data
                else:
                    mix = np.add(mix, data, out=mix, casting="unsafe")
        if mix is not None:
            mix = np.clip(mix, -1.0, 1.0)
            self.playback_stream.write((mix * 32767).astype(np.int16))
