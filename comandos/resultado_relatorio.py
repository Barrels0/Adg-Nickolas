from comandos.interface import exibir_menu_e_estoque
import sqlite3
with sqlite3.connect("adegas123.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM vendas")
        historico_vendas = cursor.fetchall()
caixa = sum(venda[8] for venda in historico_vendas)
def nota_fiscal():
    print("\n=====NOTA FISCAL===============")
    
    with sqlite3.connect("adegas123.db") as conexao:
         cursor = conexao.cursor()
         cursor.execute("""
            SELECT vendas.id, vendas.horarios, vendas.quantidade, vendas.tipo, vendas.fornecedor, vendas.safra, vendas.preco, vendas.valor, vendas.pagamento
            FROM vendas
            INNER JOIN estoque ON vendas.id_bebida = bebidas.id
         """)
         historico = cursor.fetchall()

         if len(historico) == 0:
              print("Nenhuma venda até o momento!")
         else:
              for venda in historico:
                print(f"[{venda[0]}] | Data/Hora: {venda[8]} | {venda[1]} x {venda[4]} | Total venda R$: {venda[7]:.2f}")

def painel_produtomaisvendido():
    while True:   
        print("----Painel de Estatisticas e Balanço/Produto Mais Vendido----")
        with sqlite3.connect("adegas123.db") as conexao:
             cursor = conexao.cursor()
             cursor.execute("SELECT COUNT(*) FROM vendas")
             if cursor.fetchone()[0] == 0:
                  print("Sem dados disponiveis para o balanço!")
                  return
             cursor.execute("SELECT SUM(valor) FROM vendas")
             faturamento = cursor.fetchone()[0]
             print(f"Historico de faturamento Bruto: R${faturamento:.2f}")

             cursor.execute("SELECT AVG(valor) FROM vendas")
             ticket_medio = cursor.fetchone()[0]
             print(f"====Ticket Médio por venda: R${ticket_medio:.2f}")

             cursor.execute("""
                SELECT vendas.id, vendas.horarios, vendas.quantidade, vendas.tipo, vendas.fornecedor, vendas.safra, vendas.preco, vendas.valor, vendas.pagamento " \
                FROM vendas
                INNER JOIN estoque ON vendas.id_bebida = bebidas.id
                GROUP BY estoque.nome
                ORDER BY SUM(vendas.quantidade) DESC
                LIMIT 3
             """)
             produto_campeao, maior_quantidade = cursor.fetchone()
             print(f" -> BEBIDA MAIS VENDIDA: {produto_campeao} ({maior_quantidade}) exemplares vendidos!")
             break
        
def ranking_vendas():
    print("\n--- RANKING DE MAIS VENDIDOS ---")
    if len(historico_vendas) == 0:
            print("Sem dados de vendas para gerar o ranking!")
    else:
            contagem_vendas = {}
            # Preenche o dicionário somando as quantidades vendidas de cada item
            for venda in historico_vendas:
                produto_nome = venda[2]
                qtd = venda[6]
                if produto_nome in contagem_vendas:
                    contagem_vendas[produto_nome] += qtd
                else:
                    contagem_vendas[produto_nome] = qtd

            mais_vendidos = sorted(contagem_vendas.items(), key=lambda item: item[1], reverse=True)

            for produto, qtd in mais_vendidos:
                print(f" {produto.title()}: {qtd} unidades vendidas")

def continuar_sistema():
     while True:
        print("-"*10)
        print("[1] FECHAR SISTEMA")
        print("[2] Continuar")
        print("-"*10)
        try:
            acao_pos_comando = int(input("Escolha uma ação: "))
            if acao_pos_comando == 1:
                print(f"Encerrando sistema o valor total em caixa é de R${caixa:.2f}")
                exit()
            return
        except ValueError:
            return exibir_menu_e_estoque

def relatorios_expresso():
    while True: 
            print("\n=========RELATORIOS EXPRESSOS=========")
            print("Bebidas em ALERTA DE ESTOQUE: (menos que 3 unidades): ")
            with sqlite3.connect("adegas123.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute("SELECT nome FROM estoque WHERE quantidade < 3")

                estoque_baixo = [linha[0] for linha in cursor.fetchall()]

                if len(estoque_baixo) == 0:
                    print("Nenhuma bebida encontrada com estoque baixo!")
                    break
                else:
                    print("\n-> ".join(estoque_baixo))
                    break

def filtros():
    while True:
        print("=====FILTRO POR PREÇO=====")
        prec_limit = float(input("Digite um valor limite que você deseja gastar: "))                    
        print(f"Bebidas populares abaixo de R${prec_limit}: ")
        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM estoque WHERE preco <= ?", (prec_limit,))
            estoque_barato = [linha[0] for linha in cursor.fetchall()]
        if len(estoque_barato) == 0:
            print("Nenhuma bebida encontrada abaixo de 50 reais!")
            break
        else:
            print(f"\n->""\n-> ".join(estoque_barato))
            break

    