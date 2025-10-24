import websocket
import threading
import json
from core.channel_manager.manager import ChannelManager

class StationICAdapter:
    """
    Adapter for Clear-Com Station-IC Remote API (WebSocket).
    Detects real key press events and forwards them to the ChannelManager.
    """

    def __init__(self, api_key: str, host: str = "127.0.0.1", port: int = 16000, channel_manager: ChannelManager = None):
        self.api_key = api_key
        self.host = host
        self.port = port
        self.channel_manager = channel_manager or ChannelManager()
        self.ws = None
        self.thread = threading.Thread(target=self._run_ws, daemon=True)
        self._stop = False

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

    def _run_ws(self):
        try:
            self.ws.run_forever()
        except Exception as e:
            print(f"[StationICAdapter] WebSocket thread crashed: {e}")

    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print(f"[StationICAdapter] Non-JSON message: {message}")
            return

        event_type = data.get("type")
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

    def _on_error(self, ws, error):
        print(f"[StationICAdapter] Error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("[StationICAdapter] WebSocket closed")

    def disconnect(self):
        self._stop = True
        if self.ws:
            self.ws.close()
        print("[StationICAdapter] Disconnected")
