from typing import Callable

class Beltpack:
    """
    Beltpack input emulation. In real hardware, button events would be received
    via the Station-IC adapter’s WebSocket.
    """

    def __init__(self):
        self._callbacks = {}

    def register_button(self, button_name: str, callback: Callable):
        self._callbacks[button_name] = callback

    def press_button(self, button_name: str):
        if button_name in self._callbacks:
            print(f"[Beltpack] Button pressed: {button_name}")
            self._callbacks[button_name]()
        else:
            print(f"[Warning] No callback registered for button: {button_name}")
