from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


class ECDHKeyExchange:
    def __init__(self):
        self.private_key = x25519.X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        
    def get_public_key_bytes(self) -> bytes:
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw)
    def derive_shared_key(self,peer_public_key_bytes: bytes) -> bytes:
        if len(peer_public_key_bytes) != 32:
            raise ValueError("Chave pública do peer deve ter exatamente 32 bytes (X25519)")
        
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_key_bytes)
        
        shared_secret = self.private_key.exchange(peer_public_key)
        
        hkdf = HKDF(algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,
                    info=b"sovereingc2-v1-session-key")
        return hkdf.derive(shared_secret)