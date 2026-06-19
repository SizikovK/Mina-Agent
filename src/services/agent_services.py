from agent.agent import AgentService
from database.database import register_user, get_last_session, get_history, save_message
from schemas.schemas import UserMessageDTO

_agent_instance = AgentService(max_loops=30)

def get_agent_service() -> AgentService:
    return _agent_instance

def handle_user_request(user_data: UserMessageDTO) -> str:
    id = user_data.id
    username = user_data.username
    nickname = user_data.nickname
    text = user_data.text

    register_user(id, nickname, username)

    session = get_last_session(id)

    save_message(session, "user", text)

    history = get_history(session)
    response = _agent_instance.generate_response(history)

    save_message(session, "assistant", response)

    return response