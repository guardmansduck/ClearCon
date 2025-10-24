import customtkinter as ctk
from core.channel_manager.manager import ChannelManager
from core.audio.engine import AudioEngine

class ClearConUI(ctk.CTk):
    def __init__(self, channel_manager: ChannelManager, audio_engine: AudioEngine):
        super().__init__()

        self.title("ClearCon Control Panel")
        self.geometry("480x320")
        self.resizable(False, False)

        self.channel_manager = channel_manager
        self.audio_engine = audio_engine
        self.user_id = "local_user"

        self.volume_level = ctk.DoubleVar(value=0.7)

        # ======== Layout ========
        ctk.CTkLabel(self, text="🎧 ClearCon", font=("Arial", 22, "bold")).pack(pady=10)

        self.channel_label = ctk.CTkLabel(self, text=f"Channel: {self.channel_manager.get_user_channel(self.user_id)}", font=("Arial", 18))
        self.channel_label.pack(pady=5)

        self.mute_button = ctk.CTkButton(self, text="Mute", command=self.toggle_mute, width=100)
        self.mute_button.pack(pady=5)

        ctk.CTkLabel(self, text="Volume", font=("Arial", 16)).pack(pady=5)
        self.volume_slider = ctk.CTkSlider(self, from_=0.0, to=1.0, variable=self.volume_level, command=self.set_volume)
        self.volume_slider.pack(padx=20, pady=5, fill="x")

        self.channel_frame = ctk.CTkFrame(self)
        self.channel_frame.pack(pady=15)

        ctk.CTkButton(self.channel_frame, text="⬆️ Up", width=100, command=self.next_channel).grid(row=0, column=0, padx=5)
        ctk.CTkButton(self.channel_frame, text="⬇️ Down", width=100, command=self.prev_channel).grid(row=0, column=1, padx=5)

        self.status_label = ctk.CTkLabel(self, text="Status: Connected", font=("Arial", 12))
        self.status_label.pack(pady=10)

    # ======== Controls ========
    def toggle_mute(self):
        self.channel_manager.toggle_mute(self.user_id)
        muted = self.channel_manager.is_user_muted(self.user_id)
        self.mute_button.configure(text="Unmute" if muted else "Mute")

    def next_channel(self):
        self.channel_manager.switch_user_to_next_channel(self.user_id)
        self.update_channel_display()

    def prev_channel(self):
        self.channel_manager.switch_user_to_prev_channel(self.user_id)
        self.update_channel_display()

    def set_volume(self, value):
        level = float(value)
        print(f"[UI] Volume set to {level:.2f}")

    def update_channel_display(self):
        ch = self.channel_manager.get_user_channel(self.user_id)
        self.channel_label.configure(text=f"Channel: {ch}")
