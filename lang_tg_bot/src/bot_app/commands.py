from aiogram import types

from . import messages
from .app import dp
from . data_fetcher import get_next
from . import utils


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcom(message: types.Message):
    await message.reply(messages.WELCOME_MESSAGE)


@dp.message_handler(commands=['all_words'], state='*')
async def print_all_words(message: types.Message):
    pairs = list()
    res = await get_next(0)
    while res:
        ru_word = res.get('ru_translation')
        en_word = res.get('en_word')
        pairs.append([ru_word, en_word])
        pk = res.get('pk')
        res = await get_next(pk)
    msg = utils.compile_pairs_into_message(pairs)
    await message.reply(msg)
