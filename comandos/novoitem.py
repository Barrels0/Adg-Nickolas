import sqlite3


def adicionar_item():
    while True:
        print("\n----- CADASTRAR NOVA BEBIDA --------")
        novo_nome = input("Digite o nome da bebida: ").strip().lower()
        novo_tipo = input("Digite o tipo da bebida: ").strip().lower()
        nova_safra = int(input("Digite a safra da bebida: "))
        novo_preco = float(input("Digite o preço dessa bebida: ").replace(",", "."))
        nova_quantidade = int(input("Qual o estoque dessa bebida: "))
        novo_fornecedor = input("Qual o fornecedor dessa bebida: ").strip().lower()
        nota = int(input("Qual a nota dessa bebida: "))

        if nova_quantidade < 0 or novo_preco < 0 or nota < 0 or (nota > 5 and nota < 0):
            print("ERRO: RESPOSTA INVÁLIDA (Valores negativos ou nota fora de 0-5)")
            continue
        else:
            with sqlite3.connect("adegas123.db") as conexao:
                cursor = conexao.cursor()
                cursor.execute(
                    """
                    INSERT INTO estoque(nome,tipo,safra,preco,quantidade,fornecedor,nota)
                    VALUES (?,?,?,?,?,?,?)
                """,
                    (
                        novo_nome,
                        novo_tipo,
                        nova_safra,
                        novo_preco,
                        nova_quantidade,
                        novo_fornecedor,
                        nota,
                    )
                )  # isso pode ser uma def
                conexao.commit()
            print(f"Bebida '{novo_nome}' foi salvo com sucesso! ")
            break


def adicionar_fornecedor():
    while True:
        print("\n----- NOVO FORNECEDOR --------")
        novo_fornecedor = input("Digite o nome do novo fornecedor: ").strip().lower()
        fornecedor_pais = input("Digite o país do fornecedor: ").strip().lower()
        fornecedor_cidade = input("Digite a cidade do fornecedor: ").strip().lower()
        fornecedor_estado = input("Digite o estado do fornecedor: ").strip().lower()
        try:
            fornecedor_qualidade = int(
                input("Digite a qualidade do fornecedor (1-bom, 2-regular, 3-ruim): ")
            )
            if fornecedor_qualidade < 1 or fornecedor_qualidade > 3:
                print("ERRO: Qualidade deve ser entre 1 e 3!")
                continue
        except ValueError:
            print("ERRO: Digite um número inteiro válido para a qualidade!")
            continue

        # Adiciona o dicionário na lista 'fornecedor' que foi declarada no topo do arquivo
        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute(
                """
                    INSERT INTO fornecedores(nome,pais,cidade,estado,qualidade)
                    VALUES (?,?,?,?,?)
                """,
                (
                    novo_fornecedor,
                    fornecedor_pais,
                    fornecedor_cidade,
                    fornecedor_estado,
                    fornecedor_qualidade
                ),
            )  # isso pode ser uma def
            conexao.commit()
            print(f"O fornecedor '{novo_fornecedor}' foi salvo com sucesso! ")
            break

    """fonecedores.append(
            {
                "nome": novo_fornecedor,
                "pais": fornecedor_pais,
                "cidade": fornecedor_cidade,
                "estado": fornecedor_estado,
                "qualidade": fornecedor_qualidade,
            }
        )
        salvar_arquivo("fornecedores.json", fonecedores)
        print(f"O fornecedor '{novo_fornecedor}' foi adicionado com sucesso!")
        break"""


def criar_usuario():
    print("\n------- CRIAR CONTA ----- ")

    while True:
        novo_usuario = input("Digite o nome de usuário: ").strip()

        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (novo_usuario,))
            resultado = cursor.fetchone()
        
        if resultado is not None:
            print("Esse nome de usuário já existe, tente novamente!\n")
            continue
        
        # Se chegou aqui, o nome é inédito!
        senha = input("Crie uma senha: ").strip()

        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                INSERT INTO usuarios (senha, usuario)
                VALUES (?, ?)
            """, (senha, novo_usuario))
            conexao.commit() 
            
        print("Conta criada com sucesso!")
        break 


def logar_conta():
    while True:
        print("\n--- LOGIN ---")
        usuario = input("Digite o seu nome: ").strip()
        senha = input("Digite sua senha: ").strip()
        
        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            # Buscamos combinando usuário E senha direto no banco para maior segurança
            cursor.execute("SELECT usuario, senha FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
            dados = cursor.fetchone()
            
        if dados is not None:
            print("Login realizado com sucesso!")
            break
        else:
            print("Usuário ou senha incorretos!")
            try:
                opcao = int(input("Você deseja tentar o login de novo (1) ou criar conta (2): "))
                if opcao == 1:
                    continue
                else:
                    criar_usuario()
                    continue
            except ValueError:
                print("Opção inválida. Tentando login novamente.")
                continue

        """for id_usuario, login in enumerate(usuarioss):
            if usuario in login["usuario"] and senha in login["senha"]:
                print("Login realizado com sucesso!")
                encontrou = True
            break
        if not encontrou:
            print("Senha ou usuario incorretos!")
            return criar_usuario"""
def desativar_bebida():
    while True:    
        print("\n=======DESATIVAR BEBIDA DO CATALÓGO (Soft delete)========")
        try:
            id_produto = int(input("Digite o [ID] da bebida(Ou 0 pra voltar ao menu): "))
        except ValueError:
            print("ERRO: O ID deve ser um número.")
            return
        
        if id_produto == 0:
            break
        
        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()

            cursor.execute("SELECT nome FROM estoque WHERE id = ? AND ativo = 1", (id_produto,))
            bebida = cursor.fetchone()

            if not bebida:
                print("ERRO: Bebida não encontrada ou já foi desativado.")
                return

            print("(Digite 0 pra cancelar e voltar ao menu)")
            confirmar = input(f"Tem certeza que deseja excluir a bebida '{bebida[0]}'? (Historico de vendas sera mantido. (s/n:) )").strip().lower()

            if confirmar == '0':
                break

            if confirmar == 's':
                cursor.execute("UPDATE estoque SET ativo = 0 WHERE id = ?", (id_produto,))
                conexao.commit()
                print("Bebida desativado do catalago com sucesso!!!!!")
                break
            else:
                continue
import sqlite3
def corrigir_nome():
    try:
        id_alvo = int(input("Digite o [ID] que você deseja alterar: "))
    except ValueError:
        print("Digite um ID valido")
        return
    nome_correto = input("Digite o nome correto do sorvete: ").strip()
    with sqlite3.connect("adegas.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            UPTADE estoque
            SET nome = ?
            WHERE id = ?           
                    """,(nome_correto,id_alvo))
        conexao.commit()
