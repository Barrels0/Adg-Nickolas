
import sqlite3
def promocoes():
    while True:    
            print("""---- MENU DE PROMOÇÕES ----
                1- Aplicar promoção em um item
                2- Aplicar promoção para todos os itens
                3- Aplicar promoção com base no tipo do item              
                        """)
            escolha_promo = int(input("\nEscolha uma opção: "))
            if escolha_promo == 1:
                    try:
                         desconto = float(input("Porcentagem de desconto: "))
                         if 0 < desconto < 100:
                              fator_desconto = (100 - desconto) / 100
                         else:
                              print("Desconto inválido!")
                              return
                         id_produto = int(input("Digite o [ID] da bebida: "))
                    except ValueError:
                         print("ERRO: Porcentagem ou ID são invalidos")
                         return
                    with sqlite3.connect("adegas123.db") as conexao:
                         cursor = conexao.cursor()
                         cursor.execute("UPDATE estoque SET preco = ROUND(preco * ?, 2) WHERE id = ?", (fator_desconto, id_produto,))
                         conexao.commit()
                         print("Desconto aplicado com sucesso!")
                         break
                    
            elif escolha_promo == 2:
                    desconto = float(input("Porcentagem de desconto: "))
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
                tipo = input("Qual o tipo de bebida que você deseja adicionar um desconto (Ex: Vinho, Whisky): ").strip().lower()
                try:
                    desconto = float(input("Porcentagem de desconto: "))
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
