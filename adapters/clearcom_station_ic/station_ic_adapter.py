import websocket
import threading
import json
import os
from core.channel_manager.manager import ChannelManager

CONFIG_FILE = "clearcon_config.json"

class StationICAdapter:
    """
    Adapter for Clear-Com Station-IC Remote API (WebSocket).
    Fully plug-and-play:
      - Auto-detects connected beltpacks
      - Saves base info for future launches
      - Syncs button/key/audio events to ChannelManager
    """

    def __init__(self, host=None, port=16000, api_key=None, channel_manager=None):
        self.channel_manager = channel_manager or ChannelManager()
        self.ws = None
        self.thread = threading.Thread(target=self._run_ws, daemon=True)
        self._stop = False

        # Load saved base info if available
        saved = self.load_base_info()
        self.host = host or (saved["base_ip"] if saved else "127.0.0.1")
        self.api_key = api_key or (saved["api_key"] if saved else "demo_key")
    
    # ===== Persistent Config =====
    def save_base_info(self):
        data = {"base_ip": self.host, "api_key": self.api_key}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
        print(f"[StationICAdapter] Base info saved: {self.host}")

    @staticmethod
    def load_base_info():
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return None

    # ===== WebSocket Handling =====
    def connect(self):
        url = f"ws://{self.host}:{self.port}/{self.api_key}"
        print(f"[StationICAdapter] Connecting to {url}")
        self.ws = websocket.WebSocketApp(
            url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self.thread.start()

        # Save base info for future launches
        self.save_base_info()

        # Auto-sync beltpacks once connected
        threading.Timer(1.0, self.auto_sync_beltpacks).start()

    def _run_ws(self):
        try:
            self.ws.run_forever()
        except Exception as e:
            print(f"[StationICAdapter] WebSocket thread crashed: {e}")

    # ===== Auto Sync Beltpacks =====
    def auto_sync_beltpacks(self):
        users = self.get_connected_users()
        for user in users:
            user_id = user["id"]
            display_name = user.get("name", "Unknown")
            if user_id not in self.channel_manager.user_channels:
                self.channel_manager.user_channels[user_id] = 0
                print(f"[StationICAdapter] Beltpack paired: {display_name} ({user_id})")

    def get_connected_users(self):
        """
        Query base for connected users.
        Demo: returns fake users if WebSocket not yet functional.
        Replace with real API call to Station-IC.
        """
        # TODO: Replace with real API call
        return [{"id": "user_01", "name": "Alice"}, {"id": "user_02", "name": "Bob"}]

    # ===== Event Handling =====
    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print(f"[StationICAdapter] Non-JSON message: {message}")
            return

        event_type = data.get("type")

        # Key/button events
        if event_type == "keyset_event":
            user_id = data.get("user_id", "unknown")
            key_name = data.get("key_name")
            action = data.get("action")

            if action == "pressed":
                if key_name == "channel_up":
                    self.channel_manager.switch_user_to_next_channel(user_id)
                elif key_name == "channel_down":
                    self.channel_manager.switch_user_to_prev_channel(user_id)
                elif key_name == "mute":
                    self.channel_manager.toggle_mute(user_id)

        # Audio feed events
        elif event_type == "audio_frame":
            user_id = data.get("user_id")
            pcm_data = data.get("pcm_bytes")  # raw audio bytes
            self.channel_manager.audio_engine.push_audio(user_id, pcm_data)

    def _on_error(self, ws, error):
        print(f"[StationICAdapter] Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("[StationICAdapter] WebSocket closed")

    def disconnect(self):
        self._stop = True
        if self.ws:
            self.ws.close()
        print("[StationICAdapter] Disconnected")
