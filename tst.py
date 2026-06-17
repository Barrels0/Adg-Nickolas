if response.status_code == 200:
    dados = response.json()
    lista_vinhos = dados.get("results", [])
   
    for id_vinho,vinho in enumerate(lista_vinhos, 1):
       
        nome = vinho.get("name", "desconhecido") 
        tipo = vinho.get("type", "desconhecido")
        print(f"id:{id_vinho} | NOME: {nome} | tipo: {tipo}") 
    
    id = int(input("Coloque o id do vinho que quer salvar"))
    
    vinho_salvar = lista_vinhos[id - 1]
    
    print(f"Nome do vinho salvo: {vinho_salvar['name']}, tipo do vinho: {vinho_salvar['type']}")