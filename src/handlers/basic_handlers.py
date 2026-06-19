from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
import asyncio

from schemas.schemas import UserMessageDTO
from services.agent_services import handle_user_request

router = Router()

@router.message(F.text)
async def text_handler(message: types.Message):
    user_data = UserMessageDTO(
        id=message.from_user.id,
        nickname=message.from_user.full_name,
        username=message.from_user.username,
        text=message.text
    )

    ai_response = handle_user_request(user_data)

    await message.answer(ai_response)