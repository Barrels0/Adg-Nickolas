from othrs.force import force_str
from othrs.connectsql import obter_conexao
import mysql.connector
def teste_qualidade(id_produto):
    print("\n" + "="*20)
    print("---- TESTE DE QUALIDADE (AVALIAÇÃO) ----")
    print("="*20)
    
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "SELECT fornecedor,nota FROM estoque WHERE id = %s",(id_produto,)
            )
        resultados = cursor.fetchall()
        cursor.execute("SELECT * FROM fornecedores")#usa em outras operações!
        fornecedor = cursor.fetchall()

        if not resultados:
            return False

        nota_produto = resultados[0][1]
        nome_fornecedor = resultados[0][0]
    except mysql.connector.Error as e:
        conexao.rollback()
        print(f"Ocorreu um erro: {e}")
        return
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
    
    status_fornecedor = "Não cadastrado"
    
    #Busca a qualidade do fornecedor dessa bebida específico
    for bebida in fornecedor:
        if bebida[1].strip().lower() == nome_fornecedor.strip().lower():
            if bebida[2] == 1: status_fornecedor = "Bom"
            elif bebida[2] == 2: status_fornecedor = "Regular"
            elif bebida[2] == 3: status_fornecedor = "Ruim"

    if nota_produto == 5:
        print(f"Produto excelente (Nota 5)! Fornecedor associado: {nome_fornecedor.title()} (Status: {status_fornecedor}).")
    elif nota_produto == 4:
        print(f"Produto bem avaliado (Nota 4). Fornecedor associado: {nome_fornecedor.title()} (Status: {status_fornecedor}).")
    elif nota_produto == 3:
        print(f"Produto com avaliação regular (Nota 3). Pode conter pequenas variações.")
    elif nota_produto == 2:
        print(f"ATENÇÃO: Produto mal avaliado (Nota 2). Avaliando a remoção do catálogo.")
    else:
        print(f"PERIGO: Produto péssimo (Nota 1). A adega não se responsabiliza por defeitos!")

    confirmacao = force_str("\nDeseja prosseguir com a compra deste item? (S/N): ").upper()
    
    if confirmacao == "S":
        print("-> Qualidade aceita pelo cliente. Prosseguindo...")
        return True
    else:
        print("-> Operação cancelada pelo cliente por critérios de qualidade.")
        return False