import customtkinter as ctk
from core.task_manager import cancel
import pygame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NovaApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Nova AI Voice Assistant")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.chat = ctk.CTkTextbox(self, font=("Consolas", 14))
        self.chat.pack(fill="both", expand=True, padx=15, pady=15)

        self.status = ctk.CTkLabel(
            self,
            text="Status : Ready",
            font=("Segoe UI", 15)
        )
        self.status.pack(pady=(0, 10))

        # Stop Button
        self.stop_button = ctk.CTkButton(
            self,
            text="⏹ Stop",
            command=self.stop_all
        )
        self.stop_button.pack(pady=(0, 15))

    def add_message(self, sender, message):
        self.chat.insert("end", f"{sender}: {message}\n\n")
        self.chat.see("end")

    def set_status(self, text):
        self.status.configure(text=text)

    def stop_all(self):

        cancel()

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

        self.set_status("🎤 Listening...")