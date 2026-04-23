from .key_exchange import ECDHKeyExchange
from .aes_gcm import AESGCMHandler
import os
import json
from typing import Optional, Tuple

class SecureChannel:
    def __init__(self):
        self.key_exchange: Optional[ECDHKeyExchange] = None
        self.crypto_handler: Optional[AESGCMHandler] = None
        self.is_handshaked = False
        
    def initiate_handshake(self) -> bytes:
        self.key_exchange = ECDHKeyExchange()
        self.is_handshaked = False
        return self.key_exchange.get_public_key_bytes()
    
    def complete_handshake(self, peer_public_key: bytes) -> None:
        if self.key_exchange is None:
            self.key_exchange = ECDHKeyExchange()
            
        shared_key = self.key_exchange.derive_shared_key(peer_public_key)
        self.crypto_handler = AESGCMHandler(shared_key)
        self.is_handshaked = True
        
        self.key_exchage = None
        
    def encrypt(self, data:bytes) -> bytes:
        if not self.is_handshaked or self.crypto_handler is None:
            raise RuntimeError("Handshake não foi completado. Chame complete_handshake() primeiro")
        return self.crypto_handler.encrypt(data)
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        if not self.is_handshaked or self.crypto_handler is None:
            raise RuntimeError("Handshake não foi completado. Chame complete_handshake() primeiro")
        return self.crypto_handler.decrypt(encrypted_data)
    
    def is_ready(self) -> bool:
        return self.is_handshaked and self.crypto_handler is not None
    
def create_test_secure_channel_pair():
    agent = SecureChannel()
    server = SecureChannel()
    
    agent_pub = agent.initiate_handshake()
    server_pub = server.initiate_handshake()
    
    agent.complete_handshake(server_pub)
    server.complete_handshake(agent_pub)
    return agent, server

