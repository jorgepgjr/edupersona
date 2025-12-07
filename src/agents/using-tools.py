import spade
from spade_llm import LLMAgent, LLMProvider, ChatAgent, LLMTool
import mysql.connector
from mysql.connector import Error
import csv
import os # Importar para verificar se o arquivo existe

# ⚙️ Detalhes da Conexão
DB_HOST = '127.0.0.1' # Ou o endereço IP do seu servidor MySQL
DB_DATABASE = 'edupersona' # Altere para o nome do seu banco de dados
DB_USER = 'user' # Altere para seu usuário MySQL
DB_PASSWORD = 'pass' # Altere para sua senha MySQL

async def main():
    # TOOLs que serão usados pelas agentes
  print("Criando Tools")
  async def get_disciplines(matricula: int) -> list:
    """Conecta ao MySQL e executa uma consulta SELECT."""
    conexao = None
    try:
      # 1. Estabelecer a conexão
      conexao = mysql.connector.connect(
        host=DB_HOST,
        database=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD
      )
      if conexao.is_connected():
        print("✅ Conexão bem-sucedida ao banco de dados.")
        # 2. Criar um Cursor
        # O cursor é o objeto que permite executar comandos SQL
        cursor = conexao.cursor()
        # 3. Definir a consulta SQL
        consulta_sql = """
          SELECT d.Nome, a.Tipo, a.Peso, a.ValorNota, al.ID_Aluno, al.Nome, al.Sobrenome, m.Status, m.NotaFinal, m.Frequencia from Avaliacao a
          INNER JOIN Matricula m on a.ID_Matricula = m.ID_Matricula
          INNER JOIN Aluno al on al.ID_Aluno = al.ID_Aluno
          INNER JOIN Turma t on t.ID_Turma = m.ID_Turma
          INNER JOIN Disciplina d on d.ID_Disciplina= t.ID_Disciplina
          WHERE al.ID_Aluno = %(matricula)s
          ORDER BY d.Nome
        """
        # 4. Executar a consulta
        cursor.execute(consulta_sql,{'matricula':matricula})
        # 5. Buscar e Exibir os Resultados
        # fetchall() recupera todas as linhas do resultado
        registros = cursor.fetchall()
        # Exibir cabeçalhos (opcional, dependendo do driver)
        #colunas = [i[0] for i in cursor.description]
        #print(f"\nColunas: {colunas}")

        #print("\n--- Resultados da Consulta ---")
        return registros
        #for linha in registros:
            # Cada 'linha' é uma tupla (id, nome, preco)
          #   print(linha)
    except Error as e:
      print(f"❌ Erro ao conectar ou consultar o MySQL: {e}")

    finally:
      # 6. Fechar a conexão
      if conexao is not None and conexao.is_connected():
        conexao.close()
        print("\n✔️ Conexão fechada.")
    
  
  consulta_notas = LLMTool(
    name="consulta_notas",
    description="Recupera a nota de um aluno de acordo com a sua matrícula",
    parameters={
        "type": "object",
        "properties": {
            "matricula": {"type": "int", "description": "matricula do aluno"}
        },
        "required": ["matricula"]
    },
    func=get_disciplines
  )

  async def get_oa() -> list:
    """Retorna os objetos de aprendizagem disponíveis"""
    # 📌 Nome do arquivo CSV que você quer ler
    nome_arquivo = 'adm-educacional/objetos-de-aprendizagem/oa.csv'
    print("Entrou na Tool de Objetos de Aprendizagem")
    # 1. Verificar se o arquivo existe antes de tentar ler
    if not os.path.exists(nome_arquivo):
        print(f"❌ Erro: O arquivo '{nome_arquivo}' não foi encontrado no diretório atual.")
        print("Certifique-se de que o arquivo está no mesmo local que o script Python ou forneça o caminho completo.")
    else:
        try:
            with open(nome_arquivo,mode='r',encoding='utf-8') as arquivo_csv:
               leitor_csv = csv.reader(arquivo_csv)
               return leitor_csv
        except Exception as e:
            print(f"❌ Ocorreu um erro inesperado: {e}")
  
  consulta_oa = LLMTool(
    name="consulta_oa",
    description="Recupera os objetos de aprendizagem presentes na base de dados",
    parameters={
        "type": "object",
        "properties": {
        },
        "required": []
    },
    func=get_oa
  )
  
  print("Criando Agents")
  spade_server = "localhost"

  # Create an LLM provider
  # Ollama (local)
  provider = LLMProvider.create_ollama(
      model="llama3.1:8b",
      #model="gemma3:1b",
      base_url="http://localhost:11434/v1"
  )

  # Create the LLM agent (using SPADE's built-in server)
  llm_agent = LLMAgent(
      jid=f"assistant@{spade_server}",
      password="password123",
      provider=provider,
      tools=[consulta_notas, consulta_oa],
      system_prompt="You are a helpful assistant.",
  )

  # Create the chat agent for user interaction
  chat_agent = ChatAgent(
      jid=f"user@{spade_server}",
      password="user_pass",  # Simple password for built-in server
      target_agent_jid=f"assistant@{spade_server}",
  )

  try:
      # Start both agents
      await llm_agent.start()
      await chat_agent.start()

      print("✅ Agents started successfully!")
      print("💬 You can now chat with your AI assistant")
      print("Type 'exit' to quit\n")

      # Run interactive chat
      await chat_agent.run_interactive()

  except KeyboardInterrupt:
      print("\n👋 Shutting down...")
  finally:
      # Clean up
      await chat_agent.stop()
      await llm_agent.stop()
      print("✅ Agents stopped successfully!")

if __name__ == "__main__":
    spade.run(main())