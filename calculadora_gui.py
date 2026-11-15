"""Calculadora de operacoes basicas com interface grafica em Tkinter."""

import re
import tkinter as tk
from decimal import Decimal, localcontext
from typing import Optional

FUNDO = "#071A33"
PAINEL = "#0D2B50"
BOTAO = "#164477"
BOTAO_HOVER = "#2465A8"
AZUL_DESTAQUE = "#2787D8"
TEXTO = "#F2F7FF"
TEXTO_SUAVE = "#AFC5E3"
OPERADORES = "+-*/"
HISTORICO_MAXIMO = 10

_NUMERO = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)"
_EXPRESSAO_COMPLETA = re.compile(
    r"^\s*(" + _NUMERO + r")\s*([+\-*/])\s*(" + _NUMERO + r")\s*$"
)


def formatar_resultado(valor: Decimal) -> str:
    """Converte um Decimal para texto sem zeros decimais desnecessarios."""
    if valor == 0:
        return "0"

    resultado = format(valor, "f")
    if "." in resultado:
        resultado = resultado.rstrip("0").rstrip(".")
    return resultado


def calcular(expressao: str) -> Decimal:
    """Calcula uma expressao com dois operandos e um operador basico."""
    correspondencia = _EXPRESSAO_COMPLETA.fullmatch(expressao)
    if correspondencia is None:
        raise ValueError("Digite dois numeros e um operador valido.")

    primeiro_texto, operador, segundo_texto = correspondencia.groups()
    primeiro = Decimal(primeiro_texto)
    segundo = Decimal(segundo_texto)
    if not primeiro.is_finite() or not segundo.is_finite():
        raise ValueError("Use apenas numeros finitos.")

    if operador == "/" and segundo == 0:
        raise ZeroDivisionError("Nao e possivel dividir por zero.")

    with localcontext() as contexto:
        contexto.prec = 28
        if operador == "+":
            return primeiro + segundo
        if operador == "-":
            return primeiro - segundo
        if operador == "*":
            return primeiro * segundo
        return primeiro / segundo


def _pontos_retangulo_arredondado(largura: int, altura: int):
    raio = 14
    return [
        raio, 0,
        largura - raio, 0,
        largura, 0,
        largura, raio,
        largura, altura - raio,
        largura, altura,
        largura - raio, altura,
        raio, altura,
        0, altura,
        0, altura - raio,
        0, raio,
        0, 0,
    ]


def _desenhar_retangulo_arredondado(
    canvas: tk.Canvas, largura: int, altura: int, cor: str
) -> int:
    """Desenha um fundo arredondado no Canvas e retorna seu identificador."""
    return canvas.create_polygon(
        _pontos_retangulo_arredondado(largura, altura),
        smooth=True,
        splinesteps=16,
        fill=cor,
        outline="",
    )


class BotaoArredondado(tk.Canvas):
    """Botao desenhado em Canvas para manter cantos arredondados no Tkinter."""

    def __init__(
        self,
        parent: tk.Widget,
        texto: str,
        comando,
        cor: str = BOTAO,
        cor_hover: str = BOTAO_HOVER,
        **opcoes,
    ) -> None:
        super().__init__(
            parent,
            width=opcoes.pop("width", 72),
            height=opcoes.pop("height", 54),
            bg=PAINEL,
            highlightthickness=0,
            **opcoes,
        )
        self._cor = cor
        self._cor_hover = cor_hover
        self._comando = comando
        self._fundo = _desenhar_retangulo_arredondado(
            self, 72, 54, self._cor
        )
        self._texto = self.create_text(
            36,
            27,
            text=texto,
            fill=TEXTO,
            font=("Segoe UI", 13, "bold"),
        )
        self.bind("<Button-1>", self._ao_clicar)
        self.bind("<Enter>", self._ao_entrar)
        self.bind("<Leave>", self._ao_sair)
        self.bind("<Configure>", self._ao_redimensionar)
        self.configure(cursor="hand2")

    def _ao_clicar(self, _evento) -> None:
        self._comando()

    def _ao_entrar(self, _evento) -> None:
        self.itemconfigure(self._fundo, fill=self._cor_hover)

    def _ao_sair(self, _evento) -> None:
        self.itemconfigure(self._fundo, fill=self._cor)

    def _ao_redimensionar(self, evento) -> None:
        if evento.width < 2 or evento.height < 2:
            return
        self.coords(
            self._fundo,
            *_pontos_retangulo_arredondado(evento.width, evento.height),
        )
        self.coords(self._texto, evento.width / 2, evento.height / 2)


class CalculadoraGUI:
    """Mantem o estado da calculadora e conecta os botoes a interface."""

    def __init__(self, janela: tk.Tk) -> None:
        self.janela = janela
        self.janela.title("Calculadora Azul")
        self.janela.configure(bg=FUNDO)
        self.janela.resizable(False, False)

        self.expressao = ""
        self.calculo_concluido = False
        self.entrada_com_erro = False
        self.historico = []
        self.expressao_var = tk.StringVar()
        self.resultado_var = tk.StringVar()

        self.criar_layout()
        self.atualizar_display()

    def criar_layout(self) -> None:
        """Monta o display, teclado e lista de historico."""
        container = tk.Frame(self.janela, bg=FUNDO, padx=18, pady=18)
        container.pack(fill="both", expand=True)

        tk.Label(
            container,
            text="CALCULADORA",
            bg=FUNDO,
            fg=TEXTO,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        display = tk.Frame(container, bg=PAINEL, padx=14, pady=12)
        display.pack(fill="x", pady=(0, 14))
        tk.Label(
            display,
            textvariable=self.expressao_var,
            bg=PAINEL,
            fg=TEXTO_SUAVE,
            anchor="e",
            font=("Segoe UI", 14),
            height=1,
        ).pack(fill="x")
        tk.Label(
            display,
            textvariable=self.resultado_var,
            bg=PAINEL,
            fg=TEXTO,
            anchor="e",
            font=("Segoe UI", 25, "bold"),
            height=1,
        ).pack(fill="x", pady=(4, 0))

        teclado = tk.Frame(container, bg=PAINEL)
        teclado.pack(fill="x", pady=(0, 16))
        botoes = (
            ("C", 0, 0, 1, AZUL_DESTAQUE),
            ("\u2190", 0, 1, 1, BOTAO),
            ("/", 0, 2, 1, BOTAO),
            ("*", 0, 3, 1, BOTAO),
            ("7", 1, 0, 1, BOTAO),
            ("8", 1, 1, 1, BOTAO),
            ("9", 1, 2, 1, BOTAO),
            ("-", 1, 3, 1, BOTAO),
            ("4", 2, 0, 1, BOTAO),
            ("5", 2, 1, 1, BOTAO),
            ("6", 2, 2, 1, BOTAO),
            ("+", 2, 3, 1, BOTAO),
            ("1", 3, 0, 1, BOTAO),
            ("2", 3, 1, 1, BOTAO),
            ("3", 3, 2, 1, BOTAO),
            (".", 3, 3, 1, BOTAO),
            ("0", 4, 0, 3, BOTAO),
            ("=", 4, 3, 1, AZUL_DESTAQUE),
        )

        for texto, linha, coluna, largura, cor in botoes:
            botao = BotaoArredondado(
                teclado,
                texto,
                lambda valor=texto: self.tratar_entrada(valor),
                cor=cor,
                cor_hover=BOTAO_HOVER,
            )
            botao.grid(
                row=linha,
                column=coluna,
                columnspan=largura,
                padx=4,
                pady=4,
                sticky="nsew",
            )

        for coluna in range(4):
            teclado.grid_columnconfigure(coluna, weight=1, uniform="coluna")

        cabecalho_historico = tk.Frame(container, bg=FUNDO)
        cabecalho_historico.pack(fill="x")
        tk.Label(
            cabecalho_historico,
            text="Historico recente",
            bg=FUNDO,
            fg=TEXTO,
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left")
        tk.Label(
            cabecalho_historico,
            text="C limpa tudo",
            bg=FUNDO,
            fg=TEXTO_SUAVE,
            font=("Segoe UI", 9),
        ).pack(side="right")

        self.lista_historico = tk.Listbox(
            container,
            height=6,
            bg=PAINEL,
            fg=TEXTO_SUAVE,
            selectbackground=BOTAO,
            selectforeground=TEXTO,
            relief="flat",
            highlightthickness=0,
            font=("Segoe UI", 10),
            activestyle="none",
        )
        self.lista_historico.pack(fill="both", expand=True, pady=(7, 0))

    def atualizar_display(self, valor: Optional[str] = None) -> None:
        """Atualiza a equacao e mostra uma previa quando ela estiver completa."""
        if valor is not None:
            self.expressao = valor
        self.expressao_var.set(self.expressao)

        if self.calculo_concluido or not self.expressao:
            self.resultado_var.set("")
            return

        try:
            resultado = calcular(self.expressao)
        except ZeroDivisionError:
            self.resultado_var.set("Divisao por zero")
        except ValueError:
            self.resultado_var.set("")
        else:
            self.resultado_var.set(formatar_resultado(resultado))

    def tratar_entrada(self, valor: str) -> None:
        """Direciona cada tecla para a acao apropriada."""
        if valor == "C":
            self.limpar()
        elif valor == "\u2190":
            self.apagar_ultimo()
        elif valor == "=":
            self.igual()
        elif valor in OPERADORES:
            self.digitar_operador(valor)
        elif valor == ".":
            self.digitar_decimal()
        elif valor.isdigit():
            self.digitar_numero(valor)

    def digitar_numero(self, digito: str) -> None:
        if self.calculo_concluido or self.entrada_com_erro:
            self.expressao = ""
        self.calculo_concluido = False
        self.entrada_com_erro = False

        numero_atual = re.search(r"[+-]?\d+(?:\.\d*)?$", self.expressao)
        if numero_atual and numero_atual.group() in ("0", "-0"):
            inicio = numero_atual.start()
            sinal = "-" if numero_atual.group().startswith("-") else ""
            self.expressao = self.expressao[:inicio] + sinal + digito
        else:
            self.expressao += digito
        self.atualizar_display()

    def digitar_decimal(self) -> None:
        if self.calculo_concluido or self.entrada_com_erro:
            self.expressao = ""
        self.calculo_concluido = False
        self.entrada_com_erro = False

        if not self.expressao or self.expressao[-1] in OPERADORES:
            self.expressao += "0."
        else:
            numero_atual = re.search(r"[+-]?\d+(?:\.\d*)?$", self.expressao)
            if numero_atual and "." not in numero_atual.group():
                self.expressao += "."
            elif not numero_atual:
                self.expressao += "0."
        self.atualizar_display()

    def digitar_operador(self, operador: str) -> None:
        if self.entrada_com_erro:
            return
        self.calculo_concluido = False

        if self.expressao and _EXPRESSAO_COMPLETA.fullmatch(self.expressao):
            try:
                resultado = formatar_resultado(calcular(self.expressao))
            except (ValueError, ZeroDivisionError) as erro:
                self.tratar_erro(str(erro))
                return
            self.expressao = resultado + operador
        elif not self.expressao:
            if operador == "-":
                self.expressao = "-"
            else:
                return
        elif self.expressao[-1] in OPERADORES:
            if operador == "-" and self.expressao[-1] != "-":
                self.expressao += operador
            elif (
                self.expressao[-1] == "-"
                and len(self.expressao) > 1
                and self.expressao[-2] in OPERADORES
            ):
                self.expressao = self.expressao[:-2] + operador
            else:
                self.expressao = self.expressao[:-1] + operador
        else:
            self.expressao += operador

        self.atualizar_display()

    def igual(self) -> None:
        if not self.expressao or self.entrada_com_erro:
            return

        expressao_calculada = self.expressao
        try:
            resultado = formatar_resultado(calcular(expressao_calculada))
        except (ValueError, ZeroDivisionError) as erro:
            self.tratar_erro(str(erro))
            return

        self.adicionar_ao_historico(expressao_calculada, resultado)
        self.expressao = resultado
        self.calculo_concluido = True
        self.entrada_com_erro = False
        self.atualizar_display()

    def tratar_erro(self, mensagem: str) -> None:
        """Apresenta o erro no display e aguarda uma nova entrada."""
        self.resultado_var.set("Erro: {}".format(mensagem))
        self.entrada_com_erro = True

    def adicionar_ao_historico(self, expressao: str, resultado: str) -> None:
        """Insere calculos recentes no topo e limita o historico a dez itens."""
        item = "{} = {}".format(expressao, resultado)
        self.historico.insert(0, item)
        del self.historico[HISTORICO_MAXIMO:]
        self.lista_historico.delete(0, tk.END)
        for calculo in self.historico:
            self.lista_historico.insert(tk.END, calculo)

    def apagar_ultimo(self) -> None:
        if self.entrada_com_erro:
            self.expressao = ""
        elif self.expressao:
            self.expressao = self.expressao[:-1]
        self.calculo_concluido = False
        self.entrada_com_erro = False
        self.atualizar_display()

    def limpar(self) -> None:
        self.expressao = ""
        self.calculo_concluido = False
        self.entrada_com_erro = False
        self.historico.clear()
        self.lista_historico.delete(0, tk.END)
        self.atualizar_display()


def main() -> None:
    """Inicia a interface grafica."""
    janela = tk.Tk()
    CalculadoraGUI(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
