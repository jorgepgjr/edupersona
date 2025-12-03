import spade
from spade_llm import LLMAgent, LLMProvider, ChatAgent

async def main():
    spade_server = "localhost"

    # Create an LLM provider
    # Ollama (local)
    provider = LLMProvider.create_ollama(
        # model="llama3.1:8b",
        model="gemma3:1b",
        base_url="http://localhost:11434/v1"
    )

    # Create the LLM agent (using SPADE's built-in server)
    llm_agent = LLMAgent(
        jid="assistant@localhost",
        password="password123",
        provider=provider,
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