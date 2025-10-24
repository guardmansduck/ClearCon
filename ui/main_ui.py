import customtkinter as ctk
from config.icons import IconManager
from core.channel_manager.manager import ChannelManager
from core.audio.engine import AudioEngine

class ClearConUI(ctk.CTk):
    def __init__(self, channel_manager: ChannelManager, audio_engine: AudioEngine, station_adapter=None):
        super().__init__()

        self.title("ClearCon Control Panel")
        self.geometry("600x400")
        self.resizable(False, False)

        self.channel_manager = channel_manager
        self.audio_engine = audio_engine
        self.station_adapter = station_adapter
        self.user_id = "local_user"

        self.icons = IconManager(size=(24, 24), color_tint=(255, 255, 255))

        ctk.CTkLabel(self, text="🎧 ClearCon", font=("Arial", 22, "bold")).pack(pady=10)

        # Beltpack frame
        self.beltpack_frame = ctk.CTkFrame(self)
        self.beltpack_frame.pack(pady=5, fill="x", padx=20)
        ctk.CTkLabel(self.beltpack_frame, text="Connected Belpacks:", font=("Arial", 14)).pack(anchor="w")

        self.beltpack_widgets = {}  # user_id -> widget dict

        # Volume sliders
        ctk.CTkLabel(self, text="Volume", font=("Arial", 16)).pack(pady=5)

        # Channel buttons
        self.channel_frame = ctk.CTkFrame(self)
        self.channel_frame.pack(pady=15)
        self.icon_up = self.icons.load("channel_up")
        self.icon_down = self.icons.load("channel_down")
        ctk.CTkButton(self.channel_frame, image=self.icon_up, text="", width=60, command=self.next_channel).grid(row=0, column=0, padx=10)
        ctk.CTkButton(self.channel_frame, image=self.icon_down, text="", width=60, command=self.prev_channel).grid(row=0, column=1, padx=10)

        # Mute button
        self.icon_mute = self.icons.load("mute")
        self.icon_unmute = self.icons.load("unmute")
        self.mute_btn = ctk.CTkButton(self, image=self.icon_mute, text="", width=60, command=self.toggle_mute)
        self.mute_btn.pack(pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Connecting...", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.update_ui_loop()

    def update_ui_loop(self):
        if self.station_adapter:
            for user_id, ch in self.channel_manager.user_channels.items():
                if user_id not in self.beltpack_widgets:
                    frame = ctk.CTkFrame(self.beltpack_frame)
                    frame.pack(anchor="w", pady=2, fill="x")

                    name_label = ctk.CTkLabel(frame, text=user_id, width=100)
                    name_label.pack(side="left")

                    channel_label = ctk.CTkLabel(frame, text=f"Ch: {ch}", width=50)
                    channel_label.pack(side="left", padx=5)

                    led = ctk.CTkLabel(frame, width=12, height=12, corner_radius=6,
                                       fg_color="green" if not self.channel_manager.is_user_muted(user_id) else "red", text="")
                    led.pack(side="left", padx=5)

                    # Audio meter
                    meter = ctk.CTkProgressBar(frame, width=150)
                    meter.set(0)
                    meter.pack(side="left", padx=10)

                    # Volume slider
                    slider = ctk.CTkSlider(frame, from_=0.0, to=1.0, width=100,
                                           command=lambda val, uid=user_id: self.audio_engine.set_user_volume(uid, val))
                    slider.set(0.8)
                    slider.pack(side="left", padx=5)

                    self.beltpack_widgets[user_id] = {"frame": frame, "channel_label": channel_label, "led": led,
                                                      "meter": meter, "volume_slider": slider}
                else:
                    self.beltpack_widgets[user_id]["channel_label"].configure(
                        text=f"Ch: {self.channel_manager.get_user_channel(user_id)}"
                    )
                    self.beltpack_widgets[user_id]["led"].configure(
                        fg_color="green" if not self.channel_manager.is_user_muted(user_id) else "red"
                    )
                    level = self.audio_engine.get_channel_level(user_id)
                    self.beltpack_widgets[user_id]["meter"].set(level)

        self.status_label.configure(text=f"Connected Base: {self.station_adapter.host if self.station_adapter else 'None'}")
        self.after(500, self.update_ui_loop)

    def toggle_mute(self):
        self.channel_manager.toggle_mute(self.user_id)
        muted = self.channel_manager.is_user_muted(self.user_id)
        self.mute_btn.configure(image=self.icon_unmute if muted else self.icon_mute)

    def next_channel(self):
        self.channel_manager.switch_user_to_next_channel(self.user_id)

    def prev_channel(self):
        self.channel_manager.switch_user_to_prev_channel(self.user_id)
