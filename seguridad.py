from cryptography.fernet import Fernet
import os

ARCHIVO_CLAVE = "clave.key"


def obtener_clave():
    if not os.path.exists(ARCHIVO_CLAVE):
        clave = Fernet.generate_key()
        with open(ARCHIVO_CLAVE, "wb") as f:
            f.write(clave)
    else:
        with open(ARCHIVO_CLAVE, "rb") as f:
            clave = f.read()
    return clave


def cifrar(texto):
    fernet = Fernet(obtener_clave())
    return fernet.encrypt(texto.encode())


def descifrar(texto_cifrado):
    fernet = Fernet(obtener_clave())
    return fernet.decrypt(texto_cifrado).decode()
