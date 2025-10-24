import socket
import threading
from typing import Callable

class HCIAdapter:
    """
    Adapter for Clear-Com Eclipse HX Host Control Interface (HCI).
    Listens for beltpack key events and converts them into ClearCon core events.
    """

    def __init__(self, channel_manager, host: str, port: int = 52001):
        self.channel_manager = channel_manager
        self.host = host
        self.port = port
        self.socket = None
        self._stop = False
        self.thread = threading.Thread(target=self._event_loop, daemon=True)

    def connect(self):
        """
        Connect to the Eclipse HX system via HCI.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print(f"[HCIAdapter] Connected to {self.host}:{self.port}")
        self.thread.start()

    def _event_loop(self):
        """
        Poll for HCI events and handle them.
        """
        while not self._stop:
            data = self.socket.recv(1024)
            if data:
                self._handle_event(data)

    def _handle_event(self, data: bytes):
        """
        Parse and handle an HCI event.
        """
        # Example: Parse the event data and determine the action
        # This is a simplified example; actual parsing depends on HCI protocol specifics
        event_type = data[0]
        if event_type == 0x01:  # Key press event
            key_code = data[1]
            self._process_key_event(key_code)

    def _process_key_event(self, key_code: int):
        """
        Process a key press event.
        """
        if key_code == 0x01:  # Example: 'Channel Up' key
            self.channel_manager.switch_user_to_next_channel()
        elif key_code == 0x02:  # Example: 'Channel Down' key
            self.channel_manager.switch_user_to_prev_channel()
        elif key_code == 0x03:  # Example: 'Mute' key
            self.channel_manager.toggle_mute()

    def disconnect(self):
        """
        Disconnect from the Eclipse HX system.
        """
        self._stop = True
        if self.socket:
            self.socket.close()
        print("[HCIAdapter] Disconnected")
