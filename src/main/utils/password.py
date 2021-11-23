import base64
import bcrypt

def hash_password(password_b64):
    password = base64.decodebytes(password_b64.encode())
    salt = bcrypt.gensalt(rounds=16)
    hash = bcrypt.hashpw(password,salt)
    hash_b64 = base64.encodebytes(hash)
    return hash_b64

def check_password(attempted_password_b64,password_b64):
    attempted_password = base64.decodebytes(attempted_password_b64.encode())
    password = base64.decodebytes(password_b64)

    return bcrypt.checkpw(attempted_password,password)