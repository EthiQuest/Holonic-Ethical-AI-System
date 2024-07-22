# src/core/user_communication.py

from src.agents.ceo_agent import ceo_agent
from src.agents.agent_communication import AgentCommunication

class UserCommunication:
    @staticmethod
    async def send_message_to_ceo(message: str):
        response = await ceo_agent.process_user_message(message)
        return response

    @staticmethod
    async def send_message_to_agent(agent_id: str, message: str):
        await AgentCommunication.send_message("user", agent_id, message)
        # Implement a method to get the agent's response
        response = await AgentCommunication.get_agent_response(agent_id)
        return response

    @staticmethod
    async def get_agent_list():
        return await ceo_agent.get_subordinate_agents()

user_communication = UserCommunication()