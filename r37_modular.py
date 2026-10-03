#!/usr/bin/env python3
"""
Módulo modular complementar para a prova de conceito R37.

Objetivo:
- preservar o estado original do repositório
- adicionar uma camada moderna de validação e organização
- manter o conceito sem apagar o material histórico
"""

from __future__ import annotations

import gzip
import hashlib
import io
import time
import zlib
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Tuple


DEFAULT_DOMAINS: Dict[str, Dict[str, int]] = {
    'medico': {
        'paciente': 437,
        'relata': 94,
        'dor': 256,
        'temporal': 112,
        'com': 67,
        'bruxismo': 189,
        'ao': 45,
        'acordar': 156,
        'apresenta': 201,
        'estalido': 234,
        'conduta': 89,
        'placa': 234,
        'superior': 145,
        'retorno': 178,
        'trinta': 156,
        'dias': 112,
        'desgaste': 178,
        'incisal': 145,
        'compativel': 267,
        'sono': 134,
        'abertura': 189,
        'bucal': 123,
        'sensibilidade': 289,
        'muscular': 234,
        'palpacao': 267,
    }
}


@dataclass
class R37Hibridismo:
    dominio: str = 'medico'
    chave_secreta: bytes = b'sounavy-gaia-ip-2026'
    dicionarios: Dict[str, Dict[str, int]] = field(default_factory=lambda: DEFAULT_DOMAINS)
    dict_atual: Dict[str, int] = field(init=False)

    def __post_init__(self) -> None:
        self.dict_atual = self.dicionarios.get(self.dominio, self.dicionarios['medico'])

    def quebrar_hmac_em_vetores(self, mensagem: str) -> dict:
        hmac = hashlib.sha256(self.chave_secreta + mensagem.encode('utf-8')).digest()
        v1 = int.from_bytes(hmac[0:4], 'big') % 256
        v2 = int.from_bytes(hmac[4:8], 'big') % 256
        v3 = int.from_bytes(hmac[8:12], 'big') % 256
        v4 = int.from_bytes(hmac[12:16], 'big') % 100
        return {
            'hmac_hex': hmac.hex(),
            'v1_coeficiente': v1,
            'v2_direcao': v2,
            'v3_distancia': v3,
            'v4_semantica': v4,
        }

    def gerar_fatores(self, mensagem: str) -> Tuple[Tuple[int, int, int, int, int], bytes, str]:
        palavras = mensagem.split()
        if not palavras:
            raise ValueError('Mensagem vazia não pode gerar fatores R37.')

        num_palavras = len(palavras)
        primeira_palavra = palavras[0]
        f1 = self.dict_atual.get(primeira_palavra.lower(), 0) % 256
        f2 = num_palavras % 256
        comprimento_total = sum(len(p) for p in palavras)
        f3 = (comprimento_total // num_palavras) % 256

        vetores = self.quebrar_hmac_em_vetores(mensagem)
        f4 = (vetores['v2_direcao'] % num_palavras) % 256
        f5 = vetores['v4_semantica'] % 256

        return (f1, f2, f3, f4, f5), mensagem.encode('utf-8'), vetores['hmac_hex']

    def comprimir_r37(self, mensagem: str) -> Tuple[bytes, int, str]:
        fatores, dados_originais, hmac_hex = self.gerar_fatores(mensagem)
        fatores_bytes = bytes(fatores)
        return fatores_bytes, len(dados_originais), hmac_hex

    def descomprimir_r37_simulado(self, fatores_bytes: bytes, hmac_original: str) -> dict:
        if len(fatores_bytes) < 5:
            raise ValueError('Fatores insuficientes para reconstrução simulada.')
        f1, f2, f3, f4, f5 = fatores_bytes[:5]
        return {
            'fator1_palavra_inicial': f'Palavra começando com coeff {f1}',
            'fator2_num_palavras': f'{f2} palavras',
            'fator3_comprimento_medio': f'~{f3} caracteres cada',
            'fator4_direcao': f'Posição relativa {f4}',
            'fator5_semantica': f'Contexto tipo {f5}',
            'hmac_para_validacao': hmac_original,
        }


def comparar_algoritmos(casos_teste: Iterable[str]) -> List[dict]:
    resultados: List[dict] = []
    for i, caso in enumerate(casos_teste, 1):
        tamanho_original = len(caso.encode('utf-8'))
        r37 = R37Hibridismo('medico')
        fatores_bytes, _, hmac_hex = r37.comprimir_r37(caso)
        tamanho_r37 = len(fatores_bytes)

        comprimido_zip = zlib.compress(caso.encode('utf-8'))
        tamanho_zip = len(comprimido_zip)

        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode='wb') as arquivo:
            arquivo.write(caso.encode('utf-8'))
        tamanho_gzip = len(buffer.getvalue())

        resultados.append({
            'caso': i,
            'original': tamanho_original,
            'r37': tamanho_r37,
            'zip': tamanho_zip,
            'gzip': tamanho_gzip,
            'taxa_r37': (1 - tamanho_r37 / tamanho_original) * 100,
            'taxa_zip': (1 - tamanho_zip / tamanho_original) * 100,
            'taxa_gzip': (1 - tamanho_gzip / tamanho_original) * 100,
            'hmac_hex': hmac_hex,
        })
    return resultados


def benchmark_velocidade(caso_teste: str, iteracoes: int = 1000) -> dict:
    r37 = R37Hibridismo('medico')

    inicio = time.time()
    for _ in range(iteracoes):
        r37.comprimir_r37(caso_teste)
    tempo_r37 = time.time() - inicio

    inicio = time.time()
    for _ in range(iteracoes):
        zlib.compress(caso_teste.encode('utf-8'))
    tempo_zip = time.time() - inicio

    inicio = time.time()
    for _ in range(iteracoes):
        buffer = io.BytesIO()
        with gzip.GzipFile(fileobj=buffer, mode='wb') as arquivo:
            arquivo.write(caso_teste.encode('utf-8'))
    tempo_gzip = time.time() - inicio

    return {
        'iteracoes': iteracoes,
        'tempo_r37_ms': tempo_r37 * 1000,
        'tempo_zip_ms': tempo_zip * 1000,
        'tempo_gzip_ms': tempo_gzip * 1000,
        'ganho_vs_zip': tempo_zip / tempo_r37 if tempo_r37 else float('inf'),
        'ganho_vs_gzip': tempo_gzip / tempo_r37 if tempo_r37 else float('inf'),
    }


def main() -> None:
    casos_teste = [
        'paciente relata dor temporal com bruxismo',
        'paciente ao acordar apresenta estalido',
        'conduta placa superior retorno trinta dias',
        'desgaste incisal compativel bruxismo sono',
        'abertura bucal sensibilidade muscular palpacao',
    ]

    resultados = comparar_algoritmos(casos_teste)
    for item in resultados:
        print(item)

    print('\nBenchmark:')
    print(benchmark_velocidade('paciente relata dor temporal com bruxismo ' * 10, iteracoes=500))


if __name__ == '__main__':
    main()
