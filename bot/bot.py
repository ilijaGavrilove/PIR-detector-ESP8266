from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram import html, Dispatcher, Bot
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message

from bot.config import BOT_TOKEN
from database import db_requests

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"""Здравствуйте, {html.bold(message.from_user.full_name)}!\n
Спасибо за ваш выбор охранной системы! Я буду сообщать вам о засечении движения на вашей территории. Необходимо
зарегистрировать ваш свежеприобретенный датчик! Список доступных команд приведён ниже:\n
/new [имя датчика] - Зарегистрировать новый датчик

/delete [id датчика] - Удалить датчик

/show - Показать ваши датчики

/rename [id датчика],[новое имя] - Переименовать датчик (Примечание: новое название с символом "," недопустимо)

/help - Показать список доступных команд
    """)


@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer("""
/new [имя датчика] - Зарегистрировать новый датчик

/delete [id датчика] - Удалить датчик

/show - Показать ваши датчики

/rename [id датчика],[новое имя] - Переименовать датчик (Примечание: новое название с символом "," недопустимо)

/help - Показать список доступных команд 
    """)

@dp.message(Command("new"))
async def new_detector_handler(message: Message, command: CommandObject) -> None:
    user_input = command.args
    if not user_input:
        await message.answer("Пропущено название датчика! Правильный синтаксис команды\n/new [название датчика]")
    else:
        db_requests.add_detector(user_input, message.from_user.id)
        await message.answer(f"Датчик успешно добавлен! Id датчика {user_input} - {db_requests.get_last_detector_id()}")

@dp.message(Command("delete"))
async def delete_detector_handler(message: Message, command: CommandObject) -> None:
        user_input = command.args
        if not user_input:
            await message.answer("Пропущен идентификатор датчика! Правильный синтаксис команды\n/delete [id датчика]")
        else:
            if db_requests.delete_detector(user_input, message.from_user.id):
                await message.answer("Датчик успешно удалён!")
            else:
                await message.answer("Датчика под указаным id не существует или у вас нет доступа к этому датчику")

@dp.message(Command("show"))
async def show_detectors_handler(message: Message) -> None:
    detectors = db_requests.get_detectors(message.from_user.id)
    if detectors:
        output = 'id\tНазвание\n'
        for i in detectors:
            for j in i:
                output += str(j) + '\t'
            output += '\n'
        await message.answer(output)
    else:
        await message.answer("У вас нет зарегистрированных датчиков")

@dp.message(Command("rename"))
async def rename_detector_handler(message: Message, command: CommandObject) -> None:
    user_input = command.args
    if not user_input:
        await message.answer("Пропущены один или несколько аргументов команды!"
                             "Правильный синтаксис команды\n/rename [id датчика],[новое имя]."
                             "(Примечание: новое название с символом \",\" недопустимо)")
    else:
        user_input = user_input.split(",")
        try:
            if len(user_input) > 2:
                await message.answer("Ошибка! Возможно вы используете недопустимый символ \",\" в новом названии")
            else:
                if db_requests.rename_detector(user_input[0], message.from_user.id, user_input[1]):
                    await message.answer("Датчик успешно переименован")
                else:
                    await message.answer("Датчика под указаным id не существует или у вас нет доступа к этому датчику")

        except IndexError:
            await message.answer("Ошибка. Разделите идентификатор датчика и новое название запятой. "
                                "Правильный синтаксис команды\n/rename [id датчика],[новое имя].")


@dp.message()
async def wrong_input_handler(message: Message) -> None:
    await message.answer("Простите, я не понимаю вас! Чтобы увидеть список доступных команд введите /help")



async def main() -> None:
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)







