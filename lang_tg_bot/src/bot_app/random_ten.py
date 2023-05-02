from aiogram import types
from aiogram.dispatcher import FSMContext
from . states import GameStates
from . app import dp, bot
from . keyboards import inline_kb
from . data_fetcher import get_random


@dp.message_handler(commands="train_ten", state='*')
async def train_ten(message: types.Message, state: FSMContext):
    await GameStates.random_ten.set()
    res = await get_random()
    async with state.proxy() as data:
        data['step'] = 1
        data['answer'] = res.get('ru_translation')
        data['word'] = res.get('en_word')
        await message.reply(f"{data['step']} of 10. Вы знаете, как переводится слово \"{data['word']}\"?", reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data in ["i_know", "i_dont_know"], state=GameStates.random_ten)
async def button_click_call_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    async with state.proxy() as data:
        if answer == "i_know":
            await bot.send_message(callback_query.from_user.id, "Ура! Вы молодец!", )
        else:
            await bot.send_message(callback_query.from_user.id, "У Вас всё впереди!", )
        res = await get_random()
        data['step'] += 1
        data['answer'] = res.get('ru_translation')
        data['word'] = res.get('en_word')
        if data['step'] > 10:
            await bot.send_message(callback_query.from_user.id, "The game is over!", )
            await GameStates.start.set()
        else:
            mess = f"{data['step']} of 10. Вы знаете, как переводится слово \"{data['word']}\"?"
            await bot.send_message(callback_query.from_user.id, mess, reply_markup=inline_kb)
