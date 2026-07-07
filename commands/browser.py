import webbrowser
from data.websites import websites
from core.voice import speak
from core.utils import is_connected

def handle_browser(command):
    if "open" in command.lower():
        search_query = command.lower().replace("open", "").strip()
        site = search_query.replace(" ", "").replace(".com", "").replace(".in", "").strip()
        if site in websites:
            url = websites[site]
        else:
            url = f"https://www.{site}.com"

        webbrowser.open(url)
        print(f"Opening {search_query}.")
        speak(f"Opening {search_query}.")
        return True

    
    elif any(x in command.lower() for x in ["search", "find"]):
        if not is_connected():
            print("No internet connection.")
            speak("No internet connection.")
            return True
        if command.lower().startswith("search for "):
            search_query = command[11:]
        elif command.lower().startswith("find for "):
            search_query = command[9:]
        elif command.lower().startswith("find "):
            search_query = command[5:]
        else:
            search_query = command.replace("search","",1).strip()
        
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        print(f"Searching for {search_query} on Google.")
        speak(f"Searching for {search_query} on Google.")
        return True
    return False
