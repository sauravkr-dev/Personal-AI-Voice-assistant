from gtts import gTTS
import os

os.makedirs("assets", exist_ok=True)

audio_files = {
    "yes.mp3": "Yes",
    "hi.mp3": "Hi, how can I Help you?",
    "hello.mp3": "Hello, how can I Help you?",
    "hey.mp3": "Hey, how can I Help you?",
    "good_morning.mp3": "Good morning, how can I Help you?",
    "good_afternoon.mp3": "Good afternoon, how can I Help you?",
    "good_evening.mp3": "Good evening, how can I Help you?",
    "namaste.mp3": "Namaste, how can I Help you?",
    "namaskar.mp3": "Namaskar, how can I Help you?",
    "how_are_you.mp3": "I am good, what about you?",
    "whats_up.mp3": "I am good, what about you?"
}

for file_name, text in audio_files.items():
    path = os.path.join("audios", file_name)

    if not os.path.exists(path):
        print(f"Creating {file_name}...")
        gTTS(text=text, lang="en").save(path)
    else:
        print(f"{file_name} already exists.")

print("All audio files created successfully!")