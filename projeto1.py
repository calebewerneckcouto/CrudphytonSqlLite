import sqlite3

# Classe Produto para manipulação de produtos
class Produto:
    def __init__(self, nome, descricao, quantidade, preco):
        self.nome = nome
        self.descricao = descricao
        self.quantidade = quantidade
        self.preco = preco

    def salvar_no_bd(self):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO produtos (nome, descricao, quantidade, preco) VALUES (?, ?, ?, ?)',
                       (self.nome, self.descricao, self.quantidade, self.preco))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_produtos():
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, descricao TEXT, quantidade INTEGER, preco REAL)')
        cursor.execute('SELECT * FROM produtos')
        produtos = cursor.fetchall()
        conn.close()
        return produtos

# Classe Venda para manipulação de vendas
class Venda:
    def __init__(self, id_produto, quantidade, data_venda):
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.data_venda = data_venda

    def registrar_venda(self):
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS vendas (id INTEGER PRIMARY KEY AUTOINCREMENT, id_produto INTEGER, quantidade INTEGER, data_venda DATE)')
        cursor.execute('INSERT INTO vendas (id_produto, quantidade, data_venda) VALUES (?, ?, ?)',
                       (self.id_produto, self.quantidade, self.data_venda))
        cursor.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?',
                       (self.quantidade, self.id_produto))
        conn.commit()
        conn.close()

# Funções para interação com o usuário
def cadastrar_produto():
    print("\nCadastro de Novo Produto")
    nome = input("Nome do Produto: ")
    descricao = input("Descrição: ")
    quantidade = int(input("Quantidade: "))
    preco = float(input("Preço: "))

    novo_produto = Produto(nome, descricao, quantidade, preco)
    novo_produto.salvar_no_bd()
    print("Produto cadastrado com sucesso!")

def realizar_venda():
    print("\nRegistro de Nova Venda")
    id_produto = int(input("ID do Produto vendido: "))
    quantidade = int(input("Quantidade vendida: "))
    data_venda = input("Data da Venda (YYYY-MM-DD): ")

    nova_venda = Venda(id_produto, quantidade, data_venda)
    nova_venda.registrar_venda()
    print("Venda registrada com sucesso!")

def listar_produtos():
    print("\nListagem de Produtos")
    produtos = Produto.listar_produtos()
    if produtos:
        print("ID | Nome | Descrição | Quantidade | Preço")
        for produto in produtos:
            print(f"{produto[0]} | {produto[1]} | {produto[2]} | {produto[3]} | R$ {produto[4]:.2f}")
    else:
        print("Nenhum produto encontrado.")

# Menu principal
def menu():
    while True:
        print("\n===== Sistema de Gerenciamento de Estoque =====")
        print("1. Cadastrar Novo Produto")
        print("2. Realizar Venda")
        print("3. Listar Produtos")
        print("4. Sair")
        opcao = input("Digite a opção desejada: ")

        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            realizar_venda()
        elif opcao == '3':
            listar_produtos()
        elif opcao == '4':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    menu()
