# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, limit, S, log

def analisar_limite(funcao, nome_var, ponto_aprox, epsilon=1e-6):
    """
    Analisa o limite de uma função quando se aproxima de um ponto por ambos os lados.

    Parâmetros:
    funcao: callable ou expressão sympy - A função a ser analisada
    nome_var: str - O nome da variável (ex: 'x')
    ponto_aprox: float - O ponto de aproximação
    epsilon: float - O tamanho do passo para análise numérica

    Retorna:
    dicionário contendo a análise do limite e gera um gráfico da função
    """
    # Cria variável simbólica e converte a função se necessário
    x = Symbol(nome_var)

    try:
        # Calcula o limite geral
        limite_principal = limit(funcao, x, ponto_aprox)

        # Calcula limites laterais
        limite_esquerda = limit(funcao, x, ponto_aprox, dir='-')
        limite_direita = limit(funcao, x, ponto_aprox, dir='+')

        # Gera pontos para o gráfico
        valores_x = np.linspace(ponto_aprox - 2, ponto_aprox + 2, 1000)
        valores_x = valores_x[valores_x != ponto_aprox]  # Remove o ponto de aproximação

        # Converte expressão sympy para função compatível com numpy
        f_numpy = lambda x: float(funcao.subs({Symbol(nome_var): x}).evalf())
        valores_y = [f_numpy(xi) for xi in valores_x]

        # Criação do gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(valores_x, valores_y, 'b-', label='Função')
        plt.axvline(x=ponto_aprox, color='r', linestyle='--', label=f'x = {ponto_aprox}')

        if limite_principal != S.Infinity and limite_principal != -S.Infinity:
            plt.axhline(y=float(limite_principal), color='g', linestyle='--', label=f'Limite = {limite_principal}')

        plt.grid(True)
        plt.legend()
        plt.title(f'Análise do Limite quando {nome_var} → {ponto_aprox}')
        plt.xlabel(nome_var)
        plt.ylabel('f(' + nome_var + ')')

        # Resultados da análise
        resultados = {
            'limite_principal': limite_principal,
            'limite_esquerda': limite_esquerda,
            'limite_direita': limite_direita,
            'limite_existe': limite_esquerda == limite_direita,
            'ponto_aproximacao': ponto_aprox
        }

        return resultados

    except Exception as e:
        print(f"Erro no cálculo: {str(e)}")
        return None

# Uso
def exemplo_analise():
    x = Symbol('x')
    f1 = log(x/1)
    print("\nAnalisando log(x/1) quando x → 00")
    resultado = analisar_limite(f1, 'x', float('inf'))
    if resultado:
        print(f"Limite pela esquerda: {resultado['limite_esquerda']}")
        print(f"Limite pela direita: {resultado['limite_direita']}")
        print(f"Limite existe: {resultado['limite_existe']}")

    plt.show()

if __name__ == "__main__":
    exemplo_analise()