from comandos.interface import exibir_menu_e_estoque
from othrs.force import force_float,force_int
import datetime
from othrs.connectsql import obter_conexao
import mysql.connector

def nota_fiscal():
    print("\n=====NOTA FISCAL===============")
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute("""
            SELECT vendas.id, vendas.horarios, vendas.quantidade, estoque.nome, vendas.preco, vendas.valor
            FROM vendas
            INNER JOIN estoque ON vendas.id_bebida = estoque.id
        """)
        historico = cursor.fetchall()

        if len(historico) == 0:
                print("Nenhuma venda até o momento!")
        else:
            for venda in historico:
                print(f"[{venda[0]}] | Data/Hora: {venda[1]} | {venda[2]}x {venda[3]} (R$ {venda[4]:.2f}) | Total: R$ {venda[5]:.2f}")
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
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        # O MySQL processa o agrupamento e ordenação diretamente, eliminando loops manuais complexos
        cursor.execute("""
            SELECT estoque.nome, CAST(SUM(vendas.quantidade) AS SIGNED) as total
            FROM vendas
            INNER JOIN estoque ON vendas.id_bebida = estoque.id
            GROUP BY estoque.id, estoque.nome
            ORDER BY total DESC
        """)
        ranking = cursor.fetchall()

        if not ranking:
            print("Sem dados de vendas para gerar o ranking!")
        else:
            for produto, qtd in ranking:
                print(f" {produto}: {qtd} unidades vendidas")
    except mysql.connector.Error as e:
        print(f"Erro ao gerar ranking: {e}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

def continuar_sistema():
    while True:
        print("-"*10)
        print("[1] Continuar no Menu")
        print("[2] Voltar")
        print("-"*10)
        try:
            acao_pos_comando = force_int("Escolha uma ação: ")
            if acao_pos_comando == 1 or acao_pos_comando == 2:
                return
            else:
                print("Opção inválida!")
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