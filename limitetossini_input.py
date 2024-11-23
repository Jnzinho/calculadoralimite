# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from sympy import Symbol, limit, S, sympify

def analisar_limite(funcao, nome_var, ponto_aprox, epsilon=1e-6):
    """
    Analisa o limite de uma função quando se aproxima de um ponto por ambos os lados.
    """
    x = Symbol(nome_var)

    try:
        # Calcula o limite geral
        limite_principal = limit(funcao, x, ponto_aprox)

        # Calcula limites laterais
        limite_esquerda = limit(funcao, x, ponto_aprox, dir='-')
        limite_direita = limit(funcao, x, ponto_aprox, dir='+')

        # Ajusta o intervalo de plotagem baseado no ponto de aproximação
        if ponto_aprox in [float('inf'), float('-inf')]:
            if ponto_aprox == float('inf'):
                valores_x = np.linspace(0, 100, 1000)  # Plota de 0 a 100 para infinito
            else:
                valores_x = np.linspace(-100, 0, 1000)  # Plota de -100 a 0 para -infinito
        else:
            valores_x = np.linspace(float(ponto_aprox) - 2, float(ponto_aprox) + 2, 1000)
            valores_x = valores_x[valores_x != ponto_aprox]  # Remove o ponto de aproximação

        # Converte expressão sympy para função compatível com numpy
        f_numpy = lambda x: float(funcao.subs({Symbol(nome_var): x}).evalf())
        
        # Calcula valores y com tratamento de erro
        valores_y = []
        for xi in valores_x:
            try:
                yi = f_numpy(xi)
                if -1000 < yi < 1000:  # Filtra valores muito grandes/pequenos
                    valores_y.append(yi)
                else:
                    valores_y.append(None)
            except:
                valores_y.append(None)

        # Remove None values
        valores_x = valores_x[np.array(valores_y) != None]
        valores_y = np.array(valores_y)[np.array(valores_y) != None]

        # Criação do gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(valores_x, valores_y, 'b-', label='Função')
        
        if ponto_aprox not in [float('inf'), float('-inf')]:
            plt.axvline(x=ponto_aprox, color='r', linestyle='--', label=f'x = {ponto_aprox}')

        if limite_principal != S.Infinity and limite_principal != -S.Infinity:
            plt.axhline(y=float(limite_principal), color='g', linestyle='--', label=f'Limite = {limite_principal}')

        plt.grid(True)
        plt.legend()
        if ponto_aprox == float('inf'):
            plt.title(f'Análise do Limite quando {nome_var} → ∞')
        elif ponto_aprox == float('-inf'):
            plt.title(f'Análise do Limite quando {nome_var} → -∞')
        else:
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

def main():
    print("Calculadora de Limites")
    print("---------------------")
    print("Funções disponíveis: sin(x), cos(x), tan(x), exp(x), log(x), sqrt(x)")
    print("Exemplo de entrada: x**2 + 2*x + 1")
    print("Para infinito, digite: inf ou -inf")
    
    try:
        # Recebe a função do usuário
        funcao_str = input("\nDigite a função (em termos de x): ")
        
        # Converte a string da função para expressão sympy
        x = Symbol('x')
        funcao = sympify(funcao_str)
        
        # Recebe o ponto de aproximação
        ponto_str = input("Digite o ponto de aproximação: ")
        if ponto_str.lower() == 'inf':
            ponto_aprox = float('inf')
        elif ponto_str.lower() == '-inf':
            ponto_aprox = float('-inf')
        else:
            ponto_aprox = float(ponto_str)
        
        # Analisa o limite
        resultado = analisar_limite(funcao, 'x', ponto_aprox)
        
        if resultado:
            print("\nResultados:")
            print(f"Limite principal: {resultado['limite_principal']}")
            print(f"Limite pela esquerda: {resultado['limite_esquerda']}")
            print(f"Limite pela direita: {resultado['limite_direita']}")
            print(f"O limite existe? {'Sim' if resultado['limite_existe'] else 'Não'}")
            
            plt.show()
            
            # Pergunta se quer calcular outro limite
            if input("\nDeseja calcular outro limite? (s/n): ").lower() == 's':
                main()
    
    except Exception as e:
        print(f"\nErro: {str(e)}")
        if input("\nDeseja tentar novamente? (s/n): ").lower() == 's':
            main()

if __name__ == "__main__":
    main()