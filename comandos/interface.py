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

    print("""
        ===================================================================
                            ══ MENU DE COMANDOS ══
        ===================================================================

        ┌── VENDAS E CAIXA ──────────────────────────────────────────────┐
        │ [1] Registrar Venda               [2] Nota Fiscal (Sessão)     │
        │ [3] Exportar Notinha                                           │
        └────────────────────────────────────────────────────────────────┘

        ┌── PRODUTOS E ESTOQUE ──────────────────────────────────────────┐
        │ [4] Cadastrar Nova Bebida         [5] Repor Estoque            │
        │ [6] Alterar Preço                 [7] Alterar Nome             │
        │ [8] Desativar Bebida              [9] Reativar Bebida          │
        │ [10] Sugestões (Harmonização)                                  │
        └────────────────────────────────────────────────────────────────┘

        ┌── CONSULTAS E RELATÓRIOS ──────────────────────────────────────┐
        │ [11] Buscar por Nome              [12] Relatórios Expresso     │
        │ [13] Histórico de Vendas          [14] Catálogo Ordenado       │
        │ [15] Filtro por Preço             [16] Estatísticas e Balanço  │
        └────────────────────────────────────────────────────────────────┘

        ┌── MARKETING E FORNECEDORES ────────────────────────────────────┐
        │ [17] Promoções                    [18] Novo Fornecedor         │
        │ [19] Adicionar Cupom              [20] Cupons Mais Utilizados  │
        └────────────────────────────────────────────────────────────────┘

        ┌────────────────────────────────────────────────────────────────┐
        │ [0] Sair do Sistema                                            │
        └────────────────────────────────────────────────────────────────┘
        ===================================================================
        """)
def continuar_sistema():
    while True:
        print("-"*10)
        print("[1] Continuar no Menu")
        print("[2] Voltar")
        print("-"*10)
        try:
            acao_pos_comando = force_int("Escolha uma ação: ")
            if acao_pos_comando == 1 or acao_pos_comando == 2:
                return
            else:
                print("Opção inválida!")
        except ValueError:
            return exibir_menu_e_estoque