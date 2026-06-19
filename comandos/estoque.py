from othrs.api import buscar_vinho
from othrs.force import force_int, force_float, force_str, bsc_id
from othrs.connectsql import obter_conexao
import mysql.connector, random
from comandos.marketing import adicionar_fornecedor


def adicionar_item() -> None:

    while True:
        print("\n----- CADASTRAR NOVA BEBIDA --------")
        nome_vinho = input("Digite o nome do vinho que vc deseja:")

        print("Buscando informações na API...")
        vinho_dados = buscar_vinho(nome_vinho)

        if not vinho_dados:
            print("Erro para encontrar o vinho")
            return None

        for id_vinho, vinho in enumerate(vinho_dados, 1):
            print(f"ID:{id_vinho} | NOME: {vinho['name']}")

        escolha_vinho = force_int(
            "Coloque o id do vinho que deseja cadastrar no sistema: "
        )

        vinho_escolhido_pelo_usuario = vinho_dados[escolha_vinho - 1]

        name = vinho_escolhido_pelo_usuario.get("name", "Desconhecido")
        type = vinho_escolhido_pelo_usuario.get("type", "Desconhecido")
        producer = vinho_escolhido_pelo_usuario.get("winery", "Desconhecido")
        averageRating = vinho_escolhido_pelo_usuario.get("averageRating", 0.00)

        raw_vintage = vinho_escolhido_pelo_usuario.get(
            "vintage"
        ) or vinho_escolhido_pelo_usuario.get(
            "year", 0
        )  # usei IA pq estava desesperado kkkkkkkkkkkk
        vintage = 0
        if raw_vintage:
            numeros = "".join(char for char in str(raw_vintage) if char.isdigit())
            if numeros:
                vintage = int(numeros)
        if vintage == 0:
            vintage = random.randint(1996, 2026)  # gambiarra pq a API não puxa a safra

        novo_preco = force_float("Digite o preço do vinho: ")
        nova_quantidade = force_int("Quantidade disponivel em estoque: ")

        # Inicializa a variável com uma string padrão de segurança
        novo_fornecedor = "Sem Fornecedor"

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute("""
                SELECT id, nome, pais, cidade, estado, qualidade FROM fornecedores
                           """)
            resultado = cursor.fetchall()

            if resultado:
                print("\nEsses são os nossos fornecedores:")
                for linha in resultado:
                    id_forn, nome, pais, cidade, estado, qualidade = linha

                    # Converte o número da qualidade para texto legível no print
                    txt_qualidade = {1: "Bom", 2: "Regular", 3: "Ruim"}.get(
                        qualidade, "Não Informada"
                    )

                    print(
                        f"-> {id_forn} | Nome: {nome} | Pais: {pais} | Cidade: {cidade} | Estado: {estado} | Qualidade: {txt_qualidade}"
                    )

                fornece = force_int(
                    "\nO fornecedor desse produto é algum desses? (1-Sim | 2-Não): "
                )
                if fornece == 1:
                    escolha = force_int("Digite o [ID] do seu fornecedor: ")
                    cursor.execute(
                        """
                    SELECT nome 
                    FROM fornecedores
                    WHERE id = %s
                           """,
                        (escolha,),
                    )
                    result = cursor.fetchone()
                    if result:
                        novo_fornecedor = result[0]
                    else:
                        print("Fornecedor não encontrado com esse ID!")
                        continue
                elif fornece == 2:
                    novo_fornecedor = adicionar_fornecedor()
                else:
                    print("Digite um valor valido!")
                    return
            else:
                print("\nNenhum fornecedor cadastrado ainda!")
                opcao = force_int(
                    "Deseja cadastrar um novo fornecedor agora? (1-Sim | 2-Não): "
                )
                if opcao == 1:
                    novo_fornecedor = adicionar_fornecedor()
                else:
                    print("Operação cancelada.")
                    return

        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro ao processar fornecedores: {e}")
            return
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

        if vintage is None or vintage == 0:
            vintage = 0

        if novo_fornecedor is None or novo_fornecedor == "":
            novo_fornecedor = "Sem Fornecedor"

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO estoque(nome,tipo,winery,safra,preco,quantidade,fornecedor,nota)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    name,
                    type,
                    producer,
                    vintage,
                    novo_preco,
                    nova_quantidade,
                    novo_fornecedor,
                    averageRating,
                ),
            )
            conexao.commit()
            print(f"Bebida '{name}' foi salvo com sucesso! ")
            return
        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro ao salvar no banco: {e}")
            return
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def alteracoes():
    while True:
        try:
            alteracao = force_str(
                "\nVocê deseja alterar o preço ou repor estoque (digite 'preço' ou 'estoque'): "
            ).lower()

            if alteracao == "preço" or alteracao == "preco":
                print("\n----- ALTERAR PREÇO --------")
                try:
                    id_venda = bsc_id()

                    conexao = obter_conexao()
                    cursor = conexao.cursor()
                    try:
                        cursor.execute(
                            "SELECT nome, preco FROM estoque WHERE id = %s", (id_venda,)
                        )
                        bebida = cursor.fetchone()

                        if not bebida:
                            print("ERRO: Bebida não encontrada no banco de dados!")
                            continue

                        nome_bebida = bebida[0]
                        preco_atual = bebida[1]

                        novo_preco = force_float(
                            f"Atualizar o preço da bebida {nome_bebida} (PREÇO ATUAL: R${preco_atual}): "
                        )

                        preco_atual = novo_preco

                        conexao = obter_conexao()
                        cursor = conexao.cursor()
                        cursor.execute(
                            """
                            UPDATE estoque 
                            SET preco = %s 
                            WHERE id = %s
                        """,
                            (preco_atual, id_venda),
                        )

                        conexao.commit()
                        print(
                            f"\Alteração feita com sucesso! '{nome_bebida}' agora custa R${preco_atual}."
                        )
                        break

                    except mysql.connector.Error as e:
                        conexao.rollback()
                        print("\nERRO FATAL NO BANCO DE DADOS: Transação cancelada.")
                        print(f"Motivo tecnico: {e}")
                        print(
                            "O estoque foi restaurado e nenhuma nota fiscal corrompida foi gerada."
                        )
                        break
                    finally:
                        if "conexao" in locals() and conexao.is_connected():
                            conexao.close()
                            cursor.close()
                except ValueError:
                    print("ERRO: Digite um valor válido!")

            elif alteracao == "estoque":
                print("\n----- REPOR ESTOQUE --------")

                try:
                    id_venda = bsc_id()

                    conexao = obter_conexao()
                    cursor = conexao.cursor()
                    try:
                        cursor.execute(
                            "SELECT nome, quantidade FROM estoque WHERE id = %s",
                            (id_venda,),
                        )
                        bebida = cursor.fetchone()

                        # VALIDAÇÃO: Se o banco retornou None, o ID digitado não existe na tabela
                        if not bebida:
                            print("ERRO: Bebida não encontrada no banco de dados!")
                            continue

                        # separa os valores vindos pelo select usando os seus indices
                        nome_bebida = bebida[0]
                        quantidade_atual = bebida[1]

                        quantidade_adicional = force_int(
                            f"Quantidade para adicionar ao {nome_bebida.title()} (Atual: {quantidade_atual}): "
                        )

                        quantidade_atual += quantidade_adicional

                        conexao = obter_conexao()
                        cursor = conexao.cursor()
                        cursor.execute(
                            """
                            UPDATE estoque 
                            SET quantidade = %s 
                            WHERE id = %s
                        """,
                            (quantidade_atual, id_venda),
                        )

                        conexao.commit()
                        print(
                            f"\nReposição feita com sucesso! '{nome_bebida}' agora tem {quantidade_atual} unidades."
                        )
                        break
                    except mysql.connector.Error as e:
                        conexao.rollback
                        print(f"Erro no bando de dados: {e}")
                        break
                    finally:
                        if "conexao" in locals() and conexao.is_connected():
                            conexao.close()
                            cursor.close()

                except ValueError:
                    print("ERRO: Digite valores numéricos válidos!")
                    continue
        except ValueError:
            print("Digite um valor correspondente ao que foi solicitado!")
            continue


def desativar_bebida():
    while True:
        print("\n=======DESATIVAR BEBIDA DO CATALÓGO (Soft delete)========")
        id_produto = bsc_id()

        if id_produto == 0 or id_produto is None:
            print("Retornando ao menu anterior! ")
            break

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT nome FROM estoque WHERE id = %s AND ativo = 1", (id_produto,)
            )
            bebida = cursor.fetchone()

            if not bebida:
                print("ERRO: Bebida não encontrada ou já foi desativado.")
                continue

            print("(Digite 0 pra cancelar e voltar ao menu)")
            confirmar = force_str(
                f"Tem certeza que deseja excluir a bebida '{bebida[0]}'? (Historico de vendas sera mantido. (s/n:) )"
            ).lower()

            if confirmar == "0" or confirmar == "n":
                print("operação cancelada! ")
                break

            if confirmar == "s":
                cursor.execute(
                    "UPDATE estoque SET ativo = 0 WHERE id = %s", (id_produto,)
                )
                conexao.commit()
                print("Bebida desativado do catalago com sucesso!!!!!")
                break
            else:
                print("Opção inválida. Digite 's' para sim ou 'n' para não.")
                continue
        except mysql.connector.Error as e:
            print(f"Erro no banco de dados: {e}")
            conexao.rollback()
            break
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def reativar_bebida():
    while True:
        print("\n=======REATIVAR BEBIDA DO CATALÓGO========")
        id_produto = bsc_id()

        if id_produto == 0 or id_produto is None:
            print("Retornando ao menu anterior! ")
            break

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT nome FROM estoque WHERE id = %s AND ativo = 0", (id_produto,)
            )
            bebida = cursor.fetchone()

            if not bebida:
                print("ERRO: Bebida não encontrada")
                continue

            print("(Digite 0 pra cancelar e voltar ao menu)")
            confirmar = force_str(
                f"Tem certeza que deseja reativar a bebida '{bebida[0]}'? (Historico de vendas sera mantido. (s/n:) )"
            ).lower()

            if confirmar == "0" or confirmar == "n":
                print("operação cancelada! ")
                break

            if confirmar == "s":
                cursor.execute(
                    "UPDATE estoque SET ativo = 1 WHERE id = %s", (id_produto,)
                )
                conexao.commit()
                print("Bebida reativado do catalago com sucesso!!!!!")
                break
            else:
                print("Opção inválida. Digite 's' para sim ou 'n' para não.")
                continue
        except mysql.connector.Error as e:
            print(f"Erro no banco de dados: {e}")
            conexao.rollback()
            break
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def corrigir_nome():
    id_alvo = bsc_id()
    nome_correto = force_str("Digite o nome correto do vinho: ").lower()

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            """
                UPDATE estoque
                SET nome = %s
                WHERE id = %s           
                        """,
            (nome_correto, id_alvo),
        )
        if cursor.rowcount > 0:
            print("Nome altered com sucesso!")
        else:
            print("Nenhum produto encontrado!")
    except mysql.connector.Error as e:
        print(f"Erro no banco de dados: {e}")
        conexao.rollback()
        return
    finally:
        if "conexao" in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()



def sugestoes():
    print("=====SUGESTÕES=====")
    sugest = force_int("1 -> Carnes\n2 -> Peixes\n3 -> Massas")
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        if sugest == 1:
            print("Buscando os melhores vinhos para carnes!")
            cursor.execute("SELECT nome,tipo,winery,safra,preco,quantidade,fornecedor,nota FROM estoque WHERE id IN (3,4,5) AND ativo = 1")
            result = cursor.fetchall()
            for i in result:
                    nome, tipo, winery, safra, preco, qtd, fornecedor, nota = i
                    print(f"-> {nome} ({safra}) - R${preco:.2f} | Nota Vivino: {nota} | Estoque: {qtd}")
        elif sugest == 2:
            print("Buscando os melhores vinhos para peixes!")
            cursor.execute("SELECT nome,tipo,winery,safra,preco,quantidade,fornecedor,nota FROM estoque WHERE id IN (6,7,8) AND ativo = 1")
            result = cursor.fetchall()
            for i in result:
                    nome, tipo, winery, safra, preco, qtd, fornecedor, nota = i
                    print(f"-> {nome} ({safra}) - R${preco:.2f} | Nota Vivino: {nota} | Estoque: {qtd}")
        elif sugest == 3:
            print("Buscando os melhores vinhos para peixes!")
            cursor.execute("SELECT nome,tipo,winery,safra,preco,quantidade,fornecedor,nota FROM estoque WHERE id IN (9,10,11) AND ativo = 1")
            result = cursor.fetchall()
            for i in result:
                    nome, tipo, winery, safra, preco, qtd, fornecedor, nota = i
                    print(f"-> {nome} ({safra}) - R${preco:.2f} | Nota Vivino: {nota} | Estoque: {qtd}")
    except mysql.connector.Error as e:
        print(f"Erro o banco de dados: {e}")
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()