import speech_recognition as sr
import webbrowser
import requests
import musiclibrary
import sys
from gtts import gTTS
from google import genai
import pygame
import os
import time
import uuid
from websites import websites
from greetings import greetings
import random
import pyautogui
import msvcrt
from languages import languages
from deep_translator import GoogleTranslator

current_language = "en-IN"
wake_words = ["nova", "nov", "innova"]
ai_access = False
minimized = False


def translate_to_english(text):
    try:
        return GoogleTranslator(
            source="auto",
            target="en"
        ).translate(text)
    except:
        return text

def aiProcess(command):

    client = genai.Client(api_key=gemini_api)

    response = client.models.generate_content(
        model="gemini-2.5-flash",

        config={
        "system_instruction": """
You are Nova, a personal AI assistant created by Saurav Kumar.
Never reveal that you are Gemini or Google.
Always introduce yourself as Nova.
"""
    },
        contents=command
    )

    return response.text


recognizer = sr.Recognizer()

def is_connected():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

with open(resource_path("gemini_api.txt"), "r") as f:
    gemini_api = f.read().strip()

with open(resource_path("news_api.txt"), "r") as f:
    news_api = f.read().strip()

pygame.mixer.init()
pygame.mixer.init()

def speak(text):
    filename = f"{uuid.uuid4()}.mp3"

    if current_language != "en-IN":
        text = GoogleTranslator(
            source="en",
            target=current_language.split("-")[0]
        ).translate(text)

    tts = gTTS(
        text=text,
        lang=current_language.split("-")[0]
    )

    tts.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    time.sleep(0.1)

    if os.path.exists(filename):
        os.remove(filename)

def play_audio(filename):
    pygame.mixer.music.load(resource_path(filename))
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    time.sleep(0.05)

def processCommand(c):
    global active, ai_access, minimized, current_language
    #print("processCommand:", repr(c))
    print(f"Command: {c}")

    if "language" in c.lower():
        for name, code in languages.items():
            if name in c.lower():
                current_language = code
                print(f"Language changed to {name.title()}.")
                speak(f"Language changed to {name}.")
                return

    if "open" in c.lower():

        search_query = c.lower().replace("open", "").strip()
        site = search_query.replace(" ", "").replace(".com", "").replace(".in", "").strip()
        if site in websites:
            url = websites[site]
        else:
            url = f"https://www.{site}.com"

        webbrowser.open(url)
        print(f"Opening {search_query}.")
        speak(f"Opening {search_query}.")

    elif "search" in c.lower():
        if not is_connected():
            print("No internet connection.")
            speak("No internet connection.")
            return
        search_query = c.lower().replace("search", "").strip()
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        print(f"Searching for {search_query} on Google.")
        speak(f"Searching for {search_query} on Google.")

    elif any(x in c.lower() for x in ["music","some music", "play anything"]):

        name, url = random.choice(list(musiclibrary.music.items()))

        webbrowser.open(url)
        print(f"Playing {name}")
        speak(f"Playing {name}")
        
    elif "play" in c.lower():
        if not is_connected():
            print("No internet connection.")
            speak("No internet connection.")
            return
        song = c.lower().replace("play", "").strip()

        for name, url in musiclibrary.music.items():
            if name in song:
                webbrowser.open(url)
                print(f"Playing {name}")
                speak(f"Playing {name}")
                return
        webbrowser.open(f"https://open.spotify.com/search/{song.replace(' ', '%20')}")
        print(f"searching {song} on spotify")
        speak(f"searching {song} on spotify")


    elif "news" in c.lower():
        if not is_connected():
            print("No internet connection.")
            speak("No internet connection.")
            return
        response = requests.get(
            f"https://newsapi.org/v2/everything?q=india&language=en&sortBy=publishedAt&apiKey={news_api}",
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()
            articles = data.get("articles", [])

            if not articles:
                print("No news found.")
                speak("No news found.")
                return
            i = 0
            print("Press 'q' to stop the news...")
            speak("Press 'q' to stop the news...")
            print("Here are today's top headlines.")
            speak("Here are today's top headlines.")
            while i < len(articles):

                #listen 5 news
                for _ in range(5):
                    key = ""
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode(errors="ignore").lower()

                        if key == "q":

                            print("Stopping news...")
                            speak("Stopping news")
                            break

                    if i >= len(articles):
                        break

                    print(f"{i+1}. {articles[i]['title']}")
                    speak(articles[i]["title"])
                    i += 1

                # After all news finished
                if i >= len(articles):
                    print("That's all for today's news.")
                    speak("That's all for today's news.")
                    break

                if key == "q":
                    break
                # Continue or not
                print("Do you want me to continue? Please say yes or no.")
                speak("Do you want me to continue? Please say yes or no.")

                try:
                    with sr.Microphone() as source:
                        print("Listening...")
                        audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)

                    reply = recognizer.recognize_google(audio).lower()
                    print("Reply:", reply)

                    # Continue
                    if any(x in reply for x in ["yes", "continue", "go on", "sure", "ofcourse"]):
                        continue

                    # Stop news
                    elif any(x in reply for x in ["no", "stop"]):
                        print("Okay, stopping the news.")
                        speak("Okay, stopping the news.")
                        break

                    # deactivate Nova
                    elif any(x in reply for x in ["deactivate yourself", "go to sleep", "deactivate nova", "sleep nova", "nova sleep", "nova deactivate"]):
                        print("Deactivating Nova...")
                        speak("Deactivating Nova...")
                        active = False
                        return

                    else:
                        print("I will stop the news.")
                        speak("I will stop the news.")
                        break

                except sr.WaitTimeoutError:
                    print("No response received. Stopping the news.")
                    speak("No response received. Stopping the news.")
                    break

                except sr.UnknownValueError:
                    print("I didn't understand. Stopping the news.")
                    speak("I didn't understand. Stopping the news.")
                    break
    if "desktop" in c.lower() and any(x in c.lower() for x in [
    "refresh",
    "reload"
]):
        print("Refreshing desktop.")
        speak("Refreshing desktop.")
        time.sleep(0.5)
        minimized = True
        pyautogui.hotkey("win", "d")   
        time.sleep(0.8)
        pyautogui.press("f5")

    elif any(x in c.lower() for x in [
    "refresh",
    "reload",
]):
        print("Refreshing.")
        speak("Refreshing.")
        time.sleep(0.5)
        pyautogui.press("f5")

    elif any(x in c.lower() for x in [
    "show desktop",
    "go to desktop",
    "desktop mode",
    "minimize all windows",
    "minimize windows",
    "minimise all windows",
    "minimise windows"
]):
        if minimized:
            print("Desktop is already showing.")
            speak("Desktop is already showing.")
        else:
            print("Showing desktop.")
            speak("Showing desktop.")
            time.sleep(0.5)
            pyautogui.hotkey("win", "d")
            minimized = True

    elif( 
    any(word in c.lower() for word in ["window", "windows"])
    and
    any(x in c.lower() for x in [
        "restore",
        "show",
        "bring back"
    ])
):
        if minimized:
            print("Restoring all windows.")
            speak("Restoring all windows.")
            time.sleep(0.5)
            pyautogui.hotkey("win", "d")
            minimized = False
        else:
            print("Windows are already open.")
            speak("Windows are already open.")

    elif any(x in c.lower() for x in [
    "close window",
    "close current window",
    "close this window",
    "close the window"
]):
        print("Closing current window.")
        speak("Closing current window.")
        time.sleep(0.5)      #To complete TTS
        pyautogui.hotkey("alt", "f4")

    elif "close" in c.lower() and any(x in c.lower() for x in [
    "all windows",
    "everything",
    "apps",
    "applications"
    ]):
        print("Are you sure you want to close all windows?")
        speak("Are you sure you want to close all windows?")

        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

        reply = recognizer.recognize_google(audio).lower()
        print(f"Heard: {reply}")

        if any(x in reply for x in ["yes", "sure", "go on", "ofcourse"]):
            print("Closing all windows.")
            speak("Closing all windows.")
            for _ in range(20):
                pyautogui.hotkey("alt", "f4")
                time.sleep(0.5)
        elif any(x in reply for x in ["no", "stop"]):
            print("Cancelled.")
            speak("Cancelled.")


    elif any(x in c.lower() for x in [
    "shutdown the pc",
    "shutdown pc",
    "shutdown computer",
    "turn off the pc",
    "power off",
    "turn off the computer",
    "turn off my pc",
    "turn off my computer",
    ]):
        print("Your computer will shut down in 10 seconds.")
        speak("Your computer will shut down in 10 seconds.")
        os.system("shutdown /s /t 10")

    elif any (x in c.lower() for x in [
        "restart the pc", "restart pc", "restart computer", 
        "reboot the pc", 
        "reboot pc", 
        "reboot computer"
        "restart the computer",
        "reboot the computer",
        "restart my pc",
        "restart my computer"
        ]):
        print("Your computer will restart in 10 seconds.")
        speak("Your computer will restart in 10 seconds.")
        os.system("shutdown /r /t 10")
        
    elif any(x in c.lower() for x in [
        "cancel shutdown",
        "cancel restart",
        "abort shutdown",
        "abort restart",
        "stop shutdown",
        "stop restart",
        "cancel the shutdown",
        "cancel the restart",
        "abort the shutdown",
        "abort the restart"
        ]):
        result = os.system("shutdown /a")

        if result == 0:
            print("Shutdown or restart cancelled.")
            speak("Shutdown or restart cancelled.")
        else:
            print("No shutdown or restart was scheduled.")
            speak("No shutdown or restart was scheduled.")
        

    elif any(x in c.lower() for x in ["ai access", "enable ai", "enable ai access", "enable ai mode", "ai mode"]):
        ai_access = True
        print("AI access enabled.")
        speak("AI access enabled.")

    elif any(x in c.lower() for x in ["disable ai", "disable ai access", "disable ai mode"]):
        ai_access = False
        print("AI access disabled.")
        speak("AI access disabled.")

    elif any(word in c.lower() for word in ["goodbye", "disable", "shutdown", "shutdown yourself", "disable yourself", "close yourself"]):
        print("Disabling Nova...")
        speak("Disabling Nova...")
        sys.exit()
        #let gemini handle the command if ai_access is enabled
    else:
        if ai_access:
            if not is_connected():
                print("No internet connection.")
                speak("No internet connection.")
                return
            response = aiProcess(c)
            print(response)
            speak(response)

print("=" * 41)
print("      NOVA AI VOICE ASSISTANT")
print("=" * 41)
print("Status    : Running")
print("Wake Word : Nova")
print("Ready to receive voice commands...")
print("=" * 41)
print()
    

if __name__ == "__main__":
    print("Initializing Nova...")
    speak("Initializing Nova...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 1.2
        recognizer.non_speaking_duration = 0.6
    active = False
    while True:
        #Listen for the wake word "Nova"
        #obtain audio from the microphone
        print("Processing...")
        try:
            with sr.Microphone() as source:
                if active:
                    print("Listening...")
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=7)
                else:
                    print("Listening for wake word...")
                    audio = recognizer.listen(source, timeout=None, phrase_time_limit=8)

            text = recognizer.recognize_google(
                audio,
                language=current_language
            ).lower()

            print(f"Heard: {text}")

            original_text = text

            if current_language != "en-IN":
                text = translate_to_english(text).lower()

            print("Original:", original_text)
            print("Command :", text)

            if not active:
                if any(word in text for word in wake_words):
                    active = True
                    command = text
                    for word in wake_words:
                        command = command.replace(word, "").strip()

                    #command = (command.replace("hey", "").strip())

                    if command in greetings:
                        play_audio(greetings[command])
                    elif command:
                        processCommand(command)
                    else:
                        play_audio(greetings[command])

                continue

             # -------- Active Mode --------

            if text in greetings:
                play_audio(greetings[text])
                continue

            if any(word in text for word in wake_words):
                command = text
                for word in wake_words:
                    command = command.replace(word, "").strip()
                #command = command.replace("hey", "").strip()

                
                if command in greetings:
                    play_audio(greetings[command])

                elif command in ["deactivate yourself", "go to sleep", "deactivate", "sleep",]:
                    active = False
                    print("Deactivating Nova...")
                    speak("Deactivating Nova...")
                    continue
                elif command:
                    processCommand(command)   
                else:
                    play_audio(greetings[command])                
                continue

            if text in ["deactivate yourself", "go to sleep", "deactivate", "sleep",]:
                active = False
                print("Deactivating Nova...")
                speak("Deactivating Nova...")
                continue

            processCommand(text)

        except sr.UnknownValueError:
            continue

        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")
            
