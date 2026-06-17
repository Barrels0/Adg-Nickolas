import sqlite3,os #navega em outros arquivos
from force import force_str,force_float,force_int,bsc_id
from dotenv import load_dotenv #carregar oq tem no ENV, procura no projeto o .env puxa as info de lá
def adicionar_item():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = ""
    search = force_str("Digite o nome do vinho!")
    params = {
        "search": search
        "page": 1
    }
    
    while True:
        print("\n----- CADASTRAR NOVA BEBIDA --------")
        novo_nome = force_str("Digite o nome da bebida: ").lower()
        novo_tipo = force_str("Digite o tipo da bebida: ").lower()
        nova_safra = force_int("Digite a safra da bebida: ")
        novo_preco = force_float("Digite o preço dessa bebida: ").replace(",", ".")
        nova_quantidade = force_int("Qual o estoque dessa bebida: ")
        novo_fornecedor = force_str("Qual o fornecedor dessa bebida: ").lower()
        nota = force_int("Qual a nota dessa bebida: ")

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
        novo_fornecedor = force_str("Digite o nome do novo fornecedor: ").lower()
        fornecedor_pais = force_str("Digite o país do fornecedor: ").lower()
        fornecedor_cidade = force_str("Digite a cidade do fornecedor: ").lower()
        fornecedor_estado = force_str("Digite o estado do fornecedor: ").lower()
        try:
            fornecedor_qualidade = force_int("Digite a qualidade do fornecedor (1-bom, 2-regular, 3-ruim): ")
            
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
        novo_usuario = force_str("Digite o nome de usuário: ")

        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (novo_usuario,))
            resultado = cursor.fetchone()
        
        if resultado is not None:
            print("Esse nome de usuário já existe, tente novamente!\n")
            continue
        
        # Se chegou aqui, o nome é inédito!
        senha = force_str("Crie uma senha: ")

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
        usuario = force_str("Digite o seu nome: ")
        senha = force_str("Digite sua senha: ")
        
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
                opcao = force_int("Você deseja tentar o login de novo (1) ou criar conta (2): ")
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
        id_produto = bsc_id()
        
        if id_produto == 0 or id_produto is None:
            print("Retornando ao menu anterior! ")
            break
        
        try:
            with sqlite3.connect("adegas123.db") as conexao:
                cursor = conexao.cursor()

                cursor.execute("SELECT nome FROM estoque WHERE id = ? AND ativo = 1", (id_produto,))
                bebida = cursor.fetchone()

                if not bebida:
                    print("ERRO: Bebida não encontrada ou já foi desativado.")
                    continue

                print("(Digite 0 pra cancelar e voltar ao menu)")
                confirmar = force_str(f"Tem certeza que deseja excluir a bebida '{bebida[0]}'? (Historico de vendas sera mantido. (s/n:) )").lower()

                if confirmar == '0' or confirmar == "n":
                    print("operação cancelada! ")
                    break

                if confirmar == 's':
                    cursor.execute("UPDATE estoque SET ativo = 0 WHERE id = ?", (id_produto,))
                    conexao.commit()
                    print("Bebida desativado do catalago com sucesso!!!!!")
                    break
                else:
                    print("Opção inválida. Digite 's' para sim ou 'n' para não.")
                    continue
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")
            conexao.rollback()
            break

def corrigir_nome():
    id_alvo = bsc_id()   
    nome_correto = force_str("Digite o nome correto do sorvete: ").lower()
    try:
        with sqlite3.connect("adegas.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                UPDATE estoque
                SET nome = ?
                WHERE id = ?           
                        """,(nome_correto,id_alvo))
            if cursor.rowcount > 0:
                print("Nome alterado com sucesso!")
            else:
                print("Nenhum produto encontrado!")
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        conexao.rollback
