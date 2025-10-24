import requests

class StationICAdapter:
    """
    Adapter for Clear-Com Station-IC Remote API.
    Provides methods to control Station-IC functionalities.
    """

    def __init__(self, api_url: str):
        self.api_url = api_url

    def press_key(self, key_name: str):
        """
        Simulate a key press on Station-IC.
        """
        response = requests.post(f"{self.api_url}/key/{key_name}/press")
        if response.status_code == 200:
            print(f"[StationICAdapter] Key '{key_name}' pressed successfully.")
        else:
            print(f"[StationICAdapter] Failed to press key '{key_name}'.")

    def release_key(self, key_name: str):
        """
        Simulate a key release on Station-IC.
        """
        response = requests.post(f"{self.api_url}/key/{key_name}/release")
        if response.status_code == 200:
            print(f"[StationICAdapter] Key '{key_name}' released successfully.")
        else:
            print(f"[StationICAdapter] Failed to release key '{key_name}'.")

    def set_volume(self, volume_level: int):
        """
        Set the volume level on Station-IC.
        """
        response = requests.post(f"{self.api_url}/volume", json={"level": volume_level})
        if response.status_code == 200:
            print(f"[StationICAdapter] Volume set to {volume_level}.")
        else:
            print(f"[StationICAdapter] Failed to set volume.")
