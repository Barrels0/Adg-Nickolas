import sqlite3
with sqlite3.connect() as conexao:   
    if estoque_atual == 0:
        cursor.execute("""
        UPDATE flores
        SET ativo = 0
        WHERE id = ?
        """,(5,))
        conexao.commit()
        print("Flor esgotada e foi desativada!")
    else:
        print("Flor ainda esta disponivel!")

if resultado is None:
    print("ID inválido")
else:
    print(f"{resultado[0]}")

if preco_maximo is None:
    cursor.execute("""
       SELECT especie, preco
       FROM flores""")
    resultado = cursor.fetchall()
    for flor in resultado:
      print(f"Nome: {flor[0]}\n")
else:
    cursor.execute("""
       SELECT especie, preco
       FROM flores
       WHERE preco <= ?""",(preco_maximo,))
    resultado = cursor.fetchall()
    print(f"Flores até R${preco_maximo:.2f}")
    for flor in resultado:
      print(f"Nome: {flor[0]}\n")

      def vender_buque_casal():
    try:
        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            
            print("Iniciando a venda do Buquê Casal...")
            
            cursor.execute("""
                UPDATE flores 
                SET quantidade = quantidade - 1 
                WHERE id = 1
            """)
            
            cursor.execute("""
                UPDATE flores 
                SET quantidade = quantidade - 1 
                WHERE id = 2
            """)
            
            conexao.commit()
            print("Venda realizada! Estoque de Rosas e Cravos atualizado com sucesso.")

    except sqlite3.Error as erro:
        print(f"Erro no banco de dados: {erro}")
        print("Cancelando operação e desfazendo qualquer alteração parcial...")
        
        conexao.rollback()

cursor.execute("UPDATE flores SET quantidade = quantidade + 10 WHERE ativo = 1")

cursor.execute("SELECT quantidade, ativo FROM flores WHERE id = 8")
resultado = cursor.fetchone()
if resultado is None:
    print("Flor não existe no sistema")
else:   
    quantidade = resultado[0]
    ativo = resultado[1]
    if ativo == 0:
        print("Flor desativada sistema")

    elif quantidade < 5:
        print("Quantidade insuficiente!")

    else:
        cursor.execute("UPDATE flores SET quantidade = quantidade - 5 WHERE id = 8")
        print("Compra realizada com sucesso!")
        conexao.commit()

