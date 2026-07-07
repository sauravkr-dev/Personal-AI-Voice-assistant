_cancel_requested = False


def cancel():
    global _cancel_requested
    _cancel_requested = True


def reset():
    global _cancel_requested
    _cancel_requested = False


def is_cancelled():
    return _cancel_requested