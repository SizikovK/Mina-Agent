from pydantic import BaseModel
from typing import Optional

class UserMessageDTO(BaseModel):
    id: int                         #123123123
    username: Optional[str] = None  #@Gnida
    nickname: str                   #Черемша Мытыщи 67
    text: str                       #скажи 67 1000 раз
