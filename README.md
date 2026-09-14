# Dashboard de leads do site AVVA

Relatório visual dos leads do formulário do site da AVVA (26/06 a 13/09/2026), com foco em setembro.

**Uso interno. O `index.html` contém nome, telefone e e-mail dos leads: manter este repositório privado.**

## Abrir

Abra `index.html` no navegador. Os dados já estão embutidos no arquivo.

## O que tem

- Ranking de prioridade (nota de 0 a 100, faixas A, B, C e D) com botão de WhatsApp
- Radar de proximidade até a AVVA (Rua Felipe Schmidt, 869, Centro, Florianópolis)
- Seção dos leads sem endereço, com região provável pelo DDD e mensagem pronta pedindo o bairro
- Leads por plano, receita potencial, ritmo de cadastros, faixa etária e gênero estimado
- Qualidade dos dados do formulário e tabela completa

## Como a nota é calculada

| Critério | Pontos |
|---|---|
| Proximidade | até 35 |
| Plano (Uno 30, Duo 24, Trio 16, Essencial 6) | até 30 |
| Recência (setembro 20, agosto 10, julho 4, junho 2) | até 20 |
| Idade | até 10 |
| Contato válido | até 5 |
| Reenviou o formulário | +3 |

Faixas: A a partir de 70, B a partir de 55, C a partir de 40, D abaixo disso.

## Atualizar com uma planilha nova

Requer Python 3 com `pandas` e `openpyxl`.

1. Em `src/process.py`, aponte `SRC` para a planilha exportada.
2. `cd src && python3 process.py && python3 build.py`

A planilha (`*.xlsx`) e o `data.json` intermediário ficam fora do repositório.
