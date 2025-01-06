import pg8000
from InquirerPy import prompt

# Parametros de configuração do banco de dados

db_config = {
    "database": "teste_python",
    "user": "postgres",
    "password": "my_password", # troquei para nao ter que passar a senha do db
    "host": "localhost",
    "port": 5432
}

# Realiza a conexão entre o banco de dados e o programa

def conectar_banco():
 try:
  conn = pg8000.connect(**db_config)
  print("Conexao bem sucedida!")
  return conn
 except Exception as e:
    print(f"Erro ao conectar com o banco de dados {e}")
    exit()
      
    
def exibir_produto(produto):
    if produto:
     print(f"""
        Produto {produto[0]}
        Nome: {produto[1]}
        Preco: {produto[2]}
        Quantidade: {produto[3]}
        Categoria: {produto[4]}   
        """)
    else:
      print("Produto nao encontrado!")
 
      
def adicionar_produto(cursor):
  try:
    nome_produto = input("Digite o nome do produto que voce deseja inserir:")
    preco_produto = float(input("Digite o preco do produto:"))
    quantidade_produto = int(input("Digite a quantidade do produto a ser inserido:"))
    categoria_produto = input("Digite a categoria do produto: ")
    cursor.execute(
            "INSERT INTO produto (nome, preco, quantidade, categoria) VALUES (%s, %s, %s, %s)",
            (nome_produto, preco_produto, quantidade_produto, categoria_produto)
        )
    print("Produto inserido com sucesso!")
  except Exception as e:
   print(f"Erro ao adicionar produto: {e}")
   
   
def remover_produto(cursor):
  try:
    produto_a_remover = input("Digite o nome do produto que voce deseja remover:")
    cursor.execute("SELECT * FROM produto WHERE nome = %s", (produto_a_remover,))
    produto = cursor.fetchone()
    exibir_produto(produto)
    pergunta_delete = [
        {
            "type":"list",
            "name":"opcao_delete",
            "message":"TEM CERTEZA QUE VOCE DESEJA EXCLUIR ESSE PRODUTO",
            "choices":["Sim","Nao"]
        }
     ]
    resposta_delete = prompt(pergunta_delete)
    escolha_delete = resposta_delete["opcao_delete"]
    if escolha_delete == "Sim":
      cursor.execute("DELETE FROM produto WHERE nome = %s",(produto_a_remover),)
      print("Produto removido!")
    else:
      print("Produto nao removido!")
  except Exception as e:
    print(f"Erro ao remover produto: {e}")
 
    
def selecionar_produto(cursor):
    try:
     produto_a_selecionar = input("Digite o nome do produto que voce deseja selecionar:")
     if produto_a_selecionar.lower() == "todos":
       cursor.execute("SELECT * FROM produto")
       produtos = cursor.fetchall()
       for produto in produtos:
           exibir_produto(produto)
     else:
      cursor.execute("SELECT * FROM produto WHERE nome = %s", (produto_a_selecionar,))
      produto = cursor.fetchone()
      exibir_produto(produto)   
    except Exception as e:
     print(f"Erro ao exibir produto: {e}")
     
def alterar_produto(cursor):
    try:
     produto_a_alterar = input("Digite o nome do produto que voce deseja selecionar:")
     cursor.execute("SELECT * FROM produto WHERE nome = %s", (produto_a_alterar,))
     produto = cursor.fetchone()
     if produto:
         pergunta_alterar = [
        {
            "type":"list",
            "name":"action",
            "message":"O que voce deseja alterar no produto?",
            "choices":["Nome","Preco","Quantidade","Categoria"]
        }
     ]
         resposta_alterar = prompt(pergunta_alterar)
         escolha = resposta_alterar["action"]
         novo_valor = input("Insira o valor a ser alterado:")
         if escolha == "Preco":
             novo_valor = float(novo_valor)
         elif escolha == "Quantidadade":
             novo_valor = int(novo_valor)
         cursor.execute(f"UPDATE produto SET {escolha} = %s WHERE nome = %s",(novo_valor,produto_a_alterar),)
         print("Produto alterado com sucesso!")            
     else:
         print("Produto nao encontrado!")          
    except Exception as e:
      print(f"Erro ao alterar produto: {e}")
     

def main():
    conn = conectar_banco()
    cursor = conn.cursor()
    pergunta_crud = [
        {
            "type":"list",
            "name":"opcao_crud",
            "message":"O que voce deseja fazer?",
            "choices":["Adicionar","Alterar","Selecionar","Remover","Sair do programa"]
        },
    ]   
    while True:      
     res_crud = prompt(pergunta_crud)
     escolha_crud = res_crud["opcao_crud"]
     if escolha_crud == "Adicionar":
         adicionar_produto(cursor)
     elif escolha_crud == "Alterar":
         alterar_produto(cursor)
     elif escolha_crud == "Selecionar":
         selecionar_produto(cursor)
     elif escolha_crud == "Remover":
         remover_produto(cursor)
     elif escolha_crud == "Sair do programa":
         print("Encerrando programa...")
         break
     
    conn.commit()
    cursor.close()
    conn.close()
    print("Conexao Encerrada!")
    
# Se o arquivo nao for estanciado por outro arquivo, executa a função main por aqui mesmo

if __name__ == "__main__":
    main()
      

