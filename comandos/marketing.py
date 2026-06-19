from othrs.connectsql import obter_conexao
import mysql.connector
from othrs.force import force_int, force_float, force_str, bsc_id


def promocoes():
    while True:
        print("""---- MENU DE PROMOÇÕES ----
                1- Aplicar promoção em um item
                2- Aplicar promoção para todos os itens
                3- Aplicar promoção com base no tipo do item              
                        """)
        escolha_promo = force_int("\nEscolha uma opção: ")
        if escolha_promo == 1:
            desconto = force_float("Porcentagem de desconto: ")
            if 0 < desconto < 100:
                fator_desconto = (100 - desconto) / 100
            else:
                print("Desconto inválido!")
                continue
            id_produto = bsc_id()
            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                cursor.execute(
                    "UPDATE estoque SET preco = ROUND(preco * %s, 2) WHERE id = %s",
                    (
                        fator_desconto,
                        id_produto,
                    ),
                )
                conexao.commit()
                if cursor.rowcount > 0:
                    print("Desconto aplicado com sucesso!")
                else:
                    print("Nenhuma produto foi alterado, verifique se o id existe!")
            except mysql.connector.Error as e:
                print(f"Erro ao acessar o banco de dados: {e}")
                conexao.rollback()
                break
            finally:
                if "conexao" in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()

        elif escolha_promo == 2:
            desconto = force_float("Porcentagem de desconto: ")
            if 0 < desconto < 100:
                fator_desconto = (100 - desconto) / 100
            else:
                print("Desconto inválido!")
                continue
            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                cursor.execute(
                    "UPDATE estoque SET preco = ROUND(preco * %s, 2)", (fator_desconto,)
                )
                conexao.commit()
                print("Desconto aplicado com sucesso!")
                break
            except mysql.connector.Error as e:
                conexao.rollback()
                print(f"Error: ocorreu um erro: {e}")
                break
            finally:
                if "conexao" in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()
        elif escolha_promo == 3:
            tipo = force_str(
                "Qual o tipo de bebida que você deseja adicionar um desconto (Ex: Vinho, Whisky): "
            ).lower()
            try:
                desconto = force_float("Porcentagem de desconto: ")
                if 0 < desconto < 100:
                    fator_desconto = (100 - desconto) / 100
                else:
                    print("Desconto inválido!")
                    continue
            except ValueError:
                print("ERRO: Porcentagem ou tipo são invalidos")
                return

            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                cursor.execute(
                    "UPDATE estoque SET preco = ROUND(preco * %s, 2) WHERE LOWER(tipo) = %s",
                    (fator_desconto, tipo),
                )
                conexao.commit()
                print("Desconto aplicado com sucesso!")
                break
            except mysql.connector.Error as e:
                conexao.rollback()
                print(f"Error: ocorreu um erro: {e}")
                break
            finally:
                if "conexao" in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()
        else:
            print("Opção inválida!")
            continue


def add_cupom():
    print("-----ADICIONAR CUPOM-----")
    nome = force_str("Digite o nome do cupom: ").upper()
    desconto = force_int("Digite a porcentagem do desconto: ")
    qtd = force_int("Digite a quantidade de cupons: ")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
        INSERT INTO cupons(nome,desconto,quantidade)
        VALUES (%s,%s,%s)
        """,
            (
                nome,
                desconto,
                qtd,
            ),
        )
        conexao.commit()
    except mysql.connector.Error as e:
        conexao.rollback()
        print(f"Ocorreu um erro: {e}")
        return
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def ranking_cupons():
    print("\n--- RANKING DE CUPONS MAIS USADOS ---")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        # O MySQL processa o agrupamento e ordenação diretamente, eliminando loops manuais complexos
        cursor.execute("""
            SELECT nome, qtd_used
            FROM cupons
            ORDER BY qtd_used DESC 
        """)  # ORDER vai ordenar a coluna qtd_used em formato decrescente(DESC)
        ranking = cursor.fetchall()

        if not ranking:
            print("Sem dados de vendas para gerar o ranking!")
        else:
            print(
                f"{'CUPOM':<20} | {'VEZES UTILIZADO':<15}"
            )  # pesquisei uma maneira de deixar a formatação mais bonita!!!
            print("-" * 38)
            for cupom, qtd in ranking:
                print(
                    f" {cupom:<19} | {qtd} vezes"
                )  # pesquisei uma maneira de deixar a formatação mais bonita!!!
                print("-" * 38)
    except mysql.connector.Error as e:
        print(f"Erro ao gerar ranking: {e}")
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()


def adicionar_fornecedor():
    while True:
        print("\n----- NOVO FORNECEDOR --------")
        novo_fornecedor = force_str("Digite o nome do novo fornecedor: ").lower()
        fornecedor_pais = force_str("Digite o país do fornecedor: ").lower()
        fornecedor_cidade = force_str("Digite a cidade do fornecedor: ").lower()
        fornecedor_estado = force_str("Digite o estado do fornecedor: ").lower()

        try:
            fornecedor_qualidade = force_int(
                "Digite a qualidade do fornecedor (1-bom, 2-regular, 3-ruim): "
            )
            if fornecedor_qualidade < 1 or fornecedor_qualidade > 3:
                print("ERRO: Qualidade deve ser entre 1 e 3!")
                continue
        except ValueError:
            print("ERRO: Digite um número inteiro válido para a qualidade!")
            continue

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                    INSERT INTO fornecedores(nome,pais,cidade,estado,qualidade)
                    VALUES (%s,%s,%s,%s,%s)
                """,
                (
                    novo_fornecedor,
                    fornecedor_pais,
                    fornecedor_cidade,
                    fornecedor_estado,
                    fornecedor_qualidade,
                ),
            )
            conexao.commit()
            print(f"O fornecedor '{novo_fornecedor}' foi salvo com sucesso! ")
            return novo_fornecedor

        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            return "Sem Fornecedor"
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def teste_qualidade(id_produto):
    print("\n" + "=" * 20)
    print("---- TESTE DE QUALIDADE (AVALIAÇÃO) ----")
    print("=" * 20)

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT fornecedor,nota FROM estoque WHERE id = %s", (id_produto,)
        )
        resultados = cursor.fetchall()
        cursor.execute("SELECT * FROM fornecedores")  # usa em outras operações!
        fornecedor = cursor.fetchall()

        if not resultados:
            return False

        nota_produto = resultados[0][1]
        nome_fornecedor = resultados[0][0]
    except mysql.connector.Error as e:
        conexao.rollback()
        print(f"Ocorreu um erro: {e}")
        return
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

    status_fornecedor = "Não cadastrado"

    # Busca a qualidade do fornecedor dessa bebida específico
    for bebida in fornecedor:
        if bebida[1].strip().lower() == nome_fornecedor.strip().lower():
            if bebida[2] == 1:
                status_fornecedor = "Bom"
            elif bebida[2] == 2:
                status_fornecedor = "Regular"
            elif bebida[2] == 3:
                status_fornecedor = "Ruim"

    if nota_produto == 5:
        print(
            f"Produto excelente (Nota 5)! Fornecedor associado: {nome_fornecedor.title()} (Status: {status_fornecedor})."
        )
    elif nota_produto == 4:
        print(
            f"Produto bem avaliado (Nota 4). Fornecedor associado: {nome_fornecedor.title()} (Status: {status_fornecedor})."
        )
    elif nota_produto == 3:
        print(
            f"Produto com avaliação regular (Nota 3). Pode conter pequenas variações."
        )
    elif nota_produto == 2:
        print(
            f"ATENÇÃO: Produto mal avaliado (Nota 2). Avaliando a remoção do catálogo."
        )
    else:
        print(
            f"PERIGO: Produto péssimo (Nota 1). A adega não se responsabiliza por defeitos!"
        )

    confirmacao = force_str(
        "\nDeseja prosseguir com a compra deste item? (S/N): "
    ).upper()

    if confirmacao == "S":
        print("-> Qualidade aceita pelo cliente. Prosseguindo...")
        return True
    else:
        print("-> Operação cancelada pelo cliente por critérios de qualidade.")
        return False
