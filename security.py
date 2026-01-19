from cryptography.fernet import Fernet
import os

# Archivo donde se almacena la clave de cifrado

KEY_FILE = "clave.key"


def get_key():

#Recupera la clave de cifrado. 
#Si el archivo de clave no existe, crea uno.

    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    else:
        with open(KEY_FILE, "rb") as f:
            key = f.read()
    return key    


def encrypt(text):
#Cifra una cadena de texto utilizando el cifrado simétrico Fernet.

    fernet = Fernet(get_key())
    return fernet.encrypt(text.encode())


def decrypt(encrypted_text):
# Descifra un texto cifrado y lo devuelve como una cadena.

    fernet = Fernet(get_key())
    return fernet.decrypt(encrypted_text).decode()
