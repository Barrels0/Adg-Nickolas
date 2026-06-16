import sqlite3
from force import force_int

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
    with sqlite3.connect("adegas123.db") as conexao:
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
        with sqlite3.connect("adegas123.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT nome,preco,quantidade FROM estoque")
            resultados = cursor.fetchall()

        if ordem == 1:
            estoque_ordenado = sorted(resultados, key=lambda bebida: bebida[0].lower())
        elif ordem == 2:
            estoque_ordenado = sorted(resultados, key=lambda bebida: bebida[1])
        elif ordem == 3:
            estoque_ordenado = sorted(
                resultados, key=lambda bebida: bebida[1], reverse=True
            )
        elif ordem == 4:
            estoque_ordenado = sorted(resultados, key=lambda bebida: bebida[2])
        elif ordem == 5:
            estoque_ordenado = sorted(
                resultados, key=lambda bebida: bebida[2], reverse=True
            )
        else:
            print("Opção inválida")
            return exibir_menu_e_estoque

        for bebida in estoque_ordenado:
            nome, preco, quantidade = bebida
            print(f"- {nome} - R${preco:.2f} (Qtd: {quantidade})")
        break
