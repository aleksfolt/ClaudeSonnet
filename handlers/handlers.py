from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

handlers_router = Router()


@handlers_router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "<b>Привет,</b> я - <i>Claude Sonnet</i>, бот-нейросеть, "
        "созданный для общения. Я могу понимать <i>простые</i> "
        "фразы, отвечать на вопросы, а также генерировать "
        "<i>краткие</i> рассказы. <b>Как я могу помочь вам сегодня?</b>",
        parse_mode="HTML"
    )
