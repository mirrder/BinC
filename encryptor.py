# Copyright (c) 2026 mirrder
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# ==========================================
# BinC - Binary Cipher
# ==========================================

import re

# Сетка для АНГЛИЙСКОГО (4x7)
MATRIX_EN = [
    ['a','b','c','d'], ['e','f','g','h'], ['i','j','k','l'],
    ['m','n','o','p'], ['q','r','s','t'], ['u','v','w','x'],
    ['y','z',' ',' ']
]
# Сетка для РУССКОГО (6x6)
MATRIX_RU = [
    ['а','б','в','г','д','е'], ['ё','ж','з','и','й','к'], ['л','м','н','о','п','р'],
    ['с','т','у','ф','х','ц'], ['ч','ш','щ','ъ','ы','ь'], ['э','ю','я',' ', ' ', ' ']
]

CHAR2COORD_EN = {ch: (c+1, r+1) for r, row in enumerate(MATRIX_EN) for c, ch in enumerate(row) if ch != ' '}
CHAR2COORD_RU = {ch: (c+1, r+1) for r, row in enumerate(MATRIX_RU) for c, ch in enumerate(row) if ch != ' '}

PUNCTUATION = ['.', ',', '!', '?', ';', ':', '-', '"', "'"]

def detect_lang(text):
    for ch in text:
        if 'а' <= ch.lower() <= 'я' or ch.lower() == 'ё':
            return 'RU'
    return 'EN'

def encode_text(text: str) -> str:
    lang = detect_lang(text)
    char2coord = CHAR2COORD_RU if lang == 'RU' else CHAR2COORD_EN
    
    out = [f'<{lang}><[/]=']
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]
        
        if ch == ' ':
            out.append('%-%')
            i += 1
            continue

        if ch in PUNCTUATION:
            out.append(f"['{ch}']")
            i += 1
            continue

        lower = ch.lower()
        if lower not in char2coord:
            i += 1
            continue

        col, row = char2coord[lower]
        is_upper = ch.isupper()

        run = 1
        while i + run < n and text[i+run].lower() == lower and text[i+run].isupper() == is_upper:
            run += 1

        if is_upper:
            out.append('=^=')

        if run == 1:
            coord = f"{{{col},{row}}}"
        elif run == 2:
            coord = f'{{{col},{row}"1}}{{{col},{row}"2}}'
        else:
            coord = f'{{{col},{row}"!}}'

        out.append(coord)
        i += run

    return ''.join(out)

# --- БЛОК ЗАПУСКА ---
if __name__ == "__main__":
    # Текст для шифрования (замени "ur text" на свой)
    user_text = "ur text"  
    
    # Шифруем и выводим результат с подписью
    encrypted = encode_text(user_text)
    print(f"{encrypted} [encrypted on BinC by mirrder]")
