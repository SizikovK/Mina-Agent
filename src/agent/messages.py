from langchain_core.messages import BaseMessage
from dataclasses import dataclass

@dataclass
class ChatMessage:
    username: str
    message: str

class HistoryManager:
    def __init__(self):
        self.history: list[ChatMessage] = []

    def add_user_message(self, username: str, message: str):
        self.history.append(ChatMessage(username=username, message=message))    
        
    def get_history(self) -> list[BaseMessage]:
        return self.history
    
    def last_message(self) -> str:
        if self.history:
            return self.history[-1].message
        return ""

history = HistoryManager()