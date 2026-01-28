# i18n.py
from local import es
from local import en


LANGUAGES = {
    "es": es.MESSAGES,
    "en": en.MESSAGES
}

current_lang = "es"  # Idioma por defecto


def set_language(lang_code):
    """
    Establece el idioma actual.
    Si el idioma no existe, usa español como fallback.
    """
    global current_lang
    if lang_code in LANGUAGES:
        current_lang = lang_code
    else:
        current_lang = "es"


def t(message_key):
    """
    Devuelve el texto traducido según el idioma actual.
    Fallback:
      1. Idioma actual
      2. Español
      3. La clave (debug seguro)
    """
    # Idioma actual
    if message_key in LANGUAGES.get(current_lang, {}):
        return LANGUAGES[current_lang][message_key]

    # Fallback a español
    if message_key in LANGUAGES["es"]:
        return LANGUAGES["es"][message_key]

    # Último recurso: devolver la clave
    return message_key

