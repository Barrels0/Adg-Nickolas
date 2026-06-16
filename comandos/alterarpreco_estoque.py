import sqlite3

def alteracoes():
    while True:
        try:
            alteracao = (
                input(
                    "\nVocê deseja alterar o preço ou repor estoque (digite 'preço' ou 'estoque'): "
                )
                .strip()
                .lower()
            )

            if alteracao == "preço" or alteracao == "preco":
                print("\n----- ALTERAR PREÇO --------")
                try:
                    id_venda = int(input("Digite o [ID] do produto: "))
                    
                    with sqlite3.connect("adegas123.db") as conexao:
                        cursor = conexao.cursor()
                        cursor.execute("SELECT nome, preco FROM estoque WHERE id = ?", (id_venda,))
                        bebida = cursor.fetchone()

                    # VALIDAÇÃO: Se o banco retornou None, o ID digitado não existe na tabela
                    if not bebida:
                        print("ERRO: Bebida não encontrada no banco de dados!")
                        continue 

                    # separa os valores vindos pelo select usando os seus indices
                    nome_bebida = bebida[0]
                    preco_atual = bebida[1]

                    novo_preco = int(input(
                        f"Atualizar o preço da bebida {nome_bebida} (PREÇO ATUAL: R${preco_atual}): "
                    ))
                    
                    preco_atual = novo_preco

                    with sqlite3.connect("adegas123.db") as conexao:    
                        cursor = conexao.cursor()
                        # CORREÇÃO: Usamos UPDATE para modificar o registro existente, filtrando pelo ID
                        cursor.execute("""
                            UPDATE estoque 
                            SET preco = ? 
                            WHERE id = ?
                        """, (preco_atual, id_venda))
                        
                        conexao.commit()
                        print(f"\Alteração feita com sucesso! '{nome_bebida}' agora custa R${preco_atual}.")
                        break

                except ValueError:
                    print("ERRO: Digite valores numéricos válidos!")

            elif alteracao == "estoque":
                print("\n----- REPOR ESTOQUE --------")
                
                try:
                    id_venda = int(input("Digite o [ID] do produto: "))
                    
                    with sqlite3.connect("adegas123.db") as conexao:
                        cursor = conexao.cursor()
                        cursor.execute("SELECT nome, quantidade FROM estoque WHERE id = ?", (id_venda,))
                        bebida = cursor.fetchone()

                    # VALIDAÇÃO: Se o banco retornou None, o ID digitado não existe na tabela
                    if not bebida:
                        print("ERRO: Bebida não encontrada no banco de dados!")
                        continue 

                    # separa os valores vindos pelo select usando os seus indices
                    nome_bebida = bebida[0]
                    quantidade_atual = bebida[1]

                    quantidade_adicional = int(input(
                        f"Quantidade para adicionar ao {nome_bebida.title()} (Atual: {quantidade_atual}): "
                    ))
                    
                    quantidade_atual += quantidade_adicional

                    with sqlite3.connect("adegas123.db") as conexao:    
                        cursor = conexao.cursor()
                        # CORREÇÃO: Usamos UPDATE para modificar o registro existente, filtrando pelo ID
                        cursor.execute("""
                            UPDATE estoque 
                            SET quantidade = ? 
                            WHERE id = ?
                        """, (quantidade_atual, id_venda))
                        
                        conexao.commit()
                        print(f"\nReposição feita com sucesso! '{nome_bebida}' agora tem {quantidade_atual} unidades.")
                        break

                except ValueError:
                    print("ERRO: Digite valores numéricos válidos!")
        except ValueError:
            print("Digite um valor correspondente ao que foi solicitado!")
            continue
