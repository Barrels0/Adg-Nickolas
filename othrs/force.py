#USAR O BSC_ID EM TUDO!!!!!!!!!
from othrs.connectsql import obter_conexao
import mysql.connector
def force_int(message: str) -> int:
     while True:
          try:
               return int(input(message))
          except:
               print("Digite um numero inteiro valido")
               continue

def force_float(message: str) -> float:
     while True:
          try:
               return float(input(message))
          except:
               print("Digite um numero valido")
               continue

def force_str(message: str) -> str:
     while True:
          try:
               return str(input(message)).strip()
          except:
               print("Digite uma string valida")
               continue

def bsc_id(mensagem="Digite o [ID] do produto: ") -> int:
    while True:   
        try:
            id_venda = force_int(mensagem)
        except ValueError:
            print("ERRO: O ID deve ser um número inteiro!")
            continue

        conexao = obter_conexao()
        cursor = conexao.cursor()
        
        try:
            cursor.execute("SELECT id FROM estoque WHERE id = %s AND ativo = 1", (id_venda,))
            bebida_encontrada = cursor.fetchone()
            
            if not bebida_encontrada:
                print("ERRO: ID INVÁLIDO. Essa bebida não existe no sistema.")
                continue
            
            return id_venda
            
        except mysql.connector.Error as e:
            print(f"Erro no banco de dados: {e}")
            break 
        finally:
            cursor.close()
            conexao.close()


def vrf_user(usuario_ativo):
    if usuario_ativo == 'Chefe': 
        print("Autorização concedida!")
        return True
    else:
        print("Você é um cliente e não pode acessar essa funcionalidade!")
        return False