import sqlite3
def force_int(message: str) -> int:
     while True:
          try:
               return int(input(message))
          except:
               print("Digite um numero inteiro valido")

def force_float(message: str) -> float:
     while True:
          try:
               return float(input(message))
          except:
               print("Digite um numero valido")

def force_str(message: str) -> str:
     while True:
          try:
               return str(input(message)).strip()
          except:
               print("Digite uma string valida")
def bsc_id() -> int:
     while True:   
        id_venda = force_int("Digite o [ID] do produto que você deseja: ")

        if id_venda in None:
             return id_venda
        try:
               with sqlite3.connect("adegas123.db") as conexao:
                  cursor = conexao.cursor()
                  cursor.execute("SELECT * FROM estoque WHERE id = ?",
                                 (id_venda,))
                  bebida_encontrada = cursor.fetchone()
               if not bebida_encontrada:
                  print("ERRO: ID INVÁLIDO. Essa bebida não existe no sistema.")
                  continue
               return bebida_encontrada
        except sqlite3.Error as e:
             print(f"Erro no banco de dados: {e}")
             conexao.rollback()
             return None