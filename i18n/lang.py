# lang.py
from typing import Dict

from .es import MESSAGES as ES
from .en import MESSAGES as EN


# ==========================================================
# Language registry
# ==========================================================

LANGUAGES: Dict[str, Dict[str, str]] = {
    "es": ES,
    "en": EN,
}

DEFAULT_LANG = "es"
_current_lang: Dict[str, str] = LANGUAGES[DEFAULT_LANG]


# ==========================================================
# Public API
# ==========================================================

def set_language(lang: str) -> None:
    """
    Set current language.
    If language is not supported, fallback to default.
    """
    global _current_lang
    _current_lang = LANGUAGES.get(lang, LANGUAGES[DEFAULT_LANG])


def get_language() -> str:
    """
    Returns current language code.
    """
    for code, messages in LANGUAGES.items():
        if messages is _current_lang:
            return code
    return DEFAULT_LANG


def t(key: str) -> str:
    """
    Translate a key using current language.
    Falls back to key if translation does not exist.
    """
    return _current_lang.get(key, key)

