import sqlite3
from comandos.banco_dados import inicializar_banco
from comandos.interface import exibir_menu_e_estoque, catalogo_ordenado
from comandos.novoitem import adicionar_item, adicionar_fornecedor,criar_usuario,logar_conta,desativar_bebida,corrigir_nome
from comandos.alterarpreco_estoque import alteracoes
from comandos.pesquisa_nome import busca
from comandos.promocoes import promocoes
from comandos.resultado_relatorio import ranking_vendas,nota_fiscal,painel_produtomaisvendido,continuar_sistema,relatorios_expresso,filtros

from comandos.registrar_venda import realizar_venda

inicializar_banco()

# Apenas o histórico de vendas foi mantido aqui se você precisar dele
with sqlite3.connect("adegas123.db") as conexao:
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM vendas")
    historico_vendas = cursor.fetchall()
    cursor.execute("SELECT * FROM usuarios")
    contas = cursor.fetchall()

print("""Seja bem vindo a adega Nickolas!
          1-Criar conta
          2-Fazer Login""")
escolha = int(input("Selecione um dos dois itens mostrados acima: "))

# CORREÇÃO: Chamadas limpas sem passar parâmetros (contas)
if escolha == 1:
    criar_usuario()
    logar_conta()
elif escolha == 2:
    logar_conta()
else:
    print("Escolha uma opção valida!")

while True:
    with sqlite3.connect("adegas123.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT SUM(valor) FROM vendas")
        resultado_caixa = cursor.fetchone()[0]
        caixa = resultado_caixa if resultado_caixa is not None else 0.0 

        cursor.execute("SELECT * FROM estoque")#usa em outras operações!
        estoque = cursor.fetchall()
        
        cursor.execute("SELECT * FROM vendas")
        historico_vendas = cursor.fetchall()

        cursor.execute("SELECT * FROM cupons")
        cupons = cursor.fetchall()

        cursor.execute("SELECT * FROM fornecedores")
        fornecedor = cursor.fetchall()

    exibir_menu_e_estoque(caixa)

    comando = int(input("Digite o [ID] do menu que você deseja acessar: "))

    if comando == 0:
        print(f"Obrigado por visitar nossa loja o caixa total ficou em R${caixa:.2f}")
        exit()

    elif comando == 1:
        realizar_venda()

    elif comando == 2:
        adicionar_item()
        continuar_sistema()
    elif comando == 3:
        alteracoes()
        continuar_sistema()
    elif comando == 4:
        alteracoes()
        continuar_sistema()
    elif comando == 5:
        busca()
        continuar_sistema()
    elif comando == 6:
        promocoes()
        continuar_sistema()

    elif comando == 7:
        nota_fiscal()
        continuar_sistema()

    elif comando == 8:
        painel_produtomaisvendido()
        continuar_sistema()
    elif comando == 9:
        ranking_vendas()
        continuar_sistema()

    elif comando == 10:
        adicionar_fornecedor()
        continuar_sistema()
    elif comando == 11:
        relatorios_expresso()
        continuar_sistema()
    elif comando == 12:
        catalogo_ordenado()
        continuar_sistema()
    elif comando == 13:
        filtros()
        continuar_sistema()
    elif comando == 14:
        corrigir_nome()
        continuar_sistema()
    elif comando == 15:
        desativar_bebida()
        continuar_sistema()

