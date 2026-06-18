import mysql.connector
from othrs.connectsql import obter_conexao
from othrs.force import force_str
def busca():
    print("\n----- PESQUISAR POR NOME/TIPO/FORNECEDOR -------")
    termo_busca = force_str("Digite o nome/tipo/fornecedor da bebida para busca:").lower()
    termo_com_curinga = f"%{termo_busca}%" #ele usa o "%" antes e depois pq ai ele pega tudo, por exemplo o nome é vinho e se o usuario digitar vin ele acha do mesmo jeito
    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:    
        cursor.execute(
                "SELECT nome,tipo,fornecedor,safra,preco,quantidade,nota FROM estoque WHERE ativo = 1 AND (LOWER(nome) LIKE %s OR LOWER(tipo) LIKE %s OR fornecedor LIKE %s)", (termo_com_curinga,termo_com_curinga,termo_com_curinga)
            )
        resultados = cursor.fetchall()
        if resultados:
            print("\nESSAS FORAM AS INFORMAÇÕES ENCONTRADAS:")
            print("-" * 60)
                
            for linha in resultados:
                nome, tipo, fornecedor, safra, preco, quantidade, nota = linha
                print(f"-> {nome} ({tipo}) | Safra: {safra} | Fornecedor: {fornecedor} | R$ {preco:.2f} | Estoque: {quantidade} | Nota: {nota}")
        else:
            print("Nenhuma bebida encontrada com esse nome/tipo/fornecedor!")
    except mysql.connector.Error as e:
        print(f"Erro ao realizar a busca no banco de dados: {e}")
        return
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()
        
    
                
    
    """for id_bebida, bebida in enumerate(estoque_atual):
            if termo_busca in bebida["nome"] or termo_busca in bebida["tipo"] or termo_busca in bebida["fornecedor"]:
                print(f"ESSAS FORAM AS INFORMAÇÕES ENCONTRADAS:[{id_bebida}] {bebida['nome']} ({bebida['tipo']}) | Safra: {bebida['safra']} | Fornecedor: {bebida['fornecedor']} | R$ {bebida['preco']:.2f} | Estoque: {bebida['quantidade']}")
                encontrou = True
    if not encontrou:
            print("Nenhuma bebida encontrada com esse nome/tipo/fornecedor! ")"""