from gtts import gTTS
from deep_translator import GoogleTranslator
import pygame
import uuid
import os
import time
import core.config as config
from ui.chat import add_nova_message
from core.task_manager import is_cancelled, reset

def speak(text, translate=True):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    print("Speak Language:", config.current_language)
    # print("Before Translation:", text)
    filename = f"{uuid.uuid4()}.mp3"

    if translate and config.current_language != "en-IN":
        text = GoogleTranslator(
            source="en",
            target=config.current_language.split("-")[0]
        ).translate(text)
    # print("After Translation:", text)
    print("Response:", text)
    add_nova_message(text)
    tts = gTTS(
        text=text,
        lang=config.current_language.split("-")[0]
    )

    tts.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        if is_cancelled():

            pygame.mixer.music.stop()
            reset()
            return

        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.music.unload()

    time.sleep(0.1)

    if os.path.exists(filename):
        os.remove(filename)

def translate_to_english(text):
    try:
        return GoogleTranslator(
            source="auto",  
            target="en"
        ).translate(text)
    except:
        return text