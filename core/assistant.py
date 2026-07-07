import speech_recognition as sr
from core.listener import listen
from core.wakeword import contains_wake_word, remove_wake_word
from core.active_mode import handle_active_mode
from core.voice import speak
from core.task_manager import reset, is_cancelled


def run(recognizer):
    ai_access = False
    minimized = False
    active = False

    print("Initializing Nova...")
    speak("Initializing Nova...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
        recognizer.pause_threshold = 1.2
        recognizer.non_speaking_duration = 0.6

    while True:

        if is_cancelled():
            reset()
            active = True
            continue
        print("Processing...")

        try:
            text = listen(recognizer, active)

            print(f"Heard: {text}")
            print("Command :", text)

            if contains_wake_word(text):
                text = remove_wake_word(text)
                active = True

            if not active:
                continue

            active, ai_access, minimized, handled = handle_active_mode(
                text,
                active,
                recognizer,
                ai_access,
                minimized
            )

            if handled:
                continue

        except sr.UnknownValueError:
            continue

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")