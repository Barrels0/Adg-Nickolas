# Importa o módulo nativo do Python para trabalhar com o banco de dados SQLite
import sqlite3 

# Define a função que vai preparar o banco de dados
def inicializar_banco():
    
    # Abre (ou cria) o arquivo 'adegas123.db'. O 'with' garante que a conexão feche sozinha se houver erro.
    with sqlite3.connect('adegas123.db') as conexao:

        # O cursor é o objeto que usamos para enviar comandos SQL e ler os resultados do banco
        cursor = conexao.cursor()
        
        # Cria a tabela 'estoque' caso ela ainda não exista no arquivo

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horarios TEXT NOT NULL,
            id_bebida INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            fornecedor TEXT NOT NULL,
            safra INTEGER NOT NULL,
            preco REAL NOT NULL,
            valor REAL NOT NULL,
            pagamento TEXT NOT NULL,
            FOREIGN KEY (id_bebida) REFERENCES estoque (id)
        )
            """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            fornecedor TEXT NOT NULL,
            safra INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            nota INTEGER NOT NULL,
            ativo INTEGER DEFAULT 1
        )
            """)

        # Faz uma contagem de quantas linhas existem na tabela estoque
        cursor.execute("SELECT COUNT(*) FROM estoque")
        
        # fetchone() pega o resultado da contagem. Se o primeiro valor '[0]' for igual a 0, a tabela está vazia.
        if cursor.fetchone()[0] == 0:
            
            # Uma lista contendo os dados dos primeiros vinhos para cadastrar
            bebidas_iniciais = [
            ("Casillero del Diablo", "Tinto", "Concha y Toro", 2016, 15, 250.0, 5),
            ("Angelica Zapata", "Tinto", "Catena Zapata", 2019, 15, 230.0, 5) 
            ]

            # executemany roda o INSERT para cada item da lista acima. 
            # As interrogações (?) são substitutos seguros para os dados da lista.
            cursor.executemany("""
                INSERT INTO estoque (nome, tipo, fornecedor, safra, quantidade, preco, nota)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, bebidas_iniciais)
            
            # Confirma e salva as alterações de inserção permanentemente no banco
            conexao.commit()

# Chama a função para o código ser executado de fato
inicializar_banco()