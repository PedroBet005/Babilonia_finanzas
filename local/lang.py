from local import es, en

LANGUAGES = {
    "es": es,
    "en": en
}

_current = es   # idioma por defecto

def set_language(code):
    global _current
    _current = LANGUAGES.get(code, es)

def t(key):
    return _current.t(key)
