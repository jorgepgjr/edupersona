# src/main.py

import asyncio
from agents.tutor import TutorAgent
from agents.evaluator import EvaluatorAgent

# Configurações de Conexão
# Estamos usando 'localhost' porque o Docker está rodando na nossa máquina
XMPP_SERVER = "localhost" 
PASSWORD = "senha_de_teste" # Pode ser qualquer senha

async def main():
    
    print("Iniciando Agente Tutor...")
    tutor_agent = TutorAgent(f"tutor@{XMPP_SERVER}", PASSWORD)
    # auto_register=True é o que permite o agente se criar no servidor
    await tutor_agent.start(auto_register=True) 

    print("Iniciando Agente Evaluator...")
    eval_agent = EvaluatorAgent(f"evaluator@{XMPP_SERVER}", PASSWORD)
    await eval_agent.start(auto_register=True)

    print("\n*** Agentes iniciados e rodando! ***")
    print("O Evaluator tentará enviar uma mensagem em 5 segundos.")
    print("Observe o terminal do Tutor. (Pressione Ctrl+C para parar)")

    try:
        # Mantém o script rodando para que os agentes possam trabalhar
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Encerrando agentes...")
        await tutor_agent.stop()
        await eval_agent.stop()
        print("Agentes parados.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Execução interrompida.")