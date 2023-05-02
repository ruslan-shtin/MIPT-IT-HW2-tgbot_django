from aiogram import types

from aiogram.dispatcher import FSMContext
from . states import GameStates
from . app import dp, bot
from . keyboards import inline_kb
from . data_fetcher import get_next


@dp.message_handler(commands="train_all", state='*')
async def train_all(message: types.Message, state: FSMContext):
    await GameStates.all_words.set()
    res = await get_next(0)
    if not res:
        await GameStates.start.set()
        await message.reply('Все слова пройдены!')
        return

    async with state.proxy() as data:
        data['step'] = 1
        data['pk'] = 1
        data['answer'] = res.get('ru_translation')
        data['word'] = res.get('en_word')
        await message.reply(f"{data['step']}. Вы знаете, как переводится слово \"{data['word']}\"?", reply_markup=inline_kb)


@dp.callback_query_handler(lambda c: c.data in ["i_know", "i_dont_know"], state=GameStates.all_words)
async def button_click_call_back_all(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    answer = callback_query.data
    async with state.proxy() as data:
        if answer == "i_know":
            await bot.send_message(callback_query.from_user.id, "Ура! Вы молодец!", )
            res = await get_next(data.get('pk'))
            if res:
                data['step'] += 1
                data['pk'] = res.get('pk')
                data['answer'] = res.get('ru_translation')
                data['word'] = res.get('en_word')

                mess = f"{data['step']}. Вы знаете, как переводится слово \"{data['word']}\"?"
                await bot.send_message(callback_query.from_user.id, mess, reply_markup=inline_kb)
            else:
                await bot.send_message(callback_query.from_user.id, "The game is over!", )
                await GameStates.start.set()
        else:
            await bot.send_message(callback_query.from_user.id, "Попробуй ещё!", reply_markup=inline_kb)
