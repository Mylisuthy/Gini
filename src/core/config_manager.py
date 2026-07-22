import os
import json
from cryptography.fernet import Fernet
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self.key_file = os.path.join(self.root_dir, 'system.key')
        self.config_file = os.path.join(self.root_dir, '.env_secure')
        
        # Cargar .env tradicional por si existe de antes
        load_dotenv(os.path.join(self.root_dir, '.env'))
        
        self._ensure_key()
        self.cipher = Fernet(self._load_key())

    def _ensure_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)

    def _load_key(self) -> bytes:
        with open(self.key_file, 'rb') as f:
            return f.read()

    def _read_encrypted(self) -> dict:
        if not os.path.exists(self.config_file):
            return {}
        try:
            with open(self.config_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = self.cipher.decrypt(encrypted_data).decode('utf-8')
            return json.loads(decrypted_data)
        except Exception:
            return {}

    def _write_encrypted(self, data: dict):
        encrypted_data = self.cipher.encrypt(json.dumps(data).encode('utf-8'))
        with open(self.config_file, 'wb') as f:
            f.write(encrypted_data)

    def get(self, key: str, default: str = "") -> str:
        # Priorizar el vault encriptado
        secure_data = self._read_encrypted()
        if key in secure_data:
            return secure_data[key]
        # Fallback a variable de entorno estándar
        return os.environ.get(key, default)

    def set(self, key: str, value: str):
        secure_data = self._read_encrypted()
        secure_data[key] = value
        self._write_encrypted(secure_data)
        # Establecer también en el runtime temporalmente
        os.environ[key] = value

config = ConfigManager()
