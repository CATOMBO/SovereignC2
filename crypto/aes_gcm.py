from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

class AESGCMHandler:
    def __init__(self, key: bytes):
        if len(key) != 32:
            raise ValueError("A chave deve ter exatamente 32 bytes para AES-256")
        self.aescgm = AESGCM(key)
        
    def encrypt(self, plaintext: bytes) -> bytes:
        nonce = os.urandom(12)
        ciphertext = self.aescgm.encrypt(nonce, plaintext, None)
        return nonce + ciphertext
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        if len(encrypted_data) < 12 + 16:
            raise ValueError("Dados criptografados invélidos ou muito curtos")
        
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        return self.aescgm.decrypt(nonce,ciphertext, None)