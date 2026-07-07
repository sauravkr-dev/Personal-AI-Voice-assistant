import speech_recognition as sr
from ui.chat import add_user_message, set_status

import core.config as config
from core.voice import translate_to_english

def listen(recognizer, active):
    with sr.Microphone() as source:
        if active:
            print("Listening...")
            set_status("🎤 Listening...")
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)
        else:
            print("Listening for wake word...")
            set_status("👂 Waiting for Wake Word...")
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)

    text = recognizer.recognize_google(
        audio,
        language=config.current_language
    ).lower()

    if config.current_language != "en-IN":
        text = translate_to_english(text).lower()

    add_user_message(text)
    set_status("🤔 Thinking...")
    return text