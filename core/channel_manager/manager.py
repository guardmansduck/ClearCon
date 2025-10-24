class ChannelManager:
    """
    Tracks users, channels, mute status, and links to AudioEngine.
    """

    def __init__(self, total_channels=8, audio_engine=None):
        self.total_channels = total_channels
        self.user_channels = {}  # user_id -> channel index
        self.muted_users = set()
        self.audio_engine = audio_engine or None

    def get_user_channel(self, user_id):
        return self.user_channels.get(user_id, 0)

    def switch_user_to_next_channel(self, user_id):
        current = self.get_user_channel(user_id)
        next_ch = (current + 1) % self.total_channels
        self.user_channels[user_id] = next_ch
        if self.audio_engine:
            self.audio_engine.set_user_channel(user_id, next_ch)

    def switch_user_to_prev_channel(self, user_id):
        current = self.get_user_channel(user_id)
        prev_ch = (current - 1) % self.total_channels
        self.user_channels[user_id] = prev_ch
        if self.audio_engine:
            self.audio_engine.set_user_channel(user_id, prev_ch)

    def toggle_mute(self, user_id):
        if user_id in self.muted_users:
            self.muted_users.remove(user_id)
        else:
            self.muted_users.add(user_id)

    def is_user_muted(self, user_id):
        return user_id in self.muted_users
