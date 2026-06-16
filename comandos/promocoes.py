
import sqlite3
from force import force_int,force_float,force_str,bsc_id
def promocoes():
    while True:    
            print("""---- MENU DE PROMOÇÕES ----
                1- Aplicar promoção em um item
                2- Aplicar promoção para todos os itens
                3- Aplicar promoção com base no tipo do item              
                        """)
            escolha_promo = force_int("\nEscolha uma opção: ")
            if escolha_promo == 1:
                         desconto = force_float("Porcentagem de desconto: ")
                         if 0 < desconto < 100:
                              fator_desconto = (100 - desconto) / 100
                         else:
                              print("Desconto inválido!")
                              return
                         id_produto = bsc_id
                         try:   
                            with sqlite3.connect("adegas123.db") as conexao:
                                cursor = conexao.cursor()
                                cursor.execute("UPDATE estoque SET preco = ROUND(preco * ?, 2) WHERE id = ?", (fator_desconto, id_produto,))
                                if cursor.rowcount > 0:
                                     print("Desconto aplicado com sucesso!")
                                else:
                                     print("Nenhuma produto foi alterado, verifique se o id existe!")
                         except sqlite3.Error as e:        
                            print(f"Erro ao acessar o banco de dados: {e}")
                            conexao.rollback()
                            break
                    
            elif escolha_promo == 2:
                    desconto = force_float("Porcentagem de desconto: ")
                    if 0 < desconto < 100:
                        fator_desconto = (100 - desconto) / 100
                    else:
                        print("Desconto inválido!")
                        return
                    with sqlite3.connect("adegas123.db") as conexao:
                         cursor = conexao.cursor()
                         cursor.execute("UPDATE estoque SET preco = ROUND(preco * ?, 2)",(fator_desconto,))
                         conexao.commit()
                         print("Desconto aplicado com sucesso!")
                         break
            elif escolha_promo == 3:
                tipo = force_str("Qual o tipo de bebida que você deseja adicionar um desconto (Ex: Vinho, Whisky): ").lower()
                try:
                    desconto = force_float("Porcentagem de desconto: ")
                    if 0 < desconto < 100:
                              fator_desconto = (100 - desconto) / 100
                    else:
                        print("Desconto inválido!")
                        return
                except ValueError:
                    print("ERRO: Porcentagem ou tipo são invalidos")
                    return
                
                with sqlite3.connect("adegas123.db") as conexao:
                    cursor = conexao.cursor()
                    cursor.execute("UPDATE estoque SET preco = ROUND(preco * ?, 2) WHERE LOWER(tipo) = ?",(fator_desconto,tipo))
                    conexao.commit()
                    print("Desconto aplicado com sucesso!")
                    break            

            else:
                print("Opção inválida!")
                continue
