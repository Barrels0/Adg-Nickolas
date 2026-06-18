import datetime
import mysql.connector
from othrs.connectsql import obter_conexao
from othrs.force import force_int,force_str
from comandos.testequalidade import teste_qualidade


# ADICIONAR O TESTE DE QUALIDADE NESSE CODIGO!
def realizar_venda():
    print("\n======CARINHO DE COMPRAS (SQLITE)======")
    carrinho = []

    while True:
        try:
            id_venda = force_int("Digite o [ID] do produto que você deseja: (-1 para concluir compra -2 para cancelar)")
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
            "SELECT nome, tipo, fornecedor, safra, quantidade, preco, nota FROM estoque WHERE id= %s",
            (id_venda,),
        )
        bebida_encontrada = cursor.fetchone()

        if not bebida_encontrada:
            print("ERRO ID INVÁLIDO. Essa bebida não existe no sistema")
            conexao.close()
            cursor.close()
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
        confirmar = force_str("Confirmar paramento e registrar venda? (s/n): ").lower()

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
            conexao = obter_conexao()
            cursor = conexao.cursor()
            try:
                for item in carrinho:
                    cursor.execute(
                         """
                            UPDATE estoque
                            SET quantidade = quantidade - %s
                            WHERE id = %s
                        """,
                        (item["quantidade"], item["id"]),
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
            finally: # O bloco 'finally' garante que fechará a conexão dando erro ou dando certo
                if 'conexao' in locals() and conexao.is_connected():
                    cursor.close()
                    conexao.close()
        else:
            print("Venda não realizada")



"""
from comandos.testequalidade import teste_qualidade
from comandos.banco_dados import salvar_arquivo, carregar_arquivo
import datetime

def vender(novo_estoque,historico_vendass,cuponss,caixaa):
    print("\n----- CARRINHO DE COMPRAS --------")

    carrinho = []
    while True:
            try:
                id_venda = int(
                    input(
                        "Digite o [ID] do produto que você deseja comprar: (ou -1 para finalizar a compra, -2 para cancelar a compra): "
                    )
                )
            except ValueError:
                print("ERRO: VALOR INVÁLIDO")
                continue

            if id_venda == -1:
                break
            elif id_venda == -2:
                print("Compra cancelada")
                carrinho = []
                break
            if id_venda < -2 or id_venda >= len(novo_estoque):
                print("ERRO")
                continue

            venda_autorizada = teste_qualidade(id_venda, novo_estoque)
            if not venda_autorizada:
                continue

            try:
                quantidade_desejada = int(
                    input(
                        f"Quanto exemplares do {novo_estoque[id_venda]['nome']} você deseja adicionar: "
                    )
                )
            except ValueError:
                print("ERRO: VALOR INVÁLIDO")
                continue
            qtd_ja_no_carrinho = sum(
                item["quantidade"] for item in carrinho if item["id"] == id_venda
            )
            estoque_disponivel = novo_estoque[id_venda]["quantidade"] - qtd_ja_no_carrinho

            if quantidade_desejada <= 0:
                print("ERRO: QUANTIDADE INVÁLIDA")
            elif quantidade_desejada > novo_estoque[id_venda]["quantidade"]:
                print(
                    f"ESTOQUE INSUFICIENTE. Você ja tem {qtd_ja_no_carrinho} e no estoque ainda restam {novo_estoque[id_venda]['quantidade']}"
                )
            else:
                # adiciona item no carrinho(SOMENTE TEMPORARIO)
                carrinho.append(
                    {
                        "id": id_venda,
                        "nome": novo_estoque[id_venda]["nome"],
                        "preco": novo_estoque[id_venda]["preco"],
                        "quantidade": quantidade_desejada,
                        "subtotal": quantidade_desejada * novo_estoque[id_venda]["preco"],
                    }
                )
                print(
                    f"-> {quantidade_desejada}x '{novo_estoque[id_venda]['nome']}' adicionado ao carrinho! "
                )
    if len(carrinho) > 0:
            total_compra = sum(item["subtotal"] for item in carrinho)
            print(f"\n =============FECHAMENTO CAIXA==============")
            print(f"Total a pagar: R${total_compra:.2f}")
            confirmar = (
                input("Confirmar pagamento e registrar a venda? (S/N)").strip().upper()
            )

            if confirmar == "S":
                print("----CUPOM----")
                cupom = input("Digite um cupom ou não escreva nada caso não tenha!").strip().upper()
                encontrou = False
                for id_cupom, cupomm in enumerate(cuponss):
                    if cupom in cupomm["nome"]:
                        if cupomm['quantidade'] > 0:
                            total_compra = total_compra * (1 - (cupomm['desconto'] / 100))
                            cupomm['quantidade'] -= 1
                            encontrou = True
                        else: 
                            print("Não possuimos mais unidades desse cupom!")
                            continue
                if not encontrou:
                    print("Não achamos nenhum cupom com esse nome!")
                    pass
                for item in carrinho:
                    novo_estoque[item["id"]]["quantidade"] -= item["quantidade"]

                    historico_vendass.append(
                        {
                            "horarios": datetime.datetime.now().strftime(
                                "%d/%m/%y %H:%M:%S"
                            ),
                            "item": item["nome"],  # ou item["nome"]
                            "tipo": novo_estoque[item["id"]]["tipo"],
                            "safra": novo_estoque[item["id"]]["safra"],
                            "quantidade": item["quantidade"],
                            "fornecedor": novo_estoque[item["id"]]["fornecedor"],
                            "preco": novo_estoque[item["id"]]["preco"],
                            "valor": item["subtotal"],
                        }
                    )
                caixaa += total_compra
                salvar_arquivo("estoque.json", novo_estoque)
                salvar_arquivo("vendas.json", historico_vendass)
                print("VENDA EFETIVADA. Confira o recibo no menu!!!")
            else:
                print("Compra cancelada! Carrinho descartado")
"""
