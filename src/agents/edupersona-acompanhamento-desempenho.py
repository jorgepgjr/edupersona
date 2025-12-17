"""
EduPersona

É uma solução de sistemas multi-agentes que auxiliam na melhoria do acompanhamento escolar, 
avaliando o desempenho, sugerindo material e motivando o aluno na evolução dos seus estudos.

PRÉ-REQUISITOS:
1. Iniciar SPADE built-in server em um outro terminal:
   spade run

2. Instalar dependências presentes em requirements.txt:
   pip install -r requirements.txt

"""

import os
import csv
import spade
from typing import Dict, Any

import mysql.connector
from mysql.connector import Error

from spade_llm.agent import LLMAgent, ChatAgent
from spade_llm.routing import RoutingResponse
from spade_llm.providers import LLMProvider
from spade_llm.tools import LLMTool
from spade_llm.guardrails.base import Guardrail, GuardrailResult, GuardrailAction


# 1. INFORMAÇÕES DA CONEXÃO
DB_HOST = '127.0.0.1' # Ou o endereço IP do seu servidor MySQL
DB_DATABASE = 'edupersona' # Altere para o nome do seu banco de dados
DB_USER = 'user' # Altere para seu usuário MySQL
DB_PASSWORD = 'pass' # Altere para sua senha MySQL

# 2. INFORMAÇÕES DO ARQUIVO COM OS OBJETOS DE APRENDIZAGEM
NOME_ARQUIVO = './adm-educacional/objetos-de-aprendizagem/oa.csv'

# 3. PROMPTS DOS AGENTES
COMUNICATING_PROMPT = """Você é um agente de interface para interação em uma ferramenta de apoio pedagógico.
As mensagens do usuário podem ser redirecionadas para dois agentes possíveis.
Se o usuário perguntar sobre avaliação, desempenho, estudo ou aprendizado deverá ser direcionado ao agente avaliador de desempenho.
Se o usuário perguntar sobre recomendação de objetos de aprendizagem, deverá ser direcionado ao agente tutor.
Todas as respostas devem ser redirecionadas para o usuário com clareza, de forma educada e buscando motivar o usuário a 
proseguir em seus estudos.

Seu fluxo de trabalho:
1. Identifique se a pergunta é sobre desempenho escolar ou recomendação de objetos de aprendizagem.
2. Se for sobre o desempenho escolar, identifique qual a matrícula do aluno para que seja avaliado seu desempenho (pergunte ao usuário se não for especificado).
  2.1 Use a Tool de consulta de desempenho para recuperar os dados
3. Se for sobre recomendação de objetos de aprendizagem, identifique sobre qual disciplina o usuário deseja recomendação.

Formato de resposta:
<<Para perguntas sobre desempenho escolar>>
<EVALUATING_PROMPT>
=== DESEMPENHO DO ALUNO DE MATRÍCULA: [MATRICULA] ===

Nome do aluno: [name]
Disciplinas:
[listas de disciplinas que ele está matrículado]
Notas nas atividades:
[lista com o nome das disciplinas, Tipo, Peso, ValorNota e Frequencia]

<<Para perguntas sobre objetos de aprendizagem>>
<TUTOR_PROMPT>
=== RECOMENDAÇÃO DE OBJETOS DE APRENDIZAGEM PARA DISCIPLINA: [DISCIPLINA] ===
Nome da disciplina:
Lista de tipos de objetos de aprendizagem que agradam o usuário:
[Identifique pela mensagem do usuário o tipo de objeto de aprendizagem que ele prefere, como:
- Documento
- Estudo de Caso
- Exemplo de Código
- Fórum
- Infográfico
- Jogo
- Laboratório
- Quiz
- Simulação
- Vídeo
]
"""

EVALUATING_PROMPT= """Você é um especialista pedagógico. Você recebe um conjunto de informações
de um determinado aluno e deve fazer uma avaliação pedagógica elaborando por meio das notas e frequência
uma estratégia para melhorar o desempenho do aluno. Você enviará as informações para o tutor para que seja
elaborado uma estratégia de estudos baseado nos objetos de aprendizagem disponíveis no centro de ensino.

Seu fluxo de trabalho:
1. Receba os dados completos das notas do aluno do Comunicating agent.
2. Escreva a situação em que o aluno se encontra nas disciplinas recebidas
3. Escreva uma estratégia para melhorar o desempenho nas disciplinas
4. Envie para o agente Tutor a lista com o nome das disciplinas, sem repetição, seguido de uma breve descrição se o aluno precisa de recomendação de objetos de aprendizagem

Importante:
- A faixa de desempenho por avaliação é:
  - Nota menor igual a 5: Classificação baixa (sugestão de materiais introdutórios; conteúdos fundamentais; glossários de conceitos; recursos de passo a passo.)
  - Nota entre 5 e 7,4: Classificação regular (sugestão de materiais de reforço; revisões estruturadas; exemplos contextualizados; quizzes diagnósticos.)
  - Nota entre 7,5 e 8,9: Classificação alta (sugestão de materiais intermediários e avançados; estudos de caso; materiais de aplicação prática; simulações; resolução de problemas contextualizados.)
  - Nota maior igual a 9: Classificação excelente (sugestão de materiais avançados e aprofundados; projetos práticos; problemas complexos.)
- A frequência aceita deve ser maior de 70. 
- Se comunique com clareza, de forma educada e buscando motivar o usuário a proseguir em seus estudos

Formato da resposta:
=== AVALIAÇÃO DO ALUNO ===
Situação: [situação]
Estratégia: [estrategia]
Lista de disciplinas que precisa de Objetos de Aprendizagem:
[lista com o nome das disciplinas, sem repetição, seguido de uma breve descrição se o aluno precisa de recomendação de objetos de aprendizagem]
"""

TUTOR_PROMPT = """

Seu fluxo de trabalho:
1. Receba os dados completos da avaliação do aluno do Evaluating agent ou a solicitação de um objeto de aprendizagem do Comunicating agent.
2. Use a Tool de consulta de oa para recuperar a lista de Objetos de Aprendizagem disponíveis na instituição
3. Escreva um relatório apontando os objetos de aprendizado selecionados, baseado na lista recebida pelo evaluationg agent ou do comunicating agent.
4. Adicione no fim da resposta recebida do agente anterior, o relatório produzido.

Importante:
- Se comunique com clareza, de forma educada e buscando motivar o usuário a proseguir em seus estudos
- Deixe o nome dos Objetos de aprendizagem em negrito.
- Faça uma breve descrição sobre cada objeto de aprendizagem recomendado.

Formato da resposta:
<<Para perguntas sobre desempenho escolar>>
=== AVALIAÇÃO DO ALUNO ===
Situação: [situação]
Estratégia: [estrategia]
Lista de Objetos de Aprendizagem:
[lista com nome do Objeto de aprendizagem - breve descrição do que se trata - porque foi recomendado]

<<Para perguntas sobre objetos de aprendizagem>>
=== RECOMENDAÇÃO DE OBJETOS DE APRENDIZAGEM PARA DISCIPLINA: [DISCIPLINA] ===
[lista com nome do Objeto de aprendizagem - breve descrição do que se trata - porque foi recomendado]
"""

class ComunicatingOnlyGuardrail(Guardrail):
    """Guardrail com estrutura que permitirão perguntas ao sistema."""
    
    def __init__(self, name: str = "chat_only_filter", enabled: bool = True):
        super().__init__(name, enabled, "Não posso lhe ajudar com essa questão. O sistema se propõe a realizar buscas de materiais didáticos e/ou conteúdos que possam lhe ajudar no seu processo de aprendizagem. Faça uma nova pergunta.")
        self.comunicating_keywords = [
            "desempenho", "nota", "melhorar", "recomendação de material", "frequência", 
            "aprovação", "estudos", "aprendizado", "atividades", "provas",
            "objetos de aprendizagem", "disciplina", "conteúdo", "videoaula", "estudo de caso",
            "quiz", "simulação", "laboratório", "infográfico", "jogo"
        ]
    
    async def check(self, content: str, context: Dict[str, Any]) -> GuardrailResult:
        content_lower = content.lower()

        if any(keyword in content_lower for keyword in self.comunicating_keywords):
            return GuardrailResult(
                action=GuardrailAction.PASS,
                content=content,
                reason="Pergunta relacionada ao sistema"
            )
        else:
            return GuardrailResult(
                action=GuardrailAction.BLOCK,
                content=self.blocked_message,
                reason="Pergunta não atende ao objetivo do sistema"
            )

# 4. DEFINIÇÃO DAS FUNÇÕES QUE SERÃO UTILIZADAS COMO TOOLS
async def get_disciplines(matricula: int) -> list:
    conexao = None
    try:
      conexao = mysql.connector.connect(
        host=DB_HOST,
        database=DB_DATABASE,
        user=DB_USER,
        password=DB_PASSWORD
      )
      if conexao.is_connected():
        print("✅ Conexão bem-sucedida ao banco de dados.")
        cursor = conexao.cursor()
        consulta_sql = """
          SELECT concat(al.Nome," ",al.Sobrenome) as name, 
          d.Nome as discipline,
          a.Tipo, 
          a.Peso, 
          a.ValorNota,
          m.Frequencia
          from Avaliacao a	
          INNER JOIN Matricula m on a.ID_Matricula = m.ID_Matricula
          INNER JOIN Aluno al on al.ID_Aluno = m.ID_Aluno
          INNER JOIN Turma t on t.ID_Turma = m.ID_Turma
          INNER JOIN Disciplina d on d.ID_Disciplina= t.ID_Disciplina
          WHERE al.ID_Aluno = %(matricula)s
          order by t.ID_Turma
        """
        cursor.execute(consulta_sql,{'matricula':matricula})
        registros = cursor.fetchall()
        return registros
    except Error as e:
      print(f"❌ Erro ao conectar ou consultar o MySQL: {e}")

    finally:
      # 6. Fechar a conexão
      if conexao is not None and conexao.is_connected():
        conexao.close()
        print("\n✔️ Conexão fechada.")

async def get_oa() -> list:
  """Retorna os objetos de aprendizagem disponíveis"""
  if not os.path.exists(NOME_ARQUIVO):
      print(f"❌ Erro: O arquivo '{NOME_ARQUIVO}' não foi encontrado no diretório atual.")
      print("Certifique-se de que o arquivo está no mesmo local que o script Python ou forneça o caminho completo.")
  else:
      try:
          with open(NOME_ARQUIVO,mode='r',encoding='utf-8') as arquivo_csv:
              leitor_csv = arquivo_csv.readlines()
              return leitor_csv
      except Exception as e:
          print(f"❌ Ocorreu um erro inesperado: {e}")

def review_router(msg, response, context):
    """Rotas para identificar se o caminho será para avaliação do aluno ou para recomendação de objetos de aprendizagem"""
    response_upper = response.upper()

    domain = str(msg.sender).split('@')[1]

    if "<TUTOR_PROMPT>" in response_upper:
        return RoutingResponse(recipients=[f"tutor@{domain}"])
    else:
        return RoutingResponse(recipients=[f"evaluating@{domain}"])


async def main():

  print("=== EduPersona - Sistema de acompanhamento de desempenho ===")

  # XMPP server configuration - using default SPADE settings
  xmpp_server = "localhost"
  print("🌐 Using SPADE built-in server")

  # Configuração da credencial dos agentes
  agents_config = {
      "comunicating": (f"comunicating@{xmpp_server}", "Agente de Comunicação"),
      "evaluating": (f"evaluating@{xmpp_server}", "Agente de Avaliação"),
      "tutor": (f"tutor@{xmpp_server}", "Agente de Tutoria"),
      "human": (f"human@{xmpp_server}", "Agente Humano")
  }  

  passwords = {}
  for role in agents_config.keys():
      passwords[role] = f"{role}_pass"
  print("✓ Using auto-registration with built-in server")

    # Create an LLM provider
  # Ollama (local)
  
  #provider = LLMProvider.create_ollama(
  #  model="llama3.1:8b",
    #model="gemma3:1b",
  #  base_url="http://localhost:11434/v1",
  #  timeout=180.0
  #)
  

  provider = LLMProvider.create_openai(
    api_key="<OPENAI_API_KEY>",
    model="gpt-4o-mini",
    temperature=0.7
  )
  
  input_guardrails = [ComunicatingOnlyGuardrail()]

  # TOOLs que serão usados pelas agentes
  print("Criando Tools")
    
  consulta_notas = LLMTool(
    name="consulta_notas",
    description="Recupera a nota de um aluno de acordo com a sua matrícula",
    parameters={
        "type": "object",
        "properties": {
          "matricula": {"type": "integer", "description": "matricula do aluno"}
        },
        "required": ["matricula"]
    },
    func=get_disciplines
  )
  
  consulta_oa = LLMTool(
    name="consulta_oa",
    description="Recupera os objetos de aprendizagem presentes na base de dados",
    parameters={
        "type": "object",
        "properties": {},
   #     "properties": {
   #        "disciplinas": {"type": "integer", "description": "lista de disciplinas passadas para retornar os oa"}
   #     },
   #     "required": ["disciplinas"]
    },
    func=get_oa
  )
  
  print("Criando Agents")
  agents = {}

  agents["tutor"] = LLMAgent(
    jid=agents_config["tutor"][0],
    password=passwords["tutor"],
    provider=provider,
    tools=[consulta_oa],
    reply_to=agents_config["human"][0],
    #system_prompt="Faça uma recomendação de estudo"
    system_prompt=TUTOR_PROMPT,
  )

  agents["evaluating"] = LLMAgent(
    jid=agents_config["evaluating"][0],
    password=passwords["evaluating"],
    provider=provider,
    reply_to=agents_config["tutor"][0],
    #system_prompt="Avalie as notas passadas"
    system_prompt=EVALUATING_PROMPT,
  )

  agents["comunicating"] = LLMAgent(
    jid=agents_config["comunicating"][0],
    password=passwords["comunicating"],
    provider=provider,
    input_guardrails=input_guardrails,
    routing_function=review_router,
    tools=[consulta_notas],
    reply_to=agents_config["evaluating"][0],
    #system_prompt="Se comunique de forma clara e pegue a matrícula"
    system_prompt=COMUNICATING_PROMPT,
  )

  agents["human"] = ChatAgent(
    jid=agents_config["human"][0],
    password=passwords["human"],
    target_agent_jid=agents_config["comunicating"][0],
    #display_callback=display_callback
  )

  try:
     # Start all agents
    print("\n🚀 Starting all agents...")
    porta_inicial = 10000
    for name, agent in agents.items():
      await agent.start()
      agent.web.start(hostname="127.0.0.1", port=str(porta_inicial))
      porta_inicial += 1
      print(f"✅ {name.capitalize()} agent started")

    print("\n" + "=" * 70)
    print("=== EDUPERSONA - SISTEMA DE ACOMPANHAMENTO DE DESEMPENHO ===")
    print("=" * 70)
    print("\nFluxo: Agente de Comunicação → Agente de Avaliação → Agente de Tutoria")
    print("\n📝 INSTRUÇÕES DE USO:")
    print("• Informe sua matrícula e pergunte sobre o seu desempenho, ou")
    print("• Peça recomendação de objetos de aprendizagem para uma disciplina específica.")
    print("• Type 'exit' to quit")

    print("-" * 70)

    # Run interactive workflow
    await agents["human"].run_interactive(
        input_prompt="Faça sua pergunta> ",
        exit_command="exit",
        response_timeout=600.0  # Longer timeout for complex processing
    )

    # Stop all agents
    print("\n🔄 Stopping all agents...")
    for name, agent in agents.items():
        await agent.stop()
        print(f"✅ {name.capitalize()} agent stopped")

    print("\n👋 Sempre que precisar, estamos a disposição.")

  except KeyboardInterrupt:
      print("\n👋 Shutting down...")
  finally:
    for name, agent in agents.items():
      await agent.stop()
      print(f"✅ {name.capitalize()} agent stopped")

if __name__ == "__main__":
    spade.run(main())