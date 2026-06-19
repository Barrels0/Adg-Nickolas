from othrs.force import force_str, force_int
from othrs.connectsql import obter_conexao
import mysql.connector, datetime
from comandos.marketing import teste_qualidade


def registar_venda():
    print("\n======CARINHO DE COMPRAS (SQLITE)======")
    carrinho = []

    while True:
        try:
            id_venda = force_int(
                "Digite o [ID] do produto que você deseja: (-1 para concluir compra -2 para cancelar)"
            )
        except ValueError:
            print("ERRO: ID DEVE SER UM NUMERO INTE IRO")
            continue
        if id_venda == -1:
            break
        elif id_venda == -2:
            print("Compra cancelada!")
            carrinho = []
            return

        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome, tipo, fornecedor, safra, quantidade, preco, nota, ativo FROM estoque WHERE id= %s",
            (id_venda,),
        )
        bebida_encontrada = cursor.fetchone()

        if not bebida_encontrada:
            print("ERRO ID INVÁLIDO. Essa bebida não existe no sistema")
            conexao.close()
            cursor.close()
            continue
        elif bebida_encontrada[8] == 0:
            print("Bebida esta atualmente desativada, tente outra opção!")
            continue

        (
            nome_bebida,
            tipo_bebida,
            fornecedor_bebida,
            safra_bebida,
            quantidade_bebida,
            preco_bebida,
            nota_bebida,
        ) = bebida_encontrada

        conexao.close()
        cursor.close()

        venda_autorizada = teste_qualidade(id_venda)
        if not venda_autorizada:
            print("-> Produto rejeitado no teste de qualidade. Escolha outro item.")
            continue
        try:
            quantidade = force_int(f"Quantos garrafas do {nome_bebida} você deseja: ")
        except ValueError:
            print("ERRO: quantidade invalida")
            continue
        qtd_carrinho = sum(
            item["quantidade"] for item in carrinho if item["id"] == id_venda
        )
        estoque_disponivel = quantidade_bebida - qtd_carrinho

        if quantidade <= 0:
            print("ERRO: Quantidade inválida")
            continue
        elif quantidade > estoque_disponivel:
            print(
                f"Estoque insuficiente. Você ja tem {qtd_carrinho} no carrinho, estoque total é de {quantidade_bebida}."
            )
            continue
        else:
            carrinho.append(
                {
                    "id": id_venda,
                    "nome": nome_bebida,
                    "tipo": tipo_bebida,
                    "fornecedor": fornecedor_bebida,
                    "safra": safra_bebida,
                    "quantidade": quantidade,
                    "preco": preco_bebida,
                    "nota": nota_bebida,
                    "subtotal": quantidade * preco_bebida,
                }
            )
            print(f"-> {quantidade}x '{nome_bebida}' adicionado ao carrinho!")
    if len(carrinho) > 0:
        total_compra = sum(item["subtotal"] for item in carrinho)
        print(f"\n =============FECHAMENTO CAIXA==============")
        print(f"Total a pagar: R${total_compra:.2f}")
        confirmar = force_str("Confirmar pagamento e registrar venda? (s/n): ").lower()

        if confirmar == "s":
            pass
            pagamento = force_str(
                "Qual o metodo de pagamento? ( 1-Pix | 2-Cartão de crédito | 3-Cartão de débito): "
            )
            if pagamento == "1":
                pagamento = "Pix"
            elif pagamento == "2":
                pagamento = "Cartão de crédito"
            elif pagamento == "3":
                pagamento = "Cartão de débito"
            else:
                print("ERRO:")
                return
            cupom = force_str("Você possui algum cupom de desconto? (S/N): ").upper()
            if cupom == "S" or cupom == "SIM":
                nm_cup = force_str("Digite o nome do seu cupom: ").upper()
                conexao = obter_conexao()
                cursor = conexao.cursor()
                cursor.execute(
                    "SELECT nome,desconto,quantidade FROM cupons WHERE nome = %s",
                    (nm_cup,),
                )
                result = cursor.fetchone()
                if not result or result[2] == 0:
                    print("Cupom inválido ou esgotado!")
                else:
                    total_compra *= 1 - result[1] / 100
                    print("Cupom aplicado com sucesso!")
                    cursor.execute(
                        "UPDATE cupons SET quantidade = quantidade -1,qtd_used = qtd_used + 1 WHERE nome = %s",
                        (result[0],),
                    )
            else:
                pass
            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                for item in carrinho:
                    cursor.execute(
                        """
                            UPDATE estoque
                            SET quantidade = quantidade - %s
                            SET qtd_vend = qtd_vend + %s
                            WHERE id = %s
                        """,
                        (item["quantidade"], item["quantidade"], item["id"]),
                    )
                    cursor.execute(
                        """
                            INSERT INTO vendas (horarios,id_bebida, tipo, fornecedor, safra, quantidade, preco, valor, pagamento)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                        (
                            datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            item["id"],
                            item["tipo"],
                            item["fornecedor"],
                            item["safra"],
                            item["quantidade"],
                            item["preco"],
                            item["subtotal"],
                            pagamento,
                        ),
                    )
                    conexao.commit()
                    print("Venda concluida com sucesso")
            except mysql.connector.Error as erro:
                conexao.rollback()
                print("\nERRO FATAL NO BANCO DE DADOS: Transação cancelada.")
                print(f"Motivo tecnico: {erro}")
                print(
                    "O estoque foi restaurado e nenhuma nota fiscal corrompida foi gerada."
                )
                return
            finally:  # O bloco 'finally' garante que fechará a conexão dando erro ou dando certo
                if "conexao" in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()
        else:
            print("Venda não realizada")


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
                print(
                    f"[{venda[0]}] | Data/Hora: {venda[1]} | {venda[2]}x {venda[3]} (R$ {venda[4]:.2f}) | Total: R$ {venda[5]:.2f}"
                )
    except mysql.connector.Error as e:
        conexao.rollback()
        print(f"Ocorreu um erro: {e}")
        return
    finally:
        if "conexao" in locals() and conexao.is_connected():
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
        faturamento_total = cursor.fetchone()[
            0
        ]  # esse [0] é pq ele so quer a primeira info da tupla

        nome_arquivo = (
            f"fechamento_caixa{datetime.datetime.now().strftime('%y_%m_%d_%Hh%Mm%Ss')}"
        )
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("=================================\n")
            arquivo.write("        RELATORIO DE VENDAS      \n")
            arquivo.write("=================================\n")

            for venda in vendas:
                linha = f"DATA: {venda[0]} | Bebida: {venda[1]} | Quantidade {venda[2]}"
                arquivo.write(linha)
            arquivo.write(
                f"==========FATURAMENTO TOTAL DO DIA DE HOJE: R${faturamento_total:.2f}=========="
            )
        print(f"SUCESSO! Arquivo '{nome_arquivo}' foi criado na sua pasta!")
    except mysql.connector.Error as e:
        conexao.rollback()
        print(f"Ocorreu um erro: {e}")
        return
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
