import spade
from spade_llm.tools import HumanInTheLoopTool
from spade_llm import LLMAgent, ChatAgent, LLMProvider


async def main():
    # Ollama (local)
  provider = LLMProvider.create_ollama(
      model="llama3.1:8b",
      #model="gemma3:1b",
      base_url="http://localhost:11434/v1"
  )

  # Create human consultation tool
  human_tool = HumanInTheLoopTool(
      human_expert_jid="expert_1@localhost",
      timeout=300.0,  # 5 minutes
      name="ask_human_expert",
      description="Ask human expert for current info or clarification"
  )

  # Create LLM agent with human tool
  # Note: Start SPADE server first: spade run
  agent = LLMAgent(
      jid="agent_1@localhost", 
      password="your_password",
      provider=provider,
      tools=[human_tool],
      system_prompt="""You are an AI assistant with access to a human expert.
      When you need current information, human judgment, or clarification,
      use the ask_human_expert tool."""
  )

  chat_agent = ChatAgent(
      jid="user_1@localhost",
      password="your_password", 
      target_agent_jid="agent_1@localhost"
  )

  try:
    await agent.start()
    await chat_agent.start()

    # Test questions that trigger human consultation
    await chat_agent.run_interactive()

  except KeyboardInterrupt:
      print("\n👋 Shutting down...")
  finally:
      # Clean up
      await chat_agent.stop()
      await agent.stop()
      print("✅ Agents stopped successfully!")

if __name__ == "__main__":
    spade.run(main())