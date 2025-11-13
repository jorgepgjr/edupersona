# src/agentes/tutor.py
import spade
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template

# O "filtro" de mensagens que este agente vai escutar
TEST_TEMPLATE = Template(
    metadata={"performative": "inform", "ontology": "test_ontology"}
)

class TutorAgent(Agent):
    """
    Agente Tutor - Neste exemplo, ele apenas escuta e printa.
    """

    class ListenBehaviour(CyclicBehaviour):
        """
        Behaviour que roda em loop, esperando por mensagens 
        que batam com o TEST_TEMPLATE.
        """
        async def run(self):
            print(f"[{self.agent.name}] Aguardando mensagem...")
            
            # Espera assincronamente por uma mensagem (com timeout de 10s)
            msg = await self.receive(timeout=10) 
            
            if msg:
                print(f"\n*** [{self.agent.name}] MENSAGEM RECEBIDA! ***")
                print(f"    De: {msg.sender}")
                print(f"    Corpo: {msg.body}")
                print(f"    Metadados: {msg.metadata}")
            else:
                print(f"[{self.agent.name}] Nenhuma mensagem recebida.")

    async def setup(self):
        print(f"Agente Tutor {self.jid} iniciando e pronto para ouvir.")
        # Adiciona o Behaviour ao agente, filtrando pelo template
        b = self.ListenBehaviour()
        self.add_behaviour(b, template=TEST_TEMPLATE)