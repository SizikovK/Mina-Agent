from aiogram import types, Router, F
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(f"Привет! {message.from_user.first_name} Сынок ебаный.")

@router.message(Command("send_photo"))
async def send_photo_command(message: types.Message):
    photo = FSInputFile("data/gnida.jpg")
    await message.answer_photo(photo, caption="Вот твоя фотка.")
    
@router.message(F.text, lambda message: "бабушка" in message.text.lower())
async def send_voice_command(message: types.Message):
    voice = FSInputFile("data/granny_voice.ogg")
    await message.reply("Тебе голосовое от бабушки.")
    await message.answer_voice(voice)

@router.message(F.text)
async def test_handler(message: types.Message):
    await message.reply(f"Ты написал: {message.text}")