# Exemplo simples (ver arquivo CLX_SOBERANO_R37_FATORES.py)

from hashlib import sha256

class R37:
    def __init__(self, dicionario_fixo):
        self.dict = dicionario_fixo
    
    def comprimir(self, mensagem):
        # 1. HMAC
        hmac = sha256(b'chave' + mensagem.encode()).digest()
        
        # 2. Vetores
        v1 = int.from_bytes(hmac[0:4], 'big') % 256
        v2 = int.from_bytes(hmac[4:8], 'big') % 256
        v3 = int.from_bytes(hmac[8:12], 'big') % 256
        v4 = int.from_bytes(hmac[12:16], 'big') % 100
        
        # 3. Fatores
        palavras = mensagem.split()
        f1 = self.dict[palavras[0]] % 256
        f2 = len(palavras)
        f3 = sum(len(p) for p in palavras) // f2
        f4 = v2 % f2
        f5 = v4
        
        # 4. Serializa
        return bytes([f1, f2, f3, f4, f5]), hmac
    
    def descomprimir_simulado(self, fatores):
        f1, f2, f3, f4, f5 = fatores
        print(f"Reconstrói com: {f2} palavras, média {f3}B, contexto {f5}")
        # LLM faz a reconstrução real
