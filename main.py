from core.channel_manager.manager import ChannelManager
from core.audio.engine import AudioEngine
from ui.main_ui import ClearConUI

if __name__ == "__main__":
    manager = ChannelManager(total_channels=8)
    audio = AudioEngine()

    app = ClearConUI(manager, audio)
    app.mainloop()
