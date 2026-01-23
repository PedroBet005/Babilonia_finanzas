# i18n.py
from local import es
from local import en


LANGUAGES = {
    "es": es.MESSAGES,
    "en": en.MESSAGES
}


current_lang = "es"  # Por defecto español

def set_language(lang_code):
    global current_lang
    if lang_code in LANGUAGES:
        current_lang = lang_code
    else:
        current_lang = "es"


def t(message_key):
    """Función para obtener el mensaje traducido"""
    return LANGUAGES[current_lang].get(message_key, message_key)
