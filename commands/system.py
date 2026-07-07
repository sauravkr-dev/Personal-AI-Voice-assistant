import os
import time
import pyautogui
import speech_recognition as sr
from core.voice import speak

def handle_system(command, recognizer, minimized):
    if "desktop" in command.lower() and any(x in command.lower() for x in [
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
        return True, minimized

    elif any(x in command.lower() for x in [
    "refresh",
    "reload",
]):
        print("Refreshing.")
        speak("Refreshing.")
        time.sleep(0.5)
        pyautogui.press("f5")
        return True, minimized

    elif any(x in command.lower() for x in [
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
        return True, minimized
    
    elif( 
    any(word in command.lower() for word in ["window", "windows"])
    and
    any(x in command.lower() for x in [
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
        return True, minimized
    
    elif any(x in command.lower() for x in [
    "close window",
    "close current window",
    "close this window",
    "close the window"
]):
        print("Closing current window.")
        speak("Closing current window.")
        time.sleep(0.5)      #To complete TTS
        pyautogui.hotkey("alt", "f4")
        return True, minimized

    elif "close" in command.lower() and any(x in command.lower() for x in [
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


    elif any(x in command.lower() for x in [
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
        return True, minimized

    elif any (x in command.lower() for x in [
        "restart the pc", "restart pc", "restart computer", 
        "reboot the pc", 
        "reboot pc", 
        "reboot computer",
        "restart the computer",
        "reboot the computer",
        "restart my pc",
        "restart my computer"
        ]):
        print("Your computer will restart in 10 seconds.")
        speak("Your computer will restart in 10 seconds.")
        os.system("shutdown /r /t 10")
        return True, minimized
    
    elif any(x in command.lower() for x in [
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
    return False, minimized
