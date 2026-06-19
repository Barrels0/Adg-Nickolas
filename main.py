import mysql.connector
from othrs.connectsql import obter_conexao

from comandos.banco_dados import inicializar_banco
from comandos.interface import exibir_menu_e_estoque, continuar_sistema
from comandos.caixa import registar_venda, nota_fiscal, exportar_relatorio_txt
from comandos.estoque import adicionar_item, desativar_bebida,corrigir_nome, reativar_bebida, alteracoes, sugestoes
from comandos.marketing import add_cupom, adicionar_fornecedor, promocoes, ranking_cupons
from comandos.autenticacao import logar_conta, criar_usuario
from comandos.relatorios import busca, painel_produtomaisvendido, ranking_vendas, catalogo_ordenado,relatorios_expresso, filtros
from othrs.force import force_int, vrf_user

inicializar_banco()

print("Iniciando meu sistema de vinhos...")

print("Vinhos encontrados com sucesso!")

# Apenas o histórico de vendas foi mantido aqui se você precisar dele
conexao = obter_conexao()
cursor = conexao.cursor()
try:
    cursor.execute("SELECT * FROM vendas")
    historico_vendas = cursor.fetchall()
    cursor.execute("SELECT * FROM usuarios")
    contas = cursor.fetchall()
except mysql.connector.Error as e:
         conexao.rollback()
         print(f"Ocorreu um erro: {e}")
finally:
    if 'conexao' in locals() and conexao.is_connected():
        cursor.close()
        conexao.close()

print("""Seja bem vindo a adega Nickolas!
          1-Criar conta
          2-Fazer Login""")
escolha = force_int("Selecione um dos dois itens mostrados acima: ")


if escolha == 1:
    criar_usuario()
    user_ativ = logar_conta()
elif escolha == 2:
    user_ativ = logar_conta()
else:
    print("Escolha uma opção valida!")
while True:
    conexao = obter_conexao()
    cursor = conexao.cursor()

    conexao = obter_conexao()
    cursor = conexao.cursor()
    try:
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
    except mysql.connector.Error as e:
         conexao.rollback()
         print(f"Ocorreu um erro: {e}")
         break
    finally:
        if 'conexao' in locals() and conexao.is_connected():
            cursor.close()
            conexao.close()

    exibir_menu_e_estoque(caixa)

    comando = force_int("Digite o [ID] do menu que você deseja acessar: ")

    if comando == 0:
        print(f"Obrigado por visitar nossa loja o caixa total ficou em R${caixa:.2f}")
        exit()

    # --- VENDAS E CAIXA ---
    elif comando == 1:
        registar_venda()
        continuar_sistema()
    elif comando == 2:
        nota_fiscal()
        continuar_sistema()
    elif comando == 3:
        exportar_relatorio_txt()
        continuar_sistema()

    # --- PRODUTOS E ESTOQUE ---
    elif comando == 4:
        if vrf_user(user_ativ):
            adicionar_item()
        continuar_sistema()
    elif comando == 5:
        if vrf_user(user_ativ):
            alteracoes() # Repor Estoque
        continuar_sistema()
    elif comando == 6:
        if vrf_user(user_ativ):
            alteracoes() # Alterar Preço
        continuar_sistema()
    elif comando == 7:
        if vrf_user(user_ativ):
            corrigir_nome()
        continuar_sistema()
    elif comando == 8:
        if vrf_user(user_ativ):
            desativar_bebida()
        continuar_sistema()
    elif comando == 9:
        if vrf_user(user_ativ):
            reativar_bebida()
        continuar_sistema()
    elif comando == 10:
        sugestoes()
        continuar_sistema()

    # --- CONSULTAS E RELATÓRIOS ---
    elif comando == 11:
        busca()
        continuar_sistema()
    elif comando == 12:
        relatorios_expresso()
        continuar_sistema()
    elif comando == 13:
        ranking_vendas() # Historico
        continuar_sistema()
    elif comando == 14:
        catalogo_ordenado()
        continuar_sistema()
    elif comando == 15:
        filtros()
        continuar_sistema()
    elif comando == 16:
        painel_produtomaisvendido() # Estatísticas e Balanço
        continuar_sistema()

    # --- MARKETING E FORNECEDORES ---
    elif comando == 17:
        if vrf_user(user_ativ):
            promocoes()
        continuar_sistema()
    elif comando == 18:
        if vrf_user(user_ativ):
            adicionar_fornecedor()
        continuar_sistema()
    elif comando == 19:
        if vrf_user(user_ativ):
            add_cupom()
        continuar_sistema()
    elif comando == 20:
        if vrf_user(user_ativ):
            ranking_cupons()
        continuar_sistema()

