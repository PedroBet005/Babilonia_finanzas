from .es import MESSAGES as ES
from .en import MESSAGES as EN

_current_lang = ES

def set_language(lang: str):
    global _current_lang
    if lang == "en":
        _current_lang = EN
    else:
        _current_lang = ES

def t(key):
    return _current_lang.get(key, key)
