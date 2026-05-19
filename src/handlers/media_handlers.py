from aiogram import Router, types, F, Bot
from aiogram.types import FSInputFile
import os

router = Router()

@router.message(F.photo)
async def photo_handler(message: types.Message):
    photo = FSInputFile("data/bro.jpg")
    await message.reply_photo(photo, caption="C братиком❤️🖕")

@router.message(F.sticker)
async def sticker_handler(message: types.Message):
    if message.sticker:
        await message.reply("Ишак бля, не грузится")

@router.message(F.voice)
async def voice_handler(message: types.Message):
    await message.reply("О, ты отправил голосовое сообщение!")

@router.message(F.video)
async def video_handler(message: types.Message):
    await message.reply("О, ты отправил видео!")    

@router.message(F.document)
async def document_handler(message: types.Message, bot: Bot):
    await message.reply("О, ты отправил документ!")

    os.makedirs("data", exist_ok=True)
    file_path = f"data/{message.document.file_name}"

    await bot.download(
        file=message.document.file_id,
        destination=file_path
    )