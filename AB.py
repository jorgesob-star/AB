# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def comparar_descontos():
    """
    Compara duas opções de despesas com base no apuro líquido.
    """
    try:
        # 1. Entradas do Usuário
        print("💸 Comparador de Descontos")
        print("-" * 30)
        
        apuro_total = float(input("💰 Apuro total (€): "))
        desc_combustivel = float(input("⛽ Desconto de Combustível (€): "))
        
        apuro_liquido = apuro_total - desc_combustivel
        print(f"\nApuro Líquido: {apuro_liquido:.2f} €\n")

        # 2. Opção 1
        print("--- Opção 1 ---")
        aluguer = float(input("🏠 Aluguer (€): "))
        perc_aluguer = float(input("👔 Percentual (%): "))
        
        # 3. Opção 2
        print("\n--- Opção 2 ---")
        seguro = float(input("🛡️ Seguro (€): "))
        manutencao = float(input("🛠️ Manutenção (€): "))
        perc_seguro = float(input("👔 Percentual (%): "))

        # 4. Cálculos
        sobra_opcao1 = apuro_liquido - (apuro_liquido * perc_aluguer / 100) - aluguer
        sobra_opcao2 = apuro_liquido - (apuro_liquido * perc_seguro / 100) - seguro - manutencao

        # 5. Exibir Resultados
        print("\n" + "=" * 30)
        print("🌟 Resultados da Comparação")
        print("=" * 30)
        print(f"📈 Opção 1: Sobram {sobra_opcao1:.2f} €")
        print(f"📈 Opção 2: Sobram {sobra_opcao2:.2f} €")
        print("-" * 30)

        # 6. Mensagem de Conclusão
        if sobra_opcao1 > sobra_opcao2:
            diferenca = sobra_opcao1 - sobra_opcao2
            print(f"🎉 A Opção 1 é a melhor escolha, com uma diferença de {diferenca:.2f} €.")
        elif sobra_opcao2 > sobra_opcao1:
            diferenca = sobra_opcao2 - sobra_opcao1
            print(f"🎉 A Opção 2 é a melhor escolha, com uma diferença de {diferenca:.2f} €.")
        else:
            print("As duas opções resultam no mesmo valor.")
            
        # 7. Gerar Gráfico
        labels = ['Opção 1', 'Opção 2']
        valores = [sobra_opcao1, sobra_opcao2]
        cores = ['#2196F3', '#2196F3']
        
        if sobra_opcao1 > sobra_opcao2:
            cores[0] = '#4CAF50' # Verde para a melhor opção
        elif sobra_opcao2 > sobra_opcao1:
            cores[1] = '#4CAF50'
            
        plt.figure(figsize=(8, 6))
        plt.bar(labels, valores, color=cores)
        plt.ylabel('€ Restantes')
        plt.title('Comparação entre Opções')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Adicionar os valores nas barras
        for i, v in enumerate(valores):
            plt.text(i, v + 1, f"{v:.2f} €", ha='center')
            
        plt.show()

    except ValueError:
        print("\nErro: Por favor, insira apenas valores numéricos.")

# Executa o programa
comparar_descontos()
