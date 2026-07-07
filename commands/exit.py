import sys
from core.voice import speak

def handle_exit(command):
    if any(word in command.lower() for word in ["goodbye", "disable nova", "shutdown", "shutdown yourself", "disable yourself", "close yourself"]):
            print("Disabling Nova...")
            speak("Disabling Nova...")
            sys.exit()

    return False