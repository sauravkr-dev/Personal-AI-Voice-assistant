import core.config as config


def add_user_message(text):
    if config.app:
        config.app.add_message("You", text)


def add_nova_message(text):
    if config.app:
        config.app.add_message("Nova", text)


def set_status(text):
    if config.app:
        config.app.set_status(text)