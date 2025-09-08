import json
import os
from datetime import datetime

class GerenciadorDespesas:
    def __init__(self, arquivo_dados="despesas.json"):
        self.arquivo_dados = arquivo_dados
        self.despesas = self.carregar_dados()
        
        # Inicializar categorias se não existirem
        if not self.despesas:
            self.inicializar_categorias()
    
    def inicializar_categorias(self):
        """Inicializa as categorias de despesas com valores zerados"""
        self.despesas = {
            "mensais": [
                {"nome": "Casa", "valor": 0.0},
                {"nome": "Água", "valor": 0.0},
                {"nome": "Luz", "valor": 0.0},
                {"nome": "Telemóveis", "valor": 0.0},
                {"nome": "Atelier", "valor": 0.0},
                {"nome": "Feira", "valor": 0.0},
                {"nome": "Catarina", "valor": 0.0},
                {"nome": "Ginásticas", "valor": 0.0},
                {"nome": "Segurança Social", "valor": 0.0},
                {"nome": "Extras Mensais", "valor": 0.0}
            ],
            "trimestrais": [
                {"nome": "Contabilista", "valor": 0.0},
                {"nome": "Extras Trimestrais", "valor": 0.0}
            ],
            "anuais": [
                {"nome": "Seguro", "valor": 0.0},
                {"nome": "IUC", "valor": 0.0},
                {"nome": "Contabilista", "valor": 0.0},
                {"nome": "Extras Anuais", "valor": 0.0}
            ]
        }
        self.salvar_dados()
    
    def carregar_dados(self):
        """Carrega os dados do arquivo JSON"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def salvar_dados(self):
        """Salva os dados no arquivo JSON"""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            json.dump(self.despesas, f, ensure_ascii=False, indent=4)
    
    def mostrar_menu_principal(self):
        """Exibe o menu principal"""
        while True:
            print("\n" + "="*50)
            print("      GERENCIADOR DE DESPESAS PESSOAIS")
            print("="*50)
            print("1. Visualizar despesas")
            print("2. Editar despesa")
            print("3. Adicionar nova despesa")
            print("4. Ver resumo financeiro")
            print("5. Sair")
            print("="*50)
            
            opcao = input("Escolha uma opção (1-5): ").strip()
            
            if opcao == "1":
                self.mostrar_despesas()
            elif opcao == "2":
                self.editar_despesa()
            elif opcao == "3":
                self.adicionar_despesa()
            elif opcao == "4":
                self.mostrar_resumo()
            elif opcao == "5":
                print("A guardar dados... Até logo!")
                break
            else:
                print("Opção inválida. Tente novamente.")
    
    def mostrar_despesas(self):
        """Exibe todas as despesas organizadas por categoria"""
        print("\n" + "-"*50)
        print("         SUAS DESPESAS")
        print("-"*50)
        
        for categoria, itens in self.despesas.items():
            print(f"\n{categoria.upper()}:")
            print("-" * 30)
            total_categoria = 0
            for item in itens:
                print(f"  {item['nome']}: {item['valor']:.2f} €")
                total_categoria += item['valor']
            print(f"  TOTAL {categoria.upper()}: {total_categoria:.2f} €")
        
        input("\nPressione Enter para continuar...")
    
    def editar_despesa(self):
        """Permite editar o valor de uma despesa"""
        print("\n" + "-"*50)
        print("         EDITAR DESPESA")
        print("-"*50)
        
        # Mostrar categorias
        categorias = list(self.despesas.keys())
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria.capitalize()}")
        
        try:
            opcao_categoria = int(input("\nEscolha a categoria (número): ").strip())
            if opcao_categoria < 1 or opcao_categoria > len(categorias):
                print("Categoria inválida.")
                return
            
            categoria = categorias[opcao_categoria - 1]
            
            # Mostrar despesas da categoria escolhida
            print(f"\nDespesas {categoria}:")
            for i, item in enumerate(self.despesas[categoria], 1):
                print(f"{i}. {item['nome']}: {item['valor']:.2f} €")
            
            try:
                opcao_item = int(input("\nEscolha a despesa para editar (número): ").strip())
                if opcao_item < 1 or opcao_item > len(self.despesas[categoria]):
                    print("Despesa inválida.")
                    return
                
                novo_valor = float(input("Novo valor (€): ").strip())
                self.despesas[categoria][opcao_item - 1]["valor"] = novo_valor
                self.salvar_dados()
                print("Despesa atualizada com sucesso!")
                
            except (ValueError, IndexError):
                print("Valor ou opção inválida.")
                
        except (ValueError, IndexError):
            print("Opção inválida.")
    
    def adicionar_despesa(self):
        """Permite adicionar uma nova despesa personalizada"""
        print("\n" + "-"*50)
        print("         ADICIONAR DESPESA")
        print("-"*50)
        
        # Mostrar categorias
        categorias = list(self.despesas.keys())
        for i, categoria in enumerate(categorias, 1):
            print(f"{i}. {categoria.capitalize()}")
        
        try:
            opcao_categoria = int(input("\nEscolha a categoria (número): ").strip())
            if opcao_categoria < 1 or opcao_categoria > len(categorias):
                print("Categoria inválida.")
                return
            
            categoria = categorias[opcao_categoria - 1]
            
            nome = input("Nome da nova despesa: ").strip()
            if not nome:
                print("Nome não pode estar vazio.")
                return
            
            valor = float(input("Valor (€): ").strip())
            
            # Adicionar nova despesa
            self.despesas[categoria].append({"nome": nome, "valor": valor})
            self.salvar_dados()
            print("Despesa adicionada com sucesso!")
            
        except ValueError:
            print("Valor inválido.")
    
    def mostrar_resumo(self):
        """Exibe um resumo financeiro com totais e projeções"""
        print("\n" + "="*50)
        print("         RESUMO FINANCEIRO")
        print("="*50)
        
        totais = {
            "mensal": 0,
            "trimestral": 0,
            "anual": 0
        }
        
        # Calcular totais
        for item in self.despesas["mensais"]:
            totais["mensal"] += item["valor"]
        
        for item in self.despesas["trimestrais"]:
            totais["trimestral"] += item["valor"]
        
        for item in self.despesas["anuais"]:
            totais["anual"] += item["valor"]
        
        # Calcular totais anuais
        total_anual_mensal = totais["mensal"] * 12
        total_anual_trimestral = totais["trimestral"] * 4
        total_anual = total_anual_mensal + total_anual_trimestral + totais["anual"]
        
        # Mostrar resumo
        print(f"\nDespesas Mensais: {totais['mensal']:.2f} €")
        print(f"Despesas Trimestrais: {totais['trimestral']:.2f} €")
        print(f"Despesas Anuais: {totais['anual']:.2f} €")
        print("-" * 30)
        print(f"Total Anual (projeção): {total_anual:.2f} €")
        print(f"Total Mensal (média): {total_anual / 12:.2f} €")
        
        input("\nPressione Enter para continuar...")

def main():
    """Função principal"""
    app = GerenciadorDespesas()
    
    print("Bem-vindo ao Gestor de Despesas Pessoais!")
    print("Os seus dados estão a ser guardados em 'despesas.json'")
    
    app.mostrar_menu_principal()

if __name__ == "__main__":
    main()
