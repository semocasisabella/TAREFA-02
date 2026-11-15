# Calculadora Azul

Calculadora grafica de operacoes basicas, feita em Python com Tkinter. A
interface usa tons de azul, botoes arredondados, pre-visualizacao do resultado
e historico dos calculos recentes.

## Requisitos

- Python 3.8 ou superior.
- Tkinter, normalmente incluido nas instalacoes padrao do Python.
- Nenhuma dependencia de terceiros.

## Como executar

Abra um terminal nesta pasta e execute:

```powershell
python calculadora_gui.py
```

## Como usar

- Digite numeros pelos botoes e escolha `+`, `-`, `*` ou `/`.
- Use `.` para numeros decimais.
- O display mostra a equacao na primeira linha e a previa do resultado abaixo.
- Pressione `=` para concluir o calculo; o display passa a mostrar somente o
  resultado.
- Use `←` para apagar o ultimo caractere.
- Use `C` para limpar o display e todo o historico.
- O historico mostra os dez calculos mais recentes.

Divisao por zero e expressoes invalidas sao informadas diretamente no display.
Os calculos usam `Decimal` para preservar a precisao decimal nos resultados.

## Testes

Execute os testes sem abrir a interface:

```powershell
python -m unittest -v
```

Os testes verificam as quatro operacoes, decimais, operandos negativos,
formatacao, entradas invalidas e divisao por zero.

## Estrutura

- `calculadora_gui.py`: interface Tkinter, estado da calculadora e operacoes.
- `test_calculadora_gui.py`: testes automatizados da funcao de calculo.
- `docs/COPILOT.md`: registro e orientacoes de uso do GitHub Copilot.

## Uso do GitHub Copilot

O GitHub Copilot foi usado como assistente para organizar os requisitos,
implementar a interface e a logica da calculadora, e preparar testes e
documentacao. As sugestoes devem ser revisadas e validadas com os testes antes
de serem integradas. Consulte [docs/COPILOT.md](docs/COPILOT.md).

## Publicar no GitHub

Crie um repositorio publico vazio no GitHub e, nesta pasta, configure o remoto:

```powershell
git init
git add calculadora_gui.py
git commit -m "Adiciona interface grafica da calculadora"
git add test_calculadora_gui.py
git commit -m "Adiciona testes das operacoes"
git add docs/COPILOT.md
git commit -m "Documenta o uso do GitHub Copilot"
git add README.md
git commit -m "Documenta instalacao e uso"
git add .gitignore
git commit -m "Ignora arquivos gerados localmente"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/calculadora-azul.git
git push -u origin main
```

Troque `SEU_USUARIO` pelo usuario correto e autentique-se no GitHub. Os cinco
commits listados separam mudancas relacionadas; mantenha cada commit coerente
com o conteudo que ele introduz.
