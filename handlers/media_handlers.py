from aiogram import Router, types, F

router = Router()

@router.message(F.photo)
async def photo_handler(message: types.Message):
    await message.reply(f"О, ты отправил фото! file_id: {message.photo[-1].file_id}")

@router.message(F.sticker)
async def sticker_handler(message: types.Message):
    if message.sticker:
        await message.reply("О, ты отправил стикер!")

@router.message(F.voice)
async def voice_handler(message: types.Message):
    await message.reply("О, ты отправил голосовое сообщение!")