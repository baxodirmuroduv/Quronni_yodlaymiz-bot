import httpx
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from data import Data


def menu1():
    quron = InlineKeyboardButton(text="Quron", callback_data="quron")
    tahorat = InlineKeyboardButton(text="Tahorat", callback_data="tahorat")
    gusul = InlineKeyboardButton(text="G'usul", callback_data="gusul")
    qoshimcha = InlineKeyboardButton(text="Qo'shimcha ma'lumot", callback_data="qoshimcha")
    design = [
        [tahorat, gusul],
        [quron, qoshimcha]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=design)
    return markup


def tahorat_niyatt():
    inkb = InlineKeyboardMarkup()
    inkb.add(InlineKeyboardButton(text='Orqaga', callback_data='orqaga2'))
    return inkb


def tahorat_h():
    ikb = InlineKeyboardButton(text='Taxorat olish ketma-ketligi⏩', callback_data='sikl')
    ikb1 = InlineKeyboardButton(text='Orqaga', callback_data='orqaga1')
    desine = [
        [ikb, ikb1]
    ]
    ikm = InlineKeyboardMarkup(inline_keyboard=desine)
    return ikm


def suralar_get():
    cur_page = 1
    ikm = InlineKeyboardMarkup()
    ikm.add(
        InlineKeyboardButton('⬅️', callback_data=f"page=prev_{len(Data) if cur_page == 1 else cur_page - 10}"),
        InlineKeyboardButton(f"{cur_page}/{len(Data)}", callback_data=f"page=cur_page_{cur_page}"),
        InlineKeyboardButton('➡️', callback_data=f"page=next_{1 if cur_page == len(Data) else cur_page + 10}"),
        InlineKeyboardButton("🔍", callback_data='search'),
        InlineKeyboardButton("Chiqish", callback_data='orqagas')
    )
    d = Data
    f = [f"{d[cur_page - 1][0]} {d[cur_page - 1][1]}\n"
         f"{d[cur_page][0]} {d[cur_page][1]}\n"
         f"{d[cur_page + 1][0]} {d[cur_page + 1][1]}\n"
         f"{d[cur_page + 2][0]} {d[cur_page + 2][1]}\n"
         f"{d[cur_page + 3][0]} {d[cur_page + 3][1]}\n"
         f"{d[cur_page + 4][0]} {d[cur_page + 4][1]}\n"
         f"{d[cur_page + 5][0]} {d[cur_page + 5][1]}\n"
         f"{d[cur_page + 6][0]} {d[cur_page + 6][1]}\n"
         f"{d[cur_page + 7][0]} {d[cur_page + 7][1]}\n"
         f"{d[cur_page + 8][0]} {d[cur_page + 8][1]}"]
    return [f, ikm]


def uzb_tillarda(n: int):
    krl_sura = httpx.get(
        f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/uzb-alauddinmansour/{n}.json")
    krl = ''
    k = ''
    for i in krl_sura.json()['chapter']:
        krl += (i['text'] + '\n')
        for j in Data:
            if j[0] == i['chapter']:
                k = j[1]
    e = ''
    for i in krl:
        e += i
    page = 1
    pageN = 4089
    if len(krl) > 4089:
        g = k + '\n' + e[page - 1:pageN]
        ikm = InlineKeyboardMarkup()
        ikm.add(
            InlineKeyboardButton('⬅️', callback_data='next_N'),
            InlineKeyboardButton('➡️', callback_data='prev_N'),
            InlineKeyboardButton("uzb", callback_data=f'uzb_{n}'),
            InlineKeyboardButton('arb', callback_data=f'arb_{n}'),
            InlineKeyboardButton('audio', callback_data=f'audio_{n}'),
            InlineKeyboardButton('Orqaga', callback_data='sura_orqaga'))
        return [g, ikm]
    else:
        g = k + '\n' + e
        ikm = InlineKeyboardMarkup()
        ikm.add(
            InlineKeyboardButton("uzb", callback_data=f'uzb_{n}'),
            InlineKeyboardButton('arb', callback_data=f'arb_{n}'),
            InlineKeyboardButton('audio', callback_data=f'audio_{n}'),
            InlineKeyboardButton('Orqaga', callback_data='sura_orqaga'))
        return [g, ikm]


def arb_tillarda(n: int):
    krl_sura = httpx.get(
        f'https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/ara-quran-la5/{n}.json')
    krl = ''
    k = ''
    for i in krl_sura.json()['chapter']:
        krl += (i['text'] + '\n')
        for j in Data:
            if j[0] == i['chapter']:
                k = j[1]
    e = ''
    for i in krl:
        e += i
    page = 1
    pageN = 4089
    if len(krl) > 4089:
        g = k + '\n' + e[page - 1:pageN]
        ikm = InlineKeyboardMarkup()
        ikm.add(
            InlineKeyboardButton('⬅️', callback_data=f'next_N{n}'),
            InlineKeyboardButton('➡️', callback_data=f'prev_N{n}'),
            InlineKeyboardButton("uzb", callback_data=f'uzb_{n}'),
            InlineKeyboardButton('arb', callback_data=f'arb_{n}'),
            InlineKeyboardButton('audio', callback_data=f'audio_{n}'),
            InlineKeyboardButton('Orqaga', callback_data='sura_orqaga'))
        return [g, ikm]
    else:
        g = k + '\n' + e
        ikm = InlineKeyboardMarkup()
        ikm.add(
            InlineKeyboardButton("uzb", callback_data=f'uzb_{n}'),
            InlineKeyboardButton('arb', callback_data=f'arb_{n}'),
            InlineKeyboardButton('audio', callback_data=f'audio_{n}'),
            InlineKeyboardButton('Orqaga', callback_data='sura_orqaga'))
        return [g, ikm]


def audio(n: int):
    number = n
    url = httpx.get('https://api.quran.com/api/v4/chapter_recitations/114/?language=en')
    r = url.json()
    m = r['audio_files'][int(number) - 1]
    return m['audio_url']


def ikkinchi_ekrani(t):
    if t.startswith('prev_'):
        cur_page = int(t.split('prev_')[-1])
    elif t.startswith('next_'):
        cur_page = int(t.split('next_')[-1])
    else:
        cur_page = int(t.split('cur_page_')[-1])

    ikm = InlineKeyboardMarkup()
    ikm.add(
        InlineKeyboardButton('⬅️', callback_data=f'page=prev_{len(Data) if cur_page == 1 else cur_page - 10}'),
        InlineKeyboardButton(f'{cur_page + 9}/{len(Data)}', callback_data='page=cur_page_'),
        InlineKeyboardButton('➡️', callback_data=f'page=next_{1 if cur_page == len(Data) else cur_page + 10}'),
        InlineKeyboardButton("🔍", callback_data='search'),
        InlineKeyboardButton("Chiqish", callback_data='orqagas')
    )
    d = Data

    dek = [f"{d[cur_page - 1][0]} {d[cur_page - 1][1]}\n"
           f"{d[cur_page][0]} {d[cur_page][1]}\n"
           f"{d[cur_page + 1][0]} {d[cur_page + 1][1]}\n"
           f"{d[cur_page + 2][0]} {d[cur_page + 2][1]}\n"
           f"{d[cur_page + 3][0]} {d[cur_page + 3][1]}\n"
           f"{d[cur_page + 4][0]} {d[cur_page + 4][1]}\n"
           f"{d[cur_page + 5][0]} {d[cur_page + 5][1]}\n"
           f"{d[cur_page + 6][0]} {d[cur_page + 6][1]}\n"
           f"{d[cur_page + 7][0]} {d[cur_page + 7][1]}\n"
           f"{d[cur_page + 8][0]} {d[cur_page + 8][1]}"]
    return [dek, ikm]


def qoshimcha_button():
    ikm = InlineKeyboardMarkup(row_width=3)
    ikm.add(
        InlineKeyboardButton('Alifbo', callback_data='rasm'),
        InlineKeyboardButton('Umar ibn..', web_app=WebAppInfo(url='https://t.me/Umar_ibn_Hattob_seriali')),
        InlineKeyboardButton('Islom.uz', web_app=WebAppInfo(url='https://islom.uz/')),
        InlineKeyboardButton('💙 bot yoqdi', callback_data='💙'),
        InlineKeyboardButton('💔 bot yoqmadi', callback_data='💔'),
        InlineKeyboardButton('Orqaga', callback_data='orqagal')
    )
    return ikm

