# Arquitetura do R37

Este documento adiciona uma visão estruturada da proposta R37 sem alterar o conteúdo original do repositório.

## 1) Conceito central

A ideia do R37 é tratar a mensagem como um padrão estruturado, em vez de como um fluxo bruto de bytes. Em vez de enviar o texto completo, transmite-se um conjunto compacto de fatores que captura o comportamento esperado da estrutura da frase.

## 2) Componentes do modelo

### 2.1 Dicionário fixo

O domínio médico usa um conjunto de palavras-chave e pesos associados. Esse dicionário é mantido em código, reduzindo a necessidade de transmitir contexto completo por rede.

### 2.2 HMAC

O HMAC atua como camada de autenticação. A mensagem é convertida em um valor derivado da chave secreta, e esse valor é usado para validar integridade sem que a mensagem inteira tenha que ser encaminhada novamente.

### 2.3 Vetores de derivação

Os bytes do HMAC são convertidos em vetores para gerar indicadores de:
- coeficiente
- direção
- distância
- semântica
- contexto relativo

### 2.4 Fatores compactados

Os fatores gerados representam uma compactação estrutural, não apenas uma compressão matemática linear. O objetivo é resumir o padrão sem perder a capacidade de reconstrução contextual.

## 3) Fluxo de processamento

1. Recebe a mensagem original
2. Normaliza palavras e domínio
3. Extrai fatores principais
4. Gera HMAC
5. Cria signature compacta
6. Valida integridade
7. Reconstrói ideia contextualmente

## 4) Vantagens da abordagem

- menor payload
- validação por autenticação
- contextualização por domínio
- melhor reutilização de informações esperadas
- separação clara entre compressão e autenticação

## 5) Limitação metodológica

Este é um protótipo conceitual. Ele não substitui uma arquitetura operacional completa de produção, mas funciona como um framework de prova de conceito para explorar compressão contextual e autenticação estrutural.

## 6) Preservação do histórico

A implementação original foi mantida intacta. Esta documentação representa uma camada adicional de entendimento para facilitar manutenção, revisão e integração sem alterar o material publicado.
