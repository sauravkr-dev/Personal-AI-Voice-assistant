from data.languages import languages
from core.voice import speak
import core.config as config

def handle_language(command):
    command = command.lower()

    if "language" not in command:
        return False

    for name, code in languages.items():
        if name in command:
            config.current_language = code
            print(f"Language changed to {name.title()}.")
            speak(f"Language changed to {name}.")
            return True

    return False    