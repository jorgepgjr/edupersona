import asyncio
import getpass
import os
import spade
import logging
from datetime import datetime
from typing import Dict, Any

from spade_llm.agent import LLMAgent, ChatAgent
from spade_llm.providers import LLMProvider
from spade_llm.mcp import StreamableHttpServerConfig
from spade_llm.guardrails.base import Guardrail, GuardrailResult, GuardrailAction
from spade_llm.tools import HumanInTheLoopTool
from spade_llm.utils import load_env_vars

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GitHubOnlyGuardrail(Guardrail):
    """Custom guardrail that only allows GitHub-related requests."""

    def __init__(self, name: str = "github_only_filter", enabled: bool = True):
        super().__init__(name, enabled, "I only help with GitHub-related requests. Please ask about issues, pull requests, or repository monitoring.")
        self.github_keywords = [
            "github", "issue", "issues", "pull request", "pr", "prs", 
            "repository", "repo", "commit", "branch", "merge", "review",
            "bug", "feature", "enhancement", "milestone", "project",
            "analyze", "monitor", "check", "status", "activity"
        ]

    async def check(self, content: str, context: Dict[str, Any]) -> GuardrailResult:
        """Check if content is GitHub-related."""
        content_lower = content.lower()

        if any(keyword in content_lower for keyword in self.github_keywords):
            return GuardrailResult(
                action=GuardrailAction.PASS,
                content=content,
                reason="GitHub-related request detected"
            )
        else:
            return GuardrailResult(
                action=GuardrailAction.BLOCK,
                content=self.blocked_message,
                reason="Non-GitHub request blocked"
            )

def create_github_guardrails():
    """Create input guardrails for GitHub-only requests."""
    return [GitHubOnlyGuardrail()]

def create_mcp_servers():
    """Create MCP server configurations."""

    # GitHub MCP server
    github_mcp = StreamableHttpServerConfig(
        name="GitHubMCP",
        url="https://your-mcp-server.com/github/endpoint",  # Replace with actual MCP server
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SPADE_LLM/1.0"
        },
        timeout=30.0,
        sse_read_timeout=300.0,
        terminate_on_close=True,
        cache_tools=True
    )

    # Notion MCP server
    notion_mcp = StreamableHttpServerConfig(
        name="NotionMCP",
        url="https://your-mcp-server.com/notion/endpoint",  # Replace with actual MCP server
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SPADE_LLM/1.0"
        },
        timeout=30.0,
        sse_read_timeout=300.0,
        terminate_on_close=True,
        cache_tools=True
    )

    # Gmail MCP server
    gmail_mcp = StreamableHttpServerConfig(
        name="GmailMCP",
        url="https://your-mcp-server.com/gmail/endpoint",  # Replace with actual MCP server
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SPADE_LLM/1.0"
        },
        timeout=30.0,
        sse_read_timeout=300.0,
        terminate_on_close=True,
        cache_tools=True
    )

    return github_mcp, notion_mcp, gmail_mcp

async def main():
    print("🚀 Advanced Multi-Agent GitHub Monitor System")
    print("=" * 60)

    # Load environment variables
    load_env_vars()

    # Get API keys
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key:
        openai_key = getpass.getpass("Enter your OpenAI API key: ")

    # Using SPADE's built-in server (recommended)
    print("🚀 Using SPADE's built-in server")
    print("Make sure you started it with: spade run")
    input("Press Enter when the server is running...")

    spade_server = "localhost"

    # Agent credentials
    agents_config = {
        "chat": (f"github_chat@{spade_server}", "GitHub Chat Interface"),
        "analyzer": (f"github_analyzer@{spade_server}", "GitHub Analyzer Agent"),
        "notion": (f"notion_manager@{spade_server}", "Notion Storage Agent"),
        "email": (f"email_manager@{spade_server}", "Email Manager Agent"),
        "human": (f"human_expert@{spade_server}", "Human Expert")
    }

    # Get passwords
    passwords = {}
    for role, (jid, label) in agents_config.items():
        passwords[role] = getpass.getpass(f"{label} password: ")

    # Create LLM provider
    provider = LLMProvider.create_openai(
        api_key=openai_key,
        model="gpt-4o-mini",
        temperature=0.7
    )

    # Create MCP servers
    print("\\n🔧 Configuring MCP servers...")
    github_mcp, notion_mcp, gmail_mcp = create_mcp_servers()

    # Create human-in-the-loop tool
    human_tool = HumanInTheLoopTool(
        human_expert_jid=agents_config["human"][0],
        timeout=300.0,  # 5 minutes
        name="ask_human_expert",
        description="Ask human expert for email sending confirmation and recipient details"
    )

    # Create guardrails
    input_guardrails = create_github_guardrails()

    # Create agents with structured message flow
    print("\\n🤖 Creating specialized agents...")

    # AGENT CONNECTION SETUP:
    # User → Chat Agent → Analyzer Agent → Notion Agent → Email Agent → Human Expert

    # 1. Chat Agent with Guardrails (Entry Point)
    # Receives user input and forwards to analyzer
    def display_response(message: str, sender: str):
        print(f"\\n🤖 GitHub Monitor: {message}")
        print("-" * 50)

    user_chat = ChatAgent(
        jid=agents_config["chat"][0],
        password=passwords["chat"],
        target_agent_jid=agents_config["analyzer"][0],  # → Sends to Analyzer Agent
        display_callback=display_response
    )

    # 2. GitHub Analyzer Agent (Data Collection & Analysis)
    # Receives from Chat Agent, uses GitHub MCP, forwards to Notion Agent
    analyzer_agent = LLMAgent(
        jid=agents_config["analyzer"][0],
        password=passwords["analyzer"],
        provider=provider,
        system_prompt=GITHUB_ANALYZER_PROMPT,
        input_guardrails=input_guardrails,
        mcp_servers=[github_mcp],  # Uses GitHub MCP for data collection
        reply_to=agents_config["notion"][0]  # → Forwards to Notion Agent
    )

    # 3. Notion Manager Agent (Storage & Forwarding)
    # Receives from Analyzer Agent, uses Notion MCP, forwards to Email Agent
    notion_agent = LLMAgent(
        jid=agents_config["notion"][0],
        password=passwords["notion"],
        provider=provider,
        system_prompt=NOTION_MANAGER_PROMPT,
        mcp_servers=[notion_mcp],  # Uses Notion MCP for data storage
        reply_to=agents_config["email"][0]  # → Forwards to Email Agent
    )

    # 4. Email Manager Agent (HITL & Email Sending)
    # Receives from Notion Agent, uses Human-in-the-Loop tool and Gmail MCP
    # NO reply_to = End of pipeline
    email_agent = LLMAgent(
        jid=agents_config["email"][0],
        password=passwords["email"],
        provider=provider,
        system_prompt=EMAIL_MANAGER_PROMPT,
        tools=[human_tool],  # Human-in-the-Loop capability
        mcp_servers=[gmail_mcp],  # Uses Gmail MCP for email sending
        termination_markers=["<EMAIL_PROCESS_COMPLETE>"]  # End conversation after email process
        # No reply_to = This is the end of the pipeline
    )

    # Start all agents
    print("\\n🚀 Starting multi-agent system...")
    agents = {
        "chat": user_chat,
        "analyzer": analyzer_agent, 
        "notion": notion_agent,
        "email": email_agent,
    }

    for name, agent in agents.items():
        await agent.start()
        print(f"✅ {name.capitalize()} agent started")

    # Wait for connections
    await asyncio.sleep(3.0)

    print("\\n" + "="*70)
    print("🐙 ADVANCED GITHUB MONITOR SYSTEM READY")
    print("="*70)
    print("\\n🎯 System capabilities:")
    print("1. 📊 Analyzes GitHub issues and pull requests via MCP")
    print("2. 📚 Stores analysis summaries in Notion database")
    print("3. 🤔 Consults human expert for email decisions")
    print("4. 📧 Sends professional email reports via Gmail MCP")
    print("\\n🛡️ Security: Custom guardrails ensure GitHub-only requests")
    print("🔧 Architecture: 4-agent pipeline with specialized roles")
    print("\\n💡 Example requests:")
    print("• 'Analyze recent issues in the repository'")
    print("• 'Check pull request activity this week'")
    print("• 'Monitor GitHub activity and send summary'")
    print("\\n⚠️  Note: MCP servers configured for external integrations")
    print("Ensure human expert is available for email confirmations.")
    print("\\nType 'exit' to quit\\n")
    print("-" * 70)

    # Instructions for human expert
    print(f"\\n👤 Human Expert Instructions:")
    print(f"🌐 Open web interface: http://localhost:8080")
    print(f"🔑 Connect as: {agents_config['human'][0]}")
    print("📧 You'll be asked about email sending decisions")

    try:
        # Run interactive chat
        await user_chat.run_interactive(
            input_prompt="🐙 GitHub> ",
            exit_command="exit",
            response_timeout=120.0  # Longer timeout for multi-agent processing
        )
    except KeyboardInterrupt:
        print("\\n👋 Shutting down...")
    finally:
        # Stop all agents
        print("\\n🔄 Stopping agents...")
        await user_chat.stop()
        for name, agent in agents.items():
            await agent.stop()
            print(f"✅ {name.capitalize()} agent stopped")

    print("\\n✅ Advanced GitHub Monitor system shutdown complete!")

if __name__ == "__main__":
    print("🚀 Starting Advanced Multi-Agent System...")
    print("\\n📋 Prerequisites:")
    print("• OpenAI API key")
    print("• XMPP server running")
    print("• MCP servers configured for GitHub/Notion/Gmail")
    print("• Human expert web interface: python -m spade_llm.human_interface.web_server")
    print()

    try:
        spade.run(main())
    except KeyboardInterrupt:
        print("\\n👋 System terminated by user")
    except Exception as e:
        print(f"\\n❌ System failed: {e}")
        print("💡 Check your configuration and try again")