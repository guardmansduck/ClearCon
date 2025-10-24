import customtkinter as ctk
from core.channel_manager.manager import ChannelManager
from core.audio.engine import AudioEngine
from adapters.clearcom_station_ic.station_ic_adapter import StationICAdapter
from ui.main_ui import ClearConUI

def main():
    # Set UI theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # Initialize AudioEngine
    audio_engine = AudioEngine()

    # Initialize ChannelManager with 8 channels
    channel_manager = ChannelManager(total_channels=8, audio_engine=audio_engine)

    # Initialize StationIC Adapter (auto-syncs base and beltpacks)
    station_adapter = StationICAdapter(channel_manager=channel_manager)
    station_adapter.connect()

    # Launch UI
    app = ClearConUI(channel_manager=channel_manager, audio_engine=audio_engine, station_adapter=station_adapter)
    app.mainloop()

if __name__ == "__main__":
    main()
