from typing import Callable

class Beltpack:
    """
    Simulates a beltpack input device for testing.
    Can trigger callbacks when buttons are "pressed" virtually.
    """

    def __init__(self):
        # Dictionary of button_name -> callback
        self._callbacks = {}

    def register_button(self, button_name: str, callback: Callable):
        """
        Register a callback for a button press.
        :param button_name: e.g., 'channel_up', 'channel_down', 'mute'
        :param callback: function to call when button is pressed
        """
        self._callbacks[button_name] = callback

    def press_button(self, button_name: str):
        """
        Simulate a beltpack button press for testing.
        """
        if button_name in self._callbacks:
            self._callbacks[button_name]()
        else:
            print(f"[Warning] No callback registered for button: {button_name}")
