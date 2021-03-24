import telebot
import re
import googletrans
from googletrans import Translator
from telebot import types
from datetime import datetime
import requests

trans = Translator()

response = requests.get("https://coronavirus-19-api.herokuapp.com/countries")

data = response.json()

bot = telebot.TeleBot("token")

c = False

id = ""

leng = "uzb"

izoh ={
    "izox": False,
    "secret": False,
    "reply": False,
    "id": 0
}

lengs = {
    'uzb': ["🇺🇿 O'zbek tili muvofaqiyatli o'rnatildi","🛠 Tilni tanlash", "👨‍💻 Dastur xaqida", "📝 Izoh", "🛠 Kerakli tilni tanlang:",  "🇺🇿 O'zbekiston", "🌎 Dunyo", "📍 Kerakli hududni tanlang:", "📌 Boshqa hudud", "    🦠 COVID-19 statistikasi:", "   📌 Joylashuv:   ", "   🕔 Vaqt:   ", "uz", "📌 Kerakli hudud nomini kiriting: ", "❌ Bunday joylashuv topilmadi, iltimos qayta kiriting: ", "📝 Marxamat dastur uchun o'z izoxingizni qoldiring: "],
    'rus': ["🇷🇺 Русский язык успешно установлен", "🛠 Выбор языка", "👨‍💻 О программе", "📝 Комментарий", "🛠 Выберите нужный язык:", "🇺🇿 Узбекистан", "🌎 Мир", "📍 Выберите ваше местоположение:", "📌 Другие местоположения", "   🦠 Статистика COVID-19:", "     📌 Местоположения:   ", "     🕔 Время:   ", "ru", "📌 Введите название страны, которую вы хотите: ", "❌ Такое местоположение не найдено, пожалуйста, введите заново: ", "📝 Пожалуйста, оставьте свой комментарий к программе:"],
    'eng': ["🇬🇧 English language was successfully installed", "🛠 Select language", "👨‍💻 About programm", "📝 Comment", "🛠 Select your language:", "🇺🇿 Uzbekistan", "🌎 The world", "📍 Choose your location:", "📌 Another location", "   🦠 Statistics of COVID-19:", "   📌 Location:   ", "   🕔 Time:   ", "en", "📌 Enter the name of the desired country: ", "❌ No such location found, please try again: ", "📝 Please enter your comment for the program:"]
}

covid = {
    'uzb': ["Jami kasallanganlar: ", "Bugun kasallanganlar: ", "Jami o'limlar: ", "Bugungi o'limlar: ", "Jami sog'ayganlar: ", "Hozirda faol: ", "Og'ir xolatlar: ", "Jami testlar: "],
    'rus': ["Всего заражено: ", "Заражено сегодня: ", "Общие смерти: ", "Сегодня смерти: ", "Выздоровели: ", "В настоящее время активен: ", "Критический: ", "Всего тестов: "],
    'eng': ["Total cases: ", "Today cases: ", "Total deaths: ", "Today deaths: ", "Total recovered: ", "Active: ", "Critical: ", "Total tests: "]
}

def search(country, el):
    text = ""
    for i in data:
        if i["country"] == country:
            text = i[el]
            break
    return text

def search_country(text):
    l = False
    trans_text = trans.translate(text, dest='en').text
    for i in data:
        if i["country"] == trans_text:
            l = True
    return l




def covid19(country):
    global leng, id
    curr = datetime.now()
    time = datetime.strftime(curr, "%d/%m/%y, %H:%M")
    text = lengs[leng][9]
    davlat = country
    text = text + "\n" + lengs[leng][10] + davlat
    text = text + "\n" + lengs[leng][11] + time
    text = text + "\n" + "----------------------------------------------"
    text = text + "\n   " + covid[leng][0] + "   " + str(search(country, "cases"))
    text = text + "\n   " + covid[leng][1] + "   " + str(search(country, "todayCases"))
    text = text + "\n   " + covid[leng][2] + "   " + str(search(country, "deaths"))
    text = text + "\n   " + covid[leng][3] + "   " + str(search(country, "todayDeaths"))
    text = text + "\n   " + covid[leng][4] + "   " + str(search(country, "recovered"))
    text = text + "\n   " + covid[leng][5] + "   " + str(search(country, "active"))
    text = text + "\n   " + covid[leng][6] + "   " + str(search(country, "critical"))
    text = text + "\n   " + covid[leng][7] + "   " + str(search(country, "totalTests"))
    return text


        

def replylang(id):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=3)
    buttons.add(lengs[leng][1], "🦠 COVID-19", lengs[leng][2], lengs[leng][3])
    bot.send_message(id, lengs[leng][0], reply_markup = buttons)

@bot.message_handler(commands = ["start"])
def start(message):
    text = "🇺🇿 Kerakli tilni tanlang:\n ------------------------- \n🇷🇺 Выберите нужный язык:\n--------------------------\n🇬🇧 Select your language:"
    langs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
    langs.add("🇺🇿 o'zbek", "🇷🇺 русский", "🇬🇧 english")
    bot.send_message(message.chat.id, text, reply_markup=langs)

@bot.message_handler(commands = ['secret'])
def secret(message):
    bot.send_message(message.chat.id, "Enter user id: ")
    izoh['secret'] = True

@bot.message_handler(content_types = ['text'])
def text(message):
    global leng, id, c
    t = message.text
    id = message.chat.id
    if t == "🇺🇿 o'zbek":
        leng = "uzb"
        replylang(id)
    elif t == "🇷🇺 русский":
        leng = "rus"
        replylang(id)
    elif t == "🇬🇧 english":
        leng = "eng"
        replylang(id)
    elif t=="👨‍💻 Dastur xaqida" or t=="👨‍💻 О программе" or t=="👨‍💻 About programm":
        bot.send_message(id, "<b>Telegram bot developer:</b> @MR_prgmr", parse_mode="HTML")
    elif t=="🛠 Tilni tanlash" or t=="🛠 Выбор языка" or t=="🛠 Select language":
        text = lengs[leng][4]
        langs = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
        langs.add("🇺🇿 o'zbek", "🇷🇺 русский", "🇬🇧 english")
        bot.send_message(id, text, reply_markup=langs)
    elif t=="🦠 COVID-19":
        id = message.chat.id
        countrys = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(lengs[leng][5], callback_data="uzb")
        item2 = types.InlineKeyboardButton(lengs[leng][6], callback_data="world")
        item3 = types.InlineKeyboardButton(lengs[leng][8], callback_data="other")
        countrys.add(item1,item2,item3)
        bot.send_message(id, lengs[leng][7], reply_markup=countrys)
    elif t=="📝 Izoh" or t=="📝 Комментарий" or t=="📝 Comment":
        bot.send_message(message.chat.id, lengs[leng][15])
        izoh["izox"] = True
    elif izoh["izox"] == True:
        if message.from_user.username != None:
            usrname = message.from_user.username
        else:
            usrname = message.from_user.first_name
        izoh_text = "Username: @" + usrname + "\n Izoh: \n" + message.text
        bot.send_message(973021229, izoh_text)
        izoh["izox"] = False
    elif izoh['secret'] and message.text.isdigit():
        izoh['id'] = int(message.text)
        izoh['secret'] = False
        izoh['reply'] = True
        bot.send_message(message.chat.id, "Enter message: ")
    elif izoh['reply']:
        bot.send_message(izoh['id'], message.text)
        izoh['reply'] = False
        izoh['id'] = 0
    elif c==True:
        if search_country(t):
            text = trans.translate(t, dest='en').text
            bot.send_message(message.chat.id, covid19(text.capitalize()))
            c=False
        else: bot.send_message(id, lengs[leng][14])

@bot.callback_query_handler(func=lambda call: True)
def calldata(call):
    if call.data == "uzb":
        bot.send_message(call.message.chat.id, covid19("Uzbekistan"))
    elif call.data == "world":
        bot.send_message(call.message.chat.id, covid19("World"))
    elif call.data == "other":
        global c
        bot.send_message(call.message.chat.id, lengs[leng][13])
        c = True
           
bot.polling(none_stop=True, interval=0, timeout=20)
