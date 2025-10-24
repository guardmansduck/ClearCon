class ChannelManager:
    """
    Manages user channels, mute state, and channel switching logic.
    """

    def __init__(self, total_channels=8):
        self.total_channels = total_channels
        self.user_channels = {}
        self.muted_users = set()

    def switch_user_to_next_channel(self, user_id: str):
        current = self.user_channels.get(user_id, 0)
        new_channel = (current + 1) % self.total_channels
        self.user_channels[user_id] = new_channel
        print(f"[ChannelManager] User {user_id} switched to channel {new_channel}")

    def switch_user_to_prev_channel(self, user_id: str):
        current = self.user_channels.get(user_id, 0)
        new_channel = (current - 1) % self.total_channels
        self.user_channels[user_id] = new_channel
        print(f"[ChannelManager] User {user_id} switched to channel {new_channel}")

    def toggle_mute(self, user_id: str):
        if user_id in self.muted_users:
            self.muted_users.remove(user_id)
            print(f"[ChannelManager] User {user_id} unmuted")
        else:
            self.muted_users.add(user_id)
            print(f"[ChannelManager] User {user_id} muted")

    def get_user_channel(self, user_id: str) -> int:
        return self.user_channels.get(user_id, 0)

    def is_user_muted(self, user_id: str) -> bool:
        return user_id in self.muted_users
