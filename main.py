from agent.agent import Agent 
from core.config import AgentConfig

if __name__ == "__main__":
    config = AgentConfig()
    agent = Agent(config)
    agent.run