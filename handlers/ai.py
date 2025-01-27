from aiogram import Router, F
from aiogram.types import Message
from database.history import save_chat_history, load_chat_history
import aiohttp

from filters.IsPrivate import IsPrivateChatFilter


ai_router = Router()


@ai_router.message(F.text, IsPrivateChatFilter())
async def ai(msg: Message):
    user_message = msg.text.strip()

    if not user_message:
        await msg.answer("❌ Запрос не может быть пустым!")
        return

    chat_history = load_chat_history(msg.from_user.id)

    messages = [{"role": "user", "content": entry["user"]} for entry in chat_history]
    messages.append({"role": "user", "content": user_message})

    dict_to_send = {
        "model": "claude-3.5-sonnet",
        "request": {
            "messages": messages
        }
    }

    try:
        message = await msg.answer("⏳")
        async with aiohttp.ClientSession() as session:
            async with session.post('http://api.onlysq.ru/ai/v2', json=dict_to_send) as res:
                res.raise_for_status()
                response_data = await res.json()

        bot_response = response_data.get('answer', "Ошибка: ответ не получен от API.")
        save_chat_history(msg.from_user.id, user_message, bot_response)

        try:
            await msg.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message.message_id,
                text=bot_response,
                parse_mode="Markdown"
            )
        except Exception:
            try:
                await msg.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=message.message_id,
                    text=bot_response,
                )
            except Exception as e:
                await msg.answer(f"❌ Произошла ошибка: {e}")

    except aiohttp.ClientError as e:
        await msg.answer(f"❌ Ошибка при обращении к API: {e}")
    except Exception as e:
        await msg.answer(f"❌ Произошла ошибка: {e}")