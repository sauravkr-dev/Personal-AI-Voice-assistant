wake_words = ["nova", "nov", "innova"]


def contains_wake_word(text):
    text = text.lower()
    return any(word in text for word in wake_words)


def remove_wake_word(text):
    text = text.lower()

    for word in wake_words:
        text = text.replace(word, "").strip()

    return text