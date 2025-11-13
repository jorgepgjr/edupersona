# src/agentes/evaluator.py
import spade
import asyncio
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

# O JID (ID Jabber) do agente para o qual queremos enviar
# Deve ser o mesmo JID que definimos no main.py
TUTOR_JID = "tutor@localhost"

class EvaluatorAgent(Agent):
    """
    Agente Evaluator - Neste exemplo, ele apenas envia uma mensagem
    para o Tutor e encerra (o behaviour).
    """

    class SendTestBehaviour(OneShotBehaviour):
        """
        Behaviour que roda apenas uma vez para enviar a mensagem.
        """
        async def run(self):
            print(f"[{self.agent.name}] Behaviour de envio iniciado.")
            
            # Aguarda 5 segundos para garantir que o TutorAgent 
            # já esteja online e conectado.
            await asyncio.sleep(5) 
            
            print(f"[{self.agent.name}] Enviando mensagem para {TUTOR_JID}...")

            # 1. Cria a mensagem
            msg = Message(to=TUTOR_JID)
            
            # 2. Define o conteúdo
            msg.body = "Olá Tutor, aqui é o Evaluator! (Teste de mensagem)"
            
            # 3. Define os metadados (para bater com o template do Tutor)
            msg.set_metadata("performative", "inform")
            msg.set_metadata("ontology", "test_ontology")

            # 4. Envia
            await self.send(msg)
            print(f"[{self.agent.name}] Mensagem enviada com sucesso.")

    async def setup(self):
        print(f"Agente Evaluator {self.jid} iniciando...")
        # Adiciona o Behaviour de envio único
        self.add_behaviour(self.SendTestBehaviour())