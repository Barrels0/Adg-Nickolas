import mysql.connector
from othrs.connectsql import obter_conexao
from othrs.force import force_str, force_float, force_int
from comandos.interface import exibir_menu_e_estoque


def busca():
    print("\n----- PESQUISAR POR NOME/TIPO/FORNECEDOR -------")
    termo_busca = force_str(
        "Digite o nome/tipo/fornecedor da bebida para busca:"
    ).lower()
    termo_com_curinga = f"%{termo_busca}%"  # ele usa o "%" antes e depois pq ai ele pega tudo, por exemplo o nome é vinho e se o usuario digitar vin ele acha do mesmo jeito
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT nome,tipo,fornecedor,safra,preco,quantidade,nota FROM estoque WHERE ativo = 1 AND (LOWER(nome) LIKE %s OR LOWER(tipo) LIKE %s OR fornecedor LIKE %s)",
            (termo_com_curinga, termo_com_curinga, termo_com_curinga),
        )
        resultados = cursor.fetchall()
        if resultados:
            print("\nESSAS FORAM AS INFORMAÇÕES ENCONTRADAS:")
            print("-" * 60)

            for linha in resultados:
                nome, tipo, fornecedor, safra, preco, quantidade, nota = linha
                print(
                    f"-> {nome} ({tipo}) | Safra: {safra} | Fornecedor: {fornecedor} | R$ {preco:.2f} | Estoque: {quantidade} | Nota: {nota}"
                )
        else:
            print("Nenhuma bebida encontrada com esse nome/tipo/fornecedor!")
    except mysql.connector.Error as e:
        print(f"Erro ao realizar a busca no banco de dados: {e}")
        return
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


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
            if "conexao" in locals() and conexao.is_connected():
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
                print(f"\n->" "\n-> ".join(estoque_barato))
                break
        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            return
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def catalogo_ordenado():
    while True:
        print("""
                \n-----CATALOGO ORDENADO-------
                1. Ordem alfabética
                2. Mais Barato Primeiro
                3. Mais Caros Primeiro
                4. Maior quantidade
                5. Menor quantidade
                """)
        ordem = force_int("Digite a maneira que você prefere organizar as bebidas: ")

        # sorted() > cria uma copia da lista que você selecionar, sem considerar o id
        #
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome,preco,quantidade FROM estoque")
        resultados = cursor.fetchall()

        query_base = "SELECT nome, preco, quantidade FROM livros WHERE ativo = 1"
        if ordem == 1:
            query_base = f"{query_base} ORDER BY LOWER(nome) ASC"
        elif ordem == 2:
            query_base = f"{query_base} ORDER BY preco ASC"
        elif ordem == 3:
            query_base = f"{query_base} ORDER BY preco DESC"
        elif ordem == 4:
            query_base = f"{query_base} ORDER BY quantidade DESC"
        elif ordem == 5:
            query_base = f"{query_base} ORDER BY quantidade ASC"
        else:
            conexao.close()
            cursor.close()
            print("Opção inválida")
            return exibir_menu_e_estoque

        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute(query_base)
        estoque_ordenado = cursor.fetchall()

        for bebida in estoque_ordenado:
            nome, preco, quantidade = bebida
            print(f"- {nome} - R${preco:.2f} (Qtd: {quantidade})")
        conexao.close()
        cursor.close()
        break


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
        if "conexao" in locals() and conexao.is_connected():
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
            print(
                f" -> BEBIDA MAIS VENDIDA: {dados_campeao[0]} ({dados_campeao[1]}) exemplares vendidos!"
            )
            break
        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            return
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
