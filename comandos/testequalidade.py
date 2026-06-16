from force import force_str
import sqlite3
def teste_qualidade(id_produto):
    print("\n" + "="*20)
    print("---- TESTE DE QUALIDADE (AVALIAÇÃO) ----")
    print("="*20)
    
    with sqlite3.connect("adegas123.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT nome,fornecedor,nota FROM estoque WHERE id = ?",(id_produto,)
            )
        resultados = cursor.fetchall()
        cursor.execute("SELECT * FROM fornecedores")#usa em outras operações!
        fornecedor = cursor.fetchall()

    nota_produto = resultados[0][2]
    nome_fornecedor = resultados[0][1]
    
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