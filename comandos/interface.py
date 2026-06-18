from othrs.force import force_int
from othrs.connectsql import obter_conexao
def exibir_menu_e_estoque(caixa_atual):
    """
    Função dedicada a imprimir o menu e o estoque
    """
    print(f"""
    ========================================================
                         ADEGA MARIO
                Caixa Acumulado: R${caixa_atual:.2f}
    ========================================================
    """)
    conexao = obter_conexao()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT nome,tipo,safra,preco,quantidade,fornecedor,nota,id FROM estoque"
    )
    resultados = cursor.fetchall()
    for bebida in resultados:
        nome, tipo, safra, preco, quantidade, fornecedor, nota, id = bebida
        print(
            f"[{id}] {nome} ({safra}) | Tipo: {tipo} | Fornecedor: {fornecedor} | Nota: {nota} | R$ {preco:.2f} | Estoque: {quantidade}"
        )

    """print("ACERVO DISPONÍVEL")
    for id_adega, adega in enumerate(estoque_atual):
        print(
            f"[{id_adega}] {adega['nome']} ({adega['safra']}) | Tipo: {adega['tipo']} | Autor: {adega} | R$ {adega['preco']:.2f} | Estoque: {adega['quantidade']}"
        )"""

    print("\n" + "=" * 60)
    print(f"{'MENU DE COMANDOS':^60}")
    print("=" * 60)
    print("  [1] Registrar Venda            [2] Cadastrar Nova Bebida")
    print("  [3] Alterar Preço              [4] Repor Estoque")
    print("  [5] Buscar por Nome            [6] Promoções")
    print("  [7] Nota Fiscal (Sessão)")
    print("  [8] Painel de Estatisticas e Balanço")
    print("  [9] Historico de vendas        [10] Novo Fornecedor")
    print("  [11] Relatorios Expresso       [12] Catalogo Ordenado")
    print("  [13] Filtro por preço")
    print("  [14] Alterar nome              [15] Desativar bebida")
    print("  [16] Exportar notinha")
    print("  [0] Sair do Sistema")
    print("=" * 60)


def catalogo_ordenado():
    while True:
        print("""
                \n-----CATALOGO ORDENADO-------
                1. Ordem alfabética
                2. Mais Barato Primeiro
                3. Mais Caros Primeiro
                4. Maior quantidade
                5. Menor quantidade
                """)
        ordem = force_int("Digite a maneira que você prefere organizar as bebidas: ")

        # sorted() > cria uma copia da lista que você selecionar, sem considerar o id
        #
        conexao = obter_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome,preco,quantidade FROM estoque")
        resultados = cursor.fetchall()

        query_base = "SELECT nome, preco, quantidade FROM livros WHERE ativo = 1"
        if ordem == 1:
            query_base = f"{query_base} ORDER BY LOWER(nome) ASC"
        elif ordem == 2:
            query_base = f"{query_base} ORDER BY preco ASC"
        elif ordem == 3:
            query_base = f"{query_base} ORDER BY preco DESC"
        elif ordem == 4:
            query_base = f"{query_base} ORDER BY quantidade DESC"
        elif ordem == 5:
            query_base = f"{query_base} ORDER BY quantidade ASC"
        else:
            conexao.close()
            cursor.close()
            print("Opção inválida")
            return exibir_menu_e_estoque

        conexao = obter_conexao()
        cursor = conexao.cursor()

        cursor.execute(query_base)
        estoque_ordenado = cursor.fetchall()

        for bebida in estoque_ordenado:
            nome, preco, quantidade = bebida
            print(f"- {nome} - R${preco:.2f} (Qtd: {quantidade})")
        conexao.close()
        cursor.close()
        break
