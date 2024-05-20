import re
from math import ceil
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text


def paginate_modules(page_n, module_dict, prefix, chat=None):
    modules = sorted(
        [
            EqInlineKeyboardButton(
                x.__MODULE__,
                callback_data=f"{prefix}_module({x.__MODULE__.lower()},{page_n})",
            )
            for x in module_dict.values()
        ]
    )

    pairs = [modules[i : i + 3] for i in range(0, len(modules), 3)]
    COLUMN_SIZE = 5
    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "❮", callback_data=f"{prefix}_prev({modulo_page})"
                ),
                EqInlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close"),
                EqInlineKeyboardButton(
                    "❯", callback_data=f"{prefix}_next({modulo_page})"
                ),
            )
        ]

    return pairs
