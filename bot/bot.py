import asyncio
import logging
import os
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters.command import CommandStart
import speech_recognition as sr
import subprocess
from config import settings
import httpx

bot = Bot(settings.TG_TOKEN)
dp = Dispatcher()
r = sr.Recognizer()


@dp.message(CommandStart())
async def hello_message(message: types.Message):
    await bot.send_message(message.chat.id, "Hello!")

@dp.message()
async def ai_response_message(message: types.Message):
    if message.text:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://chatlord:8000/ai", params={"q": message.text})
            await message.answer(response.json()['response'])
    elif message.voice:
        file_id = message.voice.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, f"{file_id}.mp3")

        file_name_wav = f"{file_id}.wav"
        subprocess.call(['ffmpeg', '-i', f"{file_id}.mp3", file_name_wav])

        with sr.AudioFile(file_name_wav) as source:
            audio = r.record(source)
        text = r.recognize_google(audio, language='ru')
        text = text

        async with httpx.AsyncClient() as client:
            response = await client.get("http://chatlord:8000/ai", params={"q": text}, timeout=40)
            await message.answer(response.json()['response'])

        os.remove(f"{file_id}.mp3")
        os.remove(file_name_wav)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

asyncio.run(main())