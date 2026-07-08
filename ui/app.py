import customtkinter as ctk
from core.task_manager import cancel
import pygame
from core.utils import resource_path
from PIL import Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NovaApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.iconbitmap(resource_path("assets/NovaAI.ico"))

        self.title("Nova AI Voice Assistant")
        self.geometry("900x600")
        # ================= Header =================

        self.logo_img = ctk.CTkImage(
            light_image=Image.open(resource_path("assets/logo-light.png")),
            dark_image=Image.open(resource_path("assets/logo-dark.png")),
            size=(42, 42)
        )

        self.header = ctk.CTkFrame(self, fg_color="transparent")
        self.header.pack(fill="x", padx=15, pady=(15, 5))

        self.logo = ctk.CTkLabel(
            self.header,
            image=self.logo_img,
            text=""
        )
        self.logo.pack(side="left")

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Nova AI",
            font=("Segoe UI", 26, "bold")
        )
        self.title_label.pack(side="left", padx=12)
        self.minsize(800, 500)

        self.chat = ctk.CTkTextbox(
            self,
            font=("Segoe UI", 15),
            corner_radius=12
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(5, 15)
        )

        self.bottom = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom.pack(fill="x", padx=15, pady=(0,15))

        self.status = ctk.CTkLabel(
            self.bottom,
            text="🎤 Ready",
            font=("Segoe UI", 15)
        )
        self.status.pack(side="left")

        self.stop_button = ctk.CTkButton(
            self.bottom,
            text="⏹ Stop",
            width=110,
            command=self.stop_all
        )
        self.stop_button.pack(side="right")


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