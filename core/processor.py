from commands.language import handle_language
from commands.browser import handle_browser
from commands.music import handle_music
from commands.system import handle_system
from commands.ai_mode import handle_ai_mode
from commands.exit import handle_exit
from commands.ai_command import handle_ai
from core.news import read_news

def process_command(command, recognizer, ai_access, minimized):

    if handle_language(command):
        return ai_access, minimized

    if handle_browser(command):
        return ai_access, minimized

    if handle_music(command):
        return ai_access, minimized

    if "news" in command.lower():
        read_news(recognizer)
        return ai_access, minimized

    handled, minimized = handle_system(command, recognizer, minimized)

    if handled:
        return ai_access, minimized

    handled, ai_access = handle_ai_mode(command,ai_access)

    if handled:
        return ai_access, minimized

    if handle_exit(command):
        return ai_access, minimized

    handle_ai(command, ai_access)

    return ai_access, minimized
