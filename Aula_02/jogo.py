import os
import random
import time

TAMANHO = 8


def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def renderizar_tabuleiro(posicao):

    tabuleiro = [[" " for _ in range(TAMANHO)] for _ in range(TAMANHO)]

    # Objetivo
    for linha, coluna in posicao["objetivo"]:
        tabuleiro[linha][coluna] = "O"

    # Jogador
    linha, coluna = posicao["jogador"]
    tabuleiro[linha][coluna] = "A"

    # Barreiras
    for linha, coluna in posicao["barreiras"]:
        tabuleiro[linha][coluna] = "X"

    # Cabeçalho
    print("    " + "   ".join(str(i) for i in range(TAMANHO)))

    # Tabuleiro
    for i, linha in enumerate(tabuleiro):
        print("  +" + "---+" * TAMANHO)

        print(f"{i} |", end="")

        for celula in linha:
            print(f" {celula} |", end="")

        print()

    print("  +" + "---+" * TAMANHO)


def geraldao_de_barreiras():
    num_barreiras = random.randint(10, 20)
    barreiras = set()

    while len(barreiras) < num_barreiras:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)
        if (
            (linha, coluna) not in barreiras
            and (linha, coluna) != (1, 1)
            and (linha, coluna) != (0, 0)
        ):
            barreiras.add((linha, coluna))

    return list(barreiras)


def geraldao_de_objetivo(posicao):
    while True:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)
        if (linha, coluna) != (1, 1) and (linha, coluna) not in posicao["barreiras"]:
            return [(linha, coluna)]


def geraldao_posicao_inicial(posicao):
    while True:
        linha = random.randint(0, TAMANHO - 1)
        coluna = random.randint(0, TAMANHO - 1)

        safe_area = set()
        for i in range(-2, 2):
            safe_linha = posicao["objetivo"][0][0] + i
            for j in range(-2, 2):
                safe_coluna = posicao["objetivo"][0][1] + j
                safe_area.add((safe_linha, safe_coluna))
        if (
            (linha, coluna) != (1, 1)
            and (linha, coluna) not in posicao["barreiras"]
            and (linha, coluna) not in posicao["objetivo"]
            and (linha, coluna) not in safe_area
        ):
            return (linha, coluna)


def calcular_distancia_objetivo(posicao):
    linha_jogador, coluna_jogador = posicao["jogador"]
    linha_objetivo, coluna_objetivo = posicao["objetivo"][0]

    distancia = abs(linha_jogador - linha_objetivo) + abs(
        coluna_jogador - coluna_objetivo
    )
    return distancia


def walk(posicao, posicoes_testadas):
    movimentos = [
        (posicao["jogador"][0] - 1, posicao["jogador"][1]),  # cima
        (posicao["jogador"][0] + 1, posicao["jogador"][1]),  # baixo
        (posicao["jogador"][0], posicao["jogador"][1] - 1),  # esquerda
        (posicao["jogador"][0], posicao["jogador"][1] + 1),  # direita
    ]

    movimentos_validos = [
        movimento
        for movimento in movimentos
        if (
            0 <= movimento[0] < TAMANHO
            and 0 <= movimento[1] < TAMANHO
            and movimento not in posicao["barreiras"]
        )
    ]

    if not movimentos_validos:
        return posicao["jogador"]

    menor_distancia = float("inf")
    melhor_movimento = posicao["jogador"]

    for movimento in movimentos_validos:
        nova_posicao = {"jogador": movimento, "objetivo": posicao["objetivo"]}
        distancia = calcular_distancia_objetivo(nova_posicao)

        if distancia < menor_distancia and movimento not in posicoes_testadas:
            menor_distancia = distancia
            melhor_movimento = movimento

    posicoes_testadas.add(melhor_movimento)
    return melhor_movimento


def main():
    print("Bem-vindo ao jogo!")

    posicao = {"objetivo": [(0, 0)], "jogador": (1, 1), "barreiras": [(2, 2), (3, 3)]}

    posicao["barreiras"] = geraldao_de_barreiras()
    posicao["objetivo"] = geraldao_de_objetivo(posicao)
    posicao["jogador"] = geraldao_posicao_inicial(posicao)

    posicoes_testadas = set()
    posicao["jogador"] = walk(posicao, posicoes_testadas)

    while posicao["jogador"] != posicao["objetivo"][0]:
        posicao["jogador"] = walk(posicao, posicoes_testadas)
        limpar_terminal()
        renderizar_tabuleiro(posicao)
        time.sleep(1)


if __name__ == "__main__":
    main()
