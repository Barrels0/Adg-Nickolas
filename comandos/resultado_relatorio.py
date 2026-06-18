from comandos.interface import exibir_menu_e_estoque
from force import force_float,force_int
import datetime
from connectsql import obter_conexao
import mysql.connector

conexao = obter_conexao()
cursor = conexao.cursor()
cursor.execute("SELECT * FROM vendas")
historico_vendas = cursor.fetchall()
caixa = sum(venda[8] for venda in historico_vendas)

def nota_fiscal():
    print("\n=====NOTA FISCAL===============")
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT vendas.id, vendas.horarios, vendas.quantidade, vendas.tipo, vendas.fornecedor, vendas.safra, vendas.preco, vendas.valor, vendas.pagamento
            FROM vendas
            INNER JOIN estoque ON vendas.id_bebida = estoque.id
        """)
        historico = cursor.fetchall()

        if len(historico) == 0:
                print("Nenhuma venda até o momento!")
        else:
            for venda in historico:
                print(f"[{venda[0]}] | Data/Hora: {venda[8]} | {venda[1]} x {venda[4]} | Total venda R$: {venda[7]:.2f}")
    except mysql.connector.Error as e:
         conexao.rollback()
         print(f"Ocorreu um erro: {e}")
         return
    finally:
        if 'conexao' in locals() and conexao.is_connected(): 
         cursor.close()
         conexao.close()

def painel_produtomaisvendido():
    while True:   
        print("----Painel de Estatisticas e Balanço/Produto Mais Vendido----")
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
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
                SELECT vendas.id, vendas.horarios, vendas.quantidade, vendas.tipo, vendas.fornecedor, vendas.safra, vendas.preco, vendas.valor, vendas.pagamento
                FROM vendas
                INNER JOIN estoque ON vendas.id_bebida = estoque.id
                GROUP BY estoque.nome
                ORDER BY SUM(vendas.quantidade) DESC
                LIMIT 3
            """)
            dados_campeao = cursor.fetchone()
            print(f" -> BEBIDA MAIS VENDIDA: {dados_campeao[0]} ({dados_campeao[1]}) exemplares vendidos!")
            break
        except mysql.connector.Error as e:
                 conexao.rollback()
                 print(f"Ocorreu um erro: {e}")
                 return
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
             
        
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
            acao_pos_comando = force_int("Escolha uma ação: ")
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
            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                cursor.execute("SELECT nome FROM estoque WHERE quantidade < 3")

                estoque_baixo = [linha[0] for linha in cursor.fetchall()]

                if len(estoque_baixo) == 0:
                    print("Nenhuma bebida encontrada com estoque baixo!")
                    break
                else:
                    print("\n-> ".join(estoque_baixo))
                    break
            except mysql.connector.Error as e:
                 conexao.rollback()
                 print(f"Ocorreu um erro: {e}")
                 return
            finally:
                if 'conexao' in locals() and conexao.is_connected():
                 cursor.close()
                 conexao.close()

def filtros():
    while True:
        print("=====FILTRO POR PREÇO=====")
        prec_limit = force_float("Digite um valor limite que você deseja gastar: ")                
        print(f"Bebidas populares abaixo de R${prec_limit}: ")
        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:    
                cursor.execute("SELECT nome FROM estoque WHERE preco <= %s", (prec_limit,))
                estoque_barato = [linha[0] for linha in cursor.fetchall()]
                if len(estoque_barato) == 0:
                    print("Nenhuma bebida encontrada abaixo de 50 reais!")
                    break
                else:
                    print(f"\n->""\n-> ".join(estoque_barato))
                    break
        except mysql.connector.Error as e:
                 conexao.rollback()
                 print(f"Ocorreu um erro: {e}")
                 return
        finally:
            if 'conexao' in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
             

def exportar_relatorio_txt():
    print("\nGerando relatorio de fechamento...")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT vendas.horarios, estoque.nome, vendas.quantidade, vendas.valor
            FROM vendas
            INNER JOIN estoque on vendas.id_bebida = estoque.id
            ORDER BY vendas.id ASC
        """)
        vendas = cursor.fetchall()

        if not vendas:
             print("Nenhuma venda registrada")
             return
        cursor.execute("SELECT SUM(valor) FROM vendas")
        faturamento_total = cursor.fetchone()[0]# esse [0] é pq ele so quer a primeira info da tupla

        nome_arquivo = f"fechamento_caixa{datetime.datetime.now().strftime('%y_%m_%d_%Hh%Mm%Ss')}"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
             arquivo.write("=================================\n")
             arquivo.write("        RELATORIO DE VENDAS      \n")
             arquivo.write("=================================\n")

             for venda in vendas:
                  linha = f"DATA: {venda[0]} | Bebida: {venda[1]} | Quantidade {venda[2]}"
                  arquivo.write(linha)
             arquivo.write(f"==========FATURAMENTO TOTAL DO DIA DE HOJE: R${faturamento_total:.2f}==========")
        print(f"SUCESSO! Arquivo '{nome_arquivo}' foi criado na sua pasta!")
    except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            return
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()