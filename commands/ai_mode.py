from core.voice import speak

def handle_ai_mode(command, ai_access):
    if any(x in command.lower() for x in ["ai access", "enable ai", "enable ai access", "enable ai mode", "ai mode"]):
        ai_access = True
        print("AI access enabled.")
        speak("AI access enabled.")
        return True, ai_access
    
    elif any(x in command.lower() for x in ["disable ai", "disable ai access", "disable ai mode"]):
        ai_access = False
        print("AI access disabled.")
        speak("AI access disabled.")
        return True, ai_access
    
    return False, ai_access