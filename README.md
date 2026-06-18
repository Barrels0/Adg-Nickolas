# 🍷 Adega Nickolas - Sistema de Gerenciamento de Estoque e Vendas

Um sistema robusto e completo desenvolvido em **Python** e integrado com **MySQL** para o gerenciamento inteligente de uma adega de vinhos finos. O sistema oferece desde o controle rigoroso de estoque e fluxo de caixa até relatórios estatísticos complexos e exportação de fechamentos em tempo real.

---

## 🚀 Funcionalidades Principais

* **🔐 Autenticação e Segurança:** Sistema de criação de contas e login de usuários para proteger as operações da adega.
* **📦 Gestão de Estoque Inteligente:** Cadastro de vinhos com informações detalhadas (safra, vinícola, fornecedor, preço e classificação), ajuste dinâmico de preços, controle de quantidade e desativação lógica de produtos (soft delete).
* **🛒 Registro de Vendas Blindado:** Processamento de vendas integrado ao banco de dados com validação em tempo real de IDs, cálculo automático de quantidade, valor total e formas de pagamento.
* **📊 Painel Estatístico & Balanço:** Cálculo automatizado de faturamento bruto, ticket médio por venda e identificação do produto campeão de vendas diretamente via queries agrupadas no MySQL.
* **📈 Ranking de Mais Vendidos:** Ordenação automatizada dos produtos mais populares da loja do maior para o menor.
* **⚠️ Alertas de Estoque Baixo:** Relatório expresso que lista automaticamente produtos com menos de 3 unidades disponíveis para reposição.
* **🔍 Filtros Avançados:** Busca de bebidas por nome e filtros dinâmicos por limite de preço máximo definido pelo cliente.
* **💾 Exportação de Relatórios:** Geração automática de arquivos `.txt` com o fechamento do caixa e histórico detalhado das vendas do dia, contendo carimbo de data e hora (`Timestamp`).

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Banco de Dados:** MySQL (com conector nativo `mysql-connector-python`)
* **Ferramenta de Administração:** DBeaver (para monitoramento e gerenciamento do banco de dados)

---

## 🏗️ Arquitetura do Projeto

O projeto adota uma estrutura modular organizada e limpa, facilitando a manutenção de cada funcionalidade:

```text
├── main.py                          # Ponto de entrada do sistema (Loop Principal do Menu)
├── connectsql.py                    # Configuração e gerenciamento de conexão com o MySQL
├── comandos/
│   ├── banco_dados.py               # Criação automatizada de tabelas e inserções iniciais (DML/DDL)
│   ├── interface.py                 # Renderização de menus gráficos e catálogos na tela
│   ├── novoitem.py                  # Cadastro de produtos, fornecedores e usuários
│   ├── alterarpreco_estoque.py      # Atualização de preços e quantidades no banco
│   ├── pesquisa_nome.py             # Lógica de buscas textuais no estoque
│   ├── promocoes.py                 # Gestão de descontos e campanhas promocionais
│   ├── registrar_venda.py           # Processamento e persistência de vendas no banco
│   └── resultado_relatorio.py       # Funções anal
