from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile
import asyncio


router = Router()
delay = 3


@router.message(F.text)
async def text_handler(message: types.Message):
    #await asyncio.sleep(3)

    if not message.text:
        await message.reply("Не понял брат")
        return
    if not message.text.strip():
        await message.reply("Обнял родной")
        return
    if len(message.text) < 3 or len(message.text) > 150:
        await message.reply("🖕")
        return
    
    username=message.from_user.full_name
    text=message.text
    id=message.from_user.username

    responce = f"Приветствую тебя, {username}! Ты написал: '{text}'. Твой ID: {id}"

    if not responce.strip():
        return

    await message.reply(f"{responce}")