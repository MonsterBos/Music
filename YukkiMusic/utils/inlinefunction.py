from math import ceil
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import MOD_LOAD, MOD_NOLOAD

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_modules(page_n, module_dict, prefix, chat=None):
    if not chat:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{})".format(
                        prefix, x.__MODULE__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )
    else:
        modules = sorted(
            [
                EqInlineKeyboardButton(
                    x.__MODULE__,
                    callback_data="{}_module({},{},{})".format(
                        prefix, chat, x.__MODULE__.lower(), page_n
                    ),
                )
                for x in module_dict.values()
            ]
        )

    pairs = [modules[i : i + COLUMN_SIZE] for i in range(0, len(modules), COLUMN_SIZE)]

    COLUMN_SIZE = 3
    NUM_COLUMNS = 4

    max_num_pages = ceil(len(pairs) / NUM_COLUMNS) if len(pairs) > 0 else 1
    modulo_page = page_n % max_num_pages

    if len(pairs) > NUM_COLUMNS:
        pairs = pairs[modulo_page * NUM_COLUMNS : NUM_COLUMNS * (modulo_page + 1)] + [
            (
                EqInlineKeyboardButton(
                    "❮",
                    callback_data="{}_prev({})".format(
                        prefix,
                        modulo_page - 1 if modulo_page > 0 else max_num_pages - 1,
                    ),
                ),
                EqInlineKeyboardButton(
                    "Bᴀᴄᴋ",
                    callback_data="settingsback_helper",
                ),
                EqInlineKeyboardButton(
                    "❯",
                    callback_data="{}_next({})".format(prefix, modulo_page + 1),
                ),
            )
        ]

    return pairs