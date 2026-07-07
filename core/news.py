import requests
import speech_recognition as sr
import msvcrt
from core.voice import speak
from core.utils import resource_path, is_connected
from core.task_manager import is_cancelled, reset

recognizer = sr.Recognizer()
    
with open(resource_path("news_api.txt"), "r") as f:
    news_api = f.read().strip()

def read_news(recognizer):
    global active
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
        # print("Press 'q' to stop the news...")
        # speak("Press 'q' to stop the news...")
        print("Here are today's top headlines.")
        speak("Here are today's top headlines.")
        if is_cancelled():
            return
        while i < len(articles):
            if is_cancelled():
                print("Stopping news...")
                reset()
                return

                    #listen 5 news
            for _ in range(5):
                # key = ""
                # if msvcrt.kbhit():
                #     key = msvcrt.getch().decode(errors="ignore").lower()

                #     if key == "q":

                #         print("Stopping news...")
                #         speak("Stopping news")
                #         break
                if is_cancelled():
                    print("News stopped.")
                    reset()
                    return
                if i >= len(articles):
                            break

                print(f"{i+1}. {articles[i]['title']}")
                speak(articles[i]["title"])
                if is_cancelled():
                    print("News stopped.")
                    reset()
                    return
                i += 1

                    # After all news finished
            if i >= len(articles):
                print("That's all for today's news.")
                speak("That's all for today's news.")
                break

            # if key == "q":
            #     break
                    # Continue or not
            if is_cancelled():
                print("News stopped.")
                reset()
                return
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
