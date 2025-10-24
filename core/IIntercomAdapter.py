from abc import ABC, abstractmethod

class IIntercomAdapter(ABC):
    """
    Abstract interface for all intercom adapters.
    Any adapter (Eclipse HX, Arcadia, HME DX, etc.) must implement these methods.
    """

    @abstractmethod
    def send_audio(self, channel: int, audio_data: bytes):
        """
        Send audio to a specific channel.
        :param channel: Channel number
        :param audio_data: Raw audio bytes
        """
        pass

    @abstractmethod
    def receive_audio(self, channel: int) -> bytes:
        """
        Receive audio from a specific channel.
        :param channel: Channel number
        :return: Raw audio bytes
        """
        pass

    @abstractmethod
    def set_volume(self, channel: int, level: float):
        """
        Set the output volume for a specific channel.
        :param channel: Channel number
        :param level: Volume level (0.0 - 1.0)
        """
        pass

    @abstractmethod
    def switch_channel(self, user_id: str, channel: int):
        """
        Switch a user to a different channel.
        :param user_id: Unique identifier for the user
        :param channel: Channel number
        """
        pass
