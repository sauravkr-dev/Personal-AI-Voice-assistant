from ui.app import NovaApp
from core.startup import initialize
from core.assistant import run
import core.config as config
import threading

app = NovaApp()

# Availbling GUI to whole app
config.app = app

recognizer, news_api = initialize()

threading.Thread(
    target=run,
    args=(recognizer,),
    daemon=True
).start()

app.mainloop()