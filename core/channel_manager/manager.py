class ChannelManager:
    """
    Manages user channels and responds to key events (from Station-IC or other adapters).
    """

    def __init__(self):
        # Map user_id to channel number
        self.user_channels = {}
        # Map user_id to mute status
        self.muted_users = set()

    def switch_user_to_next_channel(self, user_id: str):
        current = self.user_channels.get(user_id, 0)
        new_channel = current + 1
        # TODO: wrap or limit channel range
        self.user_channels[user_id] = new_channel
        print(f"[ChannelManager] User {user_id} switched to channel {new_channel}")

    def switch_user_to_prev_channel(self, user_id: str):
        current = self.user_channels.get(user_id, 0)
        new_channel = max(0, current - 1)
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
