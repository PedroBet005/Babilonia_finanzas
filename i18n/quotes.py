import random

BABYLON_QUOTES = [
    "El oro huye de quien no tiene propósito.",
    "Guarda una parte de todo lo que ganes.",
    "El oro trabaja diligentemente para el sabio.",
]

def get_random_quote() -> str:
    return random.choice(BABYLON_QUOTES)
