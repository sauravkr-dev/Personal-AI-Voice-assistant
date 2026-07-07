from data import musiclibrary
from core.voice import speak
import random
import webbrowser
import core.config as config
from core.utils import is_connected

def handle_music(command):
    if any(x in command.lower() for x in ["music","some music", "play anything", "some song", "play songs", "play a random song"]):

        name, url = random.choice(list(musiclibrary.music.items()))

        webbrowser.open(url)
        print(f"Playing song {name}")

        if config.current_language.startswith("en"):
                speak(f"Playing song {name}")
        else:
            speak("Playing song")
            speak(name, translate=False)
        return True
    
    elif "play" in command.lower():
        if not is_connected():
            print("No internet connection.")
            speak("No internet connection.")
            return
        song = command.lower().replace("play", "").strip()

        for name, url in musiclibrary.music.items():
            if name in song:
                webbrowser.open(url)
                if config.current_language.startswith("en"):
                    speak(f"Playing song {name}")
                else:
                    speak("Playing song")
                    speak(name, translate=False)
                return
        webbrowser.open(f"https://open.spotify.com/search/{song.replace(' ', '%20')}")
        if config.current_language.startswith("en"):
            speak(f"Searching {song} on Spotify")
        else:
            speak("Searching on Spotify")
            speak(song, translate=False)
        return True
    return False
