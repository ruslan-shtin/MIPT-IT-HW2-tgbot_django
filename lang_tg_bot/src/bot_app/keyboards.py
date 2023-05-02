from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


inline_button_know = InlineKeyboardButton("I know", callback_data="i_know")
inline_button_notknow = InlineKeyboardButton("I don't know", callback_data="i_dont_know")
inline_kb = InlineKeyboardMarkup()

inline_kb.add(inline_button_know)
inline_kb.add(inline_button_notknow)
