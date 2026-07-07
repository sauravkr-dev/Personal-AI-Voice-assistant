import speech_recognition as sr
import pygame

from core.utils import resource_path
import core.config as config

config.current_language = "en-IN"

wake_words = ["nova", "nov", "innova"]


def initialize():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 1
    recognizer.energy_threshold = 300

    with open(resource_path("news_api.txt"), "r") as f:
        news_api = f.read().strip()

    pygame.mixer.init()

    print("=" * 41)
    print("      NOVA AI VOICE ASSISTANT")
    print("=" * 41)
    print("Status    : Running")
    print("Wake Word : hey Nova, hello Nova, hi Nova")
    print("Ready to receive voice commands...")
    print("=" * 41)
    print()

    return recognizer, news_api