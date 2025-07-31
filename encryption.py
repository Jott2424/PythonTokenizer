import base64
import hashlib
from Crypto.Cipher import AES

BLOCK_SIZE = 16

def _pad(s):
    pad_len = BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE
    return s + chr(pad_len) * pad_len

def _unpad(s):
    pad_len = ord(s[-1])
    return s[:-pad_len]

def derive_key_iv(key_str):
    key = hashlib.sha256(key_str.encode()).digest()
    iv = hashlib.md5(key).digest()  # Deterministic IV derived from key
    return key, iv

def encrypt_data(data, key_str):
    key, iv = derive_key_iv(key_str)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = _pad(data)
    encrypted = cipher.encrypt(padded_data.encode())
    return base64.b64encode(encrypted).decode()

def decrypt_data(enc_data, key_str):
    key, iv = derive_key_iv(key_str)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(base64.b64decode(enc_data))
    return _unpad(decrypted.decode())

def batch_encrypt_data(data_list, key_str):
    return [encrypt_data(item, key_str) for item in data_list]

def batch_decrypt_data(enc_list, key_str):
    return [decrypt_data(item, key_str) for item in enc_list]
