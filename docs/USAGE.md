# Guia de uso

Este guia acrescenta uma camada de uso e execução sem tocar nos arquivos originais do projeto.

## Requisitos

Python 3.10 ou superior.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execução do módulo modular

```bash
python r37_modular.py
```

## Execução de testes

```bash
python -m unittest tests_r37.py
```

## Exemplo de uso em código

```python
from r37_modular import R37Hibridismo

r37 = R37Hibridismo(dominio='medico')
msg = 'paciente relata dor temporal com bruxismo'
fatores, payload_len, hmac_hex = r37.comprimir_r37(msg)
print(fatores)
print(payload_len)
print(hmac_hex)
```

## Observação importante

Este é um módulo novo e complementar. O conteúdo original do projeto permanecendo intacto foi preservado e não foi mesclado ao histórico original.
