import socket
from typing import Optional
from crypto.secure_channel import SecureChannel

class Connection:
    def __init__(self, config):
        self.config = config
        self.socket: Optional[socket.socket] = None
        self.secure_channel: SecureChannel = SecureChannel()
        self.connected: bool = False
        self.agent_id: Optional[str] = config.get("agent_id")
        
    def connect(self) -> bool:
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.config.get("server_host"), self.config.get("server_port")))
            
            print(f"[+] conectado ao servidor {self.config.get("server_host")}:{self.config.get("servewr_port")}")
            
            print("[*] Iniciando o handshake criptográfico")
            my_pub_key = self.secure_channel.initiate_handshake()
            
            self.socket.sendall(my_pub_key)
            print("[*] Chave publica enviada ao servidor")
            
            server_pub_key = self.socket.recv(32)
            if len(server_pub_key) != 32:
                raise ValueError(f"Chave pública inválida recebida: {len(server_pub_key)} bytes")
            
            self.secure_channel.complete_handshake(server_pub_key)
            print("[*] Handshake criptográfico concluído com sucesso!")
            print("[*] Canal seguro (AES-256-CGM) estabelecido")
            
            self.connected = True
            return True
        except Exception as e:
            print(f"[-] Erro na conexão/handshake: {e}")
            if self.socket:
                self.socket.close()
            return False

    def send(self, data: bytes) -> bool:
        if not self.connected or not self.secure_channel.is_ready():
            print("[-] Canal inseguro")
            return False
        
        if self.socket is None:
            print("[-] Socket não inicializado")
            return False
        
        try:
            encrypted = self.secure_channel.encrypt(data)
            length = len(encrypted).to_bytes(4, byteorder='big')
            self.socket.sendall(length + encrypted)
            return True
        except Exception as e:
            print(f"[-] Erro ao enviar dados: {e}")
            self.connected = False
            return False
        
    def receive(self) -> Optional[bytes]:
        if not self.secure_channel.is_ready() or not self.connected:
            return None
        
        try:
            if not self.socket == None: 
                length_bytes = self.socket.recv(4)
                if not length_bytes:
                    return None
            
                length = int.from_bytes(length_bytes, byteorder='big')
                if length > 65536:
                    raise ValueError("pacote grande")
                
                encrypted = b""
                while len(encrypted) < length:
                    data = length - len(encrypted)
                    chunk = self.socket.recv(data)
                    if not chunk:
                        return None
                    encrypted += chunk
                    
                decrypted = self.secure_channel.decrypt(encrypted)
                return decrypted
        
        except Exception as e:
            print(f"[-] Erro ao receber dados: {e}")
            self.connected = False
            return None
        
    
                
