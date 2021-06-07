import environ
from cryptography.fernet import Fernet


class EncryptionHelper():
    f = None
    def __init__(self):
        env = environ.Env()
        environ.Env.read_env()
        key: bytes = bytes(env('KEY'),'ascii')
        self.f = Fernet(key)

    def encrypt(self,data:bytes):
        stringBytes = bytes(data,'UTF-8')
        encr = self.f.encrypt(stringBytes)
        return encr
    
    def decrypt(self,data:bytes):        
        return self.f.decrypt(data).decode('UTF-8')