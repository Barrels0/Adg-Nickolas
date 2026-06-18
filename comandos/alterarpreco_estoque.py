import mysql.connector
from othrs.connectsql import obter_conexao
from othrs.force import force_str,force_float,force_int
def alteracoes():
    while True:
        try:
            alteracao = force_str("\nVocê deseja alterar o preço ou repor estoque (digite 'preço' ou 'estoque'): ").lower()

            if alteracao == "preço" or alteracao == "preco":
                print("\n----- ALTERAR PREÇO --------")
                try:
                    id_venda = force_int("Digite o [ID] do produto: ")
                    
                    conexao = obter_conexao()
                    cursor = conexao.cursor()
                    try:    
                        cursor.execute("SELECT nome, preco FROM estoque WHERE id = %s", (id_venda,))
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
                        cursor.execute("""
                            UPDATE estoque 
                            SET preco = %s 
                            WHERE id = %s
                        """, (preco_atual, id_venda))
                            
                        conexao.commit()
                        print(f"\Alteração feita com sucesso! '{nome_bebida}' agora custa R${preco_atual}.")
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
                        if 'conexao' in locals() and conexao.is_connected():
                            conexao.close()
                            cursor.close() 
                except ValueError:
                    print("ERRO: Digite um valor válido!")

            elif alteracao == "estoque":
                print("\n----- REPOR ESTOQUE --------")
                
                try:
                    id_venda = force_int("Digite o [ID] do produto: ")
                    
                    conexao = obter_conexao()
                    cursor = conexao.cursor()
                    try:
                        cursor.execute("SELECT nome, quantidade FROM estoque WHERE id = %s", (id_venda,))
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
                        cursor.execute("""
                            UPDATE estoque 
                            SET quantidade = %s 
                            WHERE id = %s
                        """, (quantidade_atual, id_venda))
                            
                        conexao.commit()
                        print(f"\nReposição feita com sucesso! '{nome_bebida}' agora tem {quantidade_atual} unidades.")
                        break
                    except mysql.connector.Error as e:
                        conexao.rollback
                        print(f"Erro no bando de dados: {e}")
                        break
                    finally:
                        if 'conexao' in locals() and conexao.is_connected():
                            conexao.close()
                            cursor.close()

                except ValueError:
                    print("ERRO: Digite valores numéricos válidos!")
                    continue
        except ValueError:
            print("Digite um valor correspondente ao que foi solicitado!")
            continue
