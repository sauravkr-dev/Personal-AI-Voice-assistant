from data.greetings import greetings
from core.voice import speak
import core.config as config
from core.processor import process_command


def handle_active_mode(text, active, recognizer, ai_access, minimized):

    if text in greetings:
        print("Current Language:", config.current_language)
        speak(greetings[text]["text"])
        print(f"Response: {greetings[text]['text']}")
        return active, ai_access, minimized, True

    if text in [
        "deactivate yourself",
        "go to sleep",
        "deactivate",
        "sleep"
    ]:
        active = False
        print("Deactivating Nova...")
        speak("Deactivating Nova...")
        return active, ai_access, minimized, True

    ai_access, minimized = process_command(
        text,
        recognizer,
        ai_access,
        minimized
    )

    return active, ai_access, minimized, True