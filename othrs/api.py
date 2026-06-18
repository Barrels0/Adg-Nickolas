import requests,os
from dotenv import load_dotenv



load_dotenv()
api_key = os.getenv("API_KEY")
url = "https://api.wineapi.io/wines/search"


def buscar_vinho(vinho_busca:str) -> list[dict]:
    if not vinho_busca.strip():
        print("Erro: O nome do vinho não pode ser vazio.")
        return None

    headers = {
        "X-API-Key": api_key
    }

    # O 'requests' vai pegar esses dados e colocar no final da URL de forma perfeita
    parametros = {
        "q": vinho_busca
    }
    
    response = requests.get(url, params=parametros, headers=headers)
    
    if response.status_code == 200:
            dados = response.json()
            lista_vinho = dados.get("results", [])
            return lista_vinho
    else:
        print("ERRO: ", response.status_code)
        return [{}]