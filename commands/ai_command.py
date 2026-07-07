from core.voice import speak
from core.ai_service import aiProcess
from core.utils import is_connected

def handle_ai(command, ai_access):
    if ai_access:
                if not is_connected():
                    print("No internet connection.")
                    speak("No internet connection.")
                    return
                response = aiProcess(command)
                print(response)
                speak(response)