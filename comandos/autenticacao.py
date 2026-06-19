from othrs.force import force_str, force_int
from othrs.connectsql import obter_conexao
import mysql.connector


def criar_usuario():
    print("\n------- CRIAR CONTA ----- ")

    while True:
        novo_usuario = force_str("Digite o nome de usuário: ")

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT usuario FROM usuarios WHERE usuario = %s", (novo_usuario,)
            )
            resultado = cursor.fetchone()

            if resultado is not None:
                print("Esse nome de usuário já existe, tente novamente!\n")
                continue

            senha = force_str("Crie uma senha: ")
        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            break
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO usuarios (senha, usuario)
                VALUES (%s, %s)
            """,
                (senha, novo_usuario),
            )
            conexao.commit()

            print("Conta criada com sucesso!")
            break
        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            break
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()


def logar_conta():
    while True:
        print("\n--- LOGIN ---")
        usuario = force_str("Digite o seu nome: ")
        senha = force_str("Digite sua senha: ")

        conexao = obter_conexao()
        cursor = conexao.cursor()
        try:
            cursor.execute(
                "SELECT usuario, senha FROM usuarios WHERE usuario = %s AND senha = %s",
                (usuario, senha),
            )
            dados = cursor.fetchone()

            if dados is not None:
                print("Login realizado com sucesso!")
                return usuario
            else:
                print("Usuário ou senha incorretos!")
                try:
                    opcao = force_int(
                        "Você deseja tentar o login de novo (1) ou criar conta (2): "
                    )
                    if opcao == 1:
                        continue
                    else:
                        criar_usuario()
                        continue
                except ValueError:
                    print("Opção inválida. Tentando login novamente.")
                    continue
        except mysql.connector.Error as e:
            conexao.rollback()
            print(f"Ocorreu um erro: {e}")
            break
        finally:
            if "conexao" in locals() and conexao.is_connected():
                cursor.close()
                conexao.close()
