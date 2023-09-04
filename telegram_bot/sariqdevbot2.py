import logging
import os

import httpx
import wikipedia
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import WebAppInfo, InlineKeyboardButton, BotCommand, InlineKeyboardMarkup
from dotenv import load_dotenv

from data import Data
from menu import menu1, tahorat_niyatt, tahorat_h, suralar_get, uzb_tillarda, arb_tillarda, audio, ikkinchi_ekrani, \
    qoshimcha_button


class LoginState(StatesGroup):
    name = State()


load_dotenv('.env')
wikipedia.set_lang('uz')
TOKEN = os.getenv('Token')

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

import psycopg2

con = psycopg2.connect(
    dbname='projectdb',  # noqa
    user='ddd',
    password='777',
    host='localhost'
)
cur = con.cursor()


class FormSura(StatesGroup):
    raqam = State()


class Formoyat(StatesGroup):
    raqam = State()


tahorat_vik = "Tahorat — namoz oʻqish, ibodat oldidan yuvinish," \
              " poklanish jarayoni. Xususiy shakli sifatida tayammum" \
              " koʻriladi. Islomda tahoratning ikki turi mavjud: vuzuʼ — kichik" \
              " tahorat — qoʻl oyoq va yuzni yuvish;" \
              " gʻusul — katta tahorat — toʻla" \
              " yuvinish, choʻmilish. Tahoratning 4 ta farzi bor; yuzni yuvmoq;" \
              " ikki qoʻlni tirsak ila qoʻshib yuvmoq; ikki oyoqni toʻpigʻi ila qoʻshib yuvmoq," \
              " boshning toʻrtdan bir qismiga mash tortish — ikki qoʻlni hoʻllab surtmoq. Bu farzlardan " \
              "birortasi bajarilmasa, tahorat haqiqiy boʻlmaydi. Tahoratning farzlaridan " \
              "boshqa uning sunnat va vojiblari ham boʻladi. Tahorat oladigan har bir kimsa " \
              "suvni keragidan ortiq ham, oz ham sarf qilmasligi; suvni yuzga shapillatib sochmasligi; " \
              "tahorat qilayotganda oʻrinsiz gaplashmasligi; iflos yerda tahorat olmasligi kerak. " \
              "Tahorat qilish uchun suv topilmasa tayammum qilinadi. Tahorati bor kishida quyidagi" \
              " holatlardan biri yuz bersa tahorati buzilgan hisoblanadi: vujudning biron yeridan qon," \
              " yiring, suv chiqsa; ogʻzi toʻlib qussa; tupurgan vaqt tupugini yarmidan koʻpi qon boʻlsa;" \
              " kichik va katta hojatga borsa va orqadan yel chiqarsa; bexush yoki mast boʻlsa; namoz vaqtida kulsa;" \
              " uxlasa. Tahoratni buzadigan holatlar roʻy bersa, tahoratni boshqatdan qilish lozim boʻladi. "

taxorat_niyatlari = """
Tahorat uchun suv hozirlagandan keyin:

    Qibla tomonga qarab, ichida "Tahorat olishni niyat qildim" deyiladi.
    "Auzu billahi minash-shaytonir rojiym. Bismillahir rohmanir rohiym", deyiladi.
    Qoʻllar bandigacha 3 marta yuviladi.
    Oʻng qoʻlda suv olinib, ogʻiz 3 marta gʻargʻara qilib chayiladi va misvok qilinadi.
    Burunga oʻng qoʻl bilan 3 marta suv tortilib, chap qoʻl bilan qoqib tozalanadi.
    Yuz 3 marta yuviladi.
    Avval oʻng qoʻl tirsaklar bilan qoʻshib ishqalab yuviladi, soʻngra chap qoʻl.
    Hovuchga suv olib, toʻkib tashlab, hoʻli bilan boshning hamma qismiga masx tortiladi.
    Koʻrsatkich barmoq bilan quloqlarning ichi, bosh barmoqlar bilan esa quloq orqasi masx qilinadi.
    Ikkala kaftning orqasi bilan boʻyin masx qilinadi.
    Chap qoʻl bilan oʻng oyoqni oshiq qismi bilan qoʻshib, barmoqlar orasini ishqalab 3 marta yuviladi, keyin chap oyoq.
    Qibla tomonga qarab, ichida "Ashhadu an La ilaha illallohu va ashhadu anna Muhammadan abduhu va rosuluh" deyiladi."""

gusul_vik = "Gʻusl (arab. — choʻmilish) — pok boʻlish" \
            " uchun butun badanni maxsus tartibda yuvish. " \
            "Gʻusl jinsiy aloqa, ihtilom, hayzdan keyin farz boʻladi. " \
            "Hanafiylik mazhabida Gʻuslning sharti 3 ta — ogʻizni gʻargʻara" \
            " qilish, burunni yaxshilab yuvish, badanning hamma joyini " \
            "suv bilan poklash. boshqa mazhablarda ogʻiz-burun chayish farz emas." \
            " Islomda bir haftada 1-marta (juma kuni), 2 hayit va arafa kunlari " \
            "Gʻusl qilish sunnat sanaladi. Gʻusl katta tahorat deb ham ataladi." \
            " Gʻusl mayitga nisbatan ham ishlatilib, bu ishni gʻassol (yuvgʻuchi) " \
            "bajaradi. Gʻusl haqida Qurʼonda zikr qilingan\n "

gusul_shartlar = "GʻUSLNING FARZLARI\n" \
                 "1. Ogʻizni chayqash.\n" \
                 "2. Burunni chayqash.\n" \
                 "3. Badanning barcha yerini yuvish.\n" \
                 "Gʻuslda quyidagi narsalar makruxdir:\n1. Suvni isrof qilish.\n2. Suvni oʻta oz ishlatish.\n3. Suvni yuziga urish." \
                 "4. Odamlar gapini gapirish.\n5. Uzrsiz boshqadan yordam olish.\n6 . Duo qilish. \n\n" \
                 "GʻUSLNI VOJIB QILUVCHI NARSALAR\n" \
                 "1. Ajralib chiqayotganda shahvat bilan otilib keladigan maniyni tushirish.\n" \
                 "2. Zakarning boshi old yoki orqa (farj) ichiga gʻoyib boʻlishi qiluvchiga ham, qilinuvchiga ham (gʻuslni vojib qiladi)\n" \
                 "3. Uygʻongan kishi maniy yoki maziyni koʻrishi.\n" \
                 "4 −5 . Hayz va nifosning toʻxtashi.\n" \
                 "6. SHahid boʻlmagan musulmon mayyitga ham gʻusl vojib boʻladi.\n" \
                 "7. Nomusulmon shaxs Islomga kirsa."


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await bot.set_my_commands([BotCommand("start", "Qayta ishga tushurish"), BotCommand("help", "yordam olish")])
    menu1()
    user_id = message.from_user.id
    user_username = message.from_user.username
    user_firs_name = message.from_user.first_name
    user_message = message.text
    query = "insert into bot_user(user_id, user_username,user_firs_name, message)" \
            " values (%s,%s,%s,%s)"
    cur.execute(query, (user_id, user_username, user_firs_name, user_message))
    con.commit()
    await message.answer(text='Assalomu alekum musulmonlar🤵', reply_markup=menu1())


@dp.callback_query_handler(Text('rasm'))
async def alifbo(clb: types.CallbackQuery):
    await clb.message.delete()
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton('Orqaga', callback_data='orqa👉'))
    await bot.send_photo(clb.from_user.id, open('position3.jpg', 'rb'), reply_markup=ikm)


@dp.callback_query_handler(lambda call: call.data == 'orqa👉')
async def back_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Qo'shimcha tugmalar", reply_markup=qoshimcha_button())


@dp.callback_query_handler(Text('qoshimcha'))
async def qoshimcha_malumotlar(clb: types.CallbackQuery):
    await clb.message.delete()
    await clb.message.answer("Qo'shimcha tugmalar", reply_markup=qoshimcha_button())


@dp.callback_query_handler(lambda call: call.data == '💙')
async def back_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    username = callback.from_user.first_name
    reaksiya = callback.data
    query = 'insert into like_(user_name, reaction) values (%s,%s)'
    cur.execute(query, (username, reaksiya))
    con.commit()
    ikm = InlineKeyboardMarkup()
    ikm.add(
        InlineKeyboardButton('Orqaga', callback_data='orqa💙')
    )
    await callback.message.answer('Sizga yoqqanidan xursandmiz🥰 ', reply_markup=ikm)


@dp.callback_query_handler(lambda call: call.data == '💔')
async def back_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    username = callback.from_user.first_name
    reaksiya = callback.data
    query = 'insert into like_(user_name, reaction) values (%s,%s)'
    cur.execute(query, (username, reaksiya))
    con.commit()
    ikm = InlineKeyboardMarkup()
    ikm.add(
        InlineKeyboardButton('Orqaga', callback_data='orqa💙')
    )
    await callback.message.answer('Fikringiz uchun raxmat🤗', reply_markup=ikm)


@dp.callback_query_handler(lambda call: call.data == 'orqa💙')
async def back_menu(callback: types.CallbackQuery):
    await bot.edit_message_text("Qo'shimcha tugmalar", callback.from_user.id, callback.message.message_id,
                                reply_markup=qoshimcha_button())


@dp.callback_query_handler(lambda call: call.data == 'orqagal')
async def back_menu(callback: types.CallbackQuery):
    await bot.edit_message_text('Assalomu alekum musulmonlar🤵', callback.from_user.id, callback.message.message_id,
                                reply_markup=menu1())


@dp.callback_query_handler(Text("tahorat"))
async def tahorat_haqida(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=tahorat_vik, reply_markup=tahorat_h())


@dp.callback_query_handler(lambda call: call.data == 'orqaga1')
async def back_menu(callback: types.CallbackQuery):
    await bot.edit_message_text('Assalomu alekum musulmonlar🤵', callback.from_user.id, callback.message.message_id,
                                reply_markup=menu1())


@dp.callback_query_handler(Text("sikl"))
async def tahorat_niyatlari(callback: types.CallbackQuery):
    await callback.message.delete()
    tahorat_niyatt()
    await callback.message.answer(taxorat_niyatlari, reply_markup=tahorat_niyatt())


@dp.callback_query_handler(lambda call: call.data == 'orqaga2')
async def back_menu(callback: types.CallbackQuery):
    await bot.edit_message_text(tahorat_vik, callback.from_user.id, callback.message.message_id,
                                reply_markup=tahorat_h())


@dp.callback_query_handler(Text("gusul"))
async def gusul(callback: types.CallbackQuery):
    await callback.message.delete()
    inkb = InlineKeyboardMarkup()
    inkb.add(
        InlineKeyboardButton(text='Orqaga', callback_data='orqaga3'),
        InlineKeyboardButton("Qo'shimcha 📂", web_app=WebAppInfo(url='https://uz.wikipedia.org/wiki/G%CA%BBusl'))
    )
    await callback.message.answer(text=gusul_vik + gusul_shartlar, reply_markup=inkb)


@dp.callback_query_handler(lambda call: call.data == 'orqaga3')
async def back_menu(callback: types.CallbackQuery):
    await bot.edit_message_text('Assalomu alekum musulmonlar🤵', callback.from_user.id, callback.message.message_id,
                                reply_markup=menu1())


sd = suralar_get()
data = ''
for i in sd[0]:
    data += ''.join(i)


@dp.callback_query_handler(Text("quron"))
async def quronga_kirish(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Surani qidirish\n" + data, reply_markup=sd[1])


@dp.callback_query_handler(Text('search'))
async def search(callback: types.CallbackQuery):
    await FormSura.raqam.set()
    await callback.message.answer('Surani raqamini kiriting: ')


@dp.callback_query_handler(Text('orqagas'))
async def orqagas(clb: types.CallbackQuery):
    await bot.edit_message_text('Assalomu alekum musulmonlar🤵', clb.from_user.id, clb.message.message_id,
                                reply_markup=menu1())


@dp.message_handler(state=FormSura.raqam)
async def oyatlarga_kirish(msg: types.Message, state: FSMContext):
    await state.update_data(number=msg.text)
    sb = uzb_tillarda(msg.text)
    await msg.answer(sb[0], reply_markup=sb[1])
    await state.finish()


@dp.callback_query_handler(Text('sura_orqaga'))
async def orq(clb: types.CallbackQuery):
    await bot.edit_message_text("Surani qidirish\n" + data, clb.from_user.id, clb.message.message_id,
                                reply_markup=sd[1])


@dp.callback_query_handler(lambda callback: 'arb_' in callback.data)
async def arab_tilida(clb: types.CallbackQuery):
    await clb.message.delete()
    n = clb.data.lstrip('arb_')
    sb = arb_tillarda(n)
    await clb.message.answer(sb[0], reply_markup=sb[1])


@dp.callback_query_handler(lambda callback: 'uzb_' in callback.data)
async def uzb_tilidaa(clb: types.CallbackQuery):
    await clb.message.delete()
    n = clb.data.lstrip('uzb_')
    sb = uzb_tillarda(n)
    await clb.message.answer(sb[0], reply_markup=sb[1])


@dp.callback_query_handler(lambda callback: 'audio_' in callback.data)
async def audio_file(clb: types.CallbackQuery):
    n = clb.data.lstrip('audio_')
    sb = audio(n)
    ikm = InlineKeyboardMarkup(row_width=2)
    ikm.add(
        InlineKeyboardButton('Orqaga', callback_data='orqagat'),
    )
    await clb.message.answer(sb, reply_markup=ikm)


@dp.callback_query_handler(Text('orqagat'))
async def orqagat(clb: types.CallbackQuery):
    await bot.edit_message_text("Surani qidirish\n" + data, clb.from_user.id, clb.message.message_id,
                                reply_markup=sd[1])


@dp.callback_query_handler(Text(contains='page'))
async def wek(callback: types.CallbackQuery):
    t = callback.data.split('=')[1]
    op = ikkinchi_ekrani(t)
    data = ''
    for i in op[0]:
        data += ''.join(i)
    await bot.edit_message_text("Surani qidirish\n" + data, callback.from_user.id, callback.message.message_id,
                                reply_markup=op[1])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
