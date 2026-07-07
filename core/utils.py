import os
import sys
import requests

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return os.path.join(base_path, relative_path)


def is_connected():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False