# -*- coding: utf-8 -*-
import telebot
from telebot import types
import sqlite3
import uuid
import logging
import random
import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
import time

# --- CONFIGURATION HYPEXO SHOP ---
API_TOKEN = '8924489052:AAGpb992PLfB9jV1uOz083EGAFb2gKfeRSg'
ADMIN_IDS = [8382445383]
SHOP_NAME = "HYPEXO SHOP"
MANAGER_USERNAME = "manager_hypexo"
INFO_CHANNEL = "https://t.me/hypeexo"
BOT_USERNAME = "hyepexoo_bot"  

# Direct link to profile image
MAIN_IMG = "https://ibb.co/9ky8Jcvt"

# Realistic BTC/USD rate for payment calculation
BTC_USD_RATE = 70000.0

# Banks for payment (Ukraine and Belarus removed)
BANKS = {
    'Россия': ['Сбербанк', 'Т-Банк', 'Озон Банк', 'ВТБ', 'Альфа-Банк', 'Райффайзен'],
    'Казахстан': ['Kaspi.kz', 'Halyk Bank', 'ForteBank', 'Jusan Bank']
}

ALL_PRODUCT_NAMES = [
    "Гашиш Euro (Classic)", "Гашиш Ice-o-Lator (Top Tier)", "Гашиш Marocco Gold", "Гашиш Afghan Premium", 
    "Гашиш Nepal Stick", "Гашиш Fresh Frozen", "Гашиш Dry Sift",
    "Кокаин VHQ (92% Pure)", "Кокаин Fishscale (Bolivia)", "Кокаин Colombia High Quality", "Кокаин Royal White",
    "Кокаин Peru Premium", "Кокаин Crack (Rocks)",
    "Мефедрон Кристалл (Big Crystal)", "Мефедрон Мука (Classic)", "Мефедрон VHQ (Needle)", "Мефедрон Power Crystal",
    "Мефедрон Кристалл (Emerald)", "Мефедрон Мелкий Кристалл (Sugar)",
    "Амфетамин Sulphate (High Speed)", "Амфетамин Pink Panther", "Амфетамин Euro Speed", 
    "Амфетамин VHQ White", "Амфетамин Фосфат",
    "Шишки AK-47 (Indoor)", "Шишки Amnesia Haze (Extra)", "Шишки Gorilla Glue #4", 
    "Шишки White Widow (Classic)", "Шишки OG Kush (Strong)", "Шишки Lemon Haze (Citrus)", 
    "Шишки Girl Scout Cookies", "Шишки Jack Herer", "Шишки Northern Lights", "Шишки Pineapple Express",
    "Альфа-ПВП Blue Sky", "Альфа-ПВП Crystal Clear", "Альфа-ПВП Flour White", 
    "Альфа-ПВП Red Bull", "Альфа-ПВП Apple Green",
    "МДМА Кристаллы (Pure)", "МДМА Champagne (Gold)", "МДМА Cola Crystal",
    "Экстази Punisher (300mg)", "Экстази Tesla (Orange)", "Экстази Skype (Blue)", 
    "Экстази Burger King", "Экстази Red Bull (Pink)", "Экстази Philipp Plein", "Экстази WhatsApp",
    "ЛСД-25 250мкг (Aztec)", "ЛСД-25 California Sunshine", "ЛСД-25 Hoffman (200мкг)",
    "Грибы Golden Teacher (Dried)", "Грибы McKennaii", "DMT Crystal (Spirit)", 
    "2C-B Nexus (Pink)", "Кетамин S-isomer (Crystal)", "Кетамин Рацемат",
    "Метадон VHQ (Stone)", "Героин Classic (H-1)", "Ксанакс 2мг (Pfizer Style)", 
    "Лирика 300мг", "Трамадол 200мг"
]

COUNTRIES_DATA = {
    'Россия': [
        'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону',
        'Уфа', 'Красноярск', 'Воронеж', 'Пермь', 'Волгоград', 'Краснодар', 'Саратов', 'Тюмень', 'Тольятти', 'Ижевск',
        'Барнаул', 'Ульяновск', 'Иркутск', 'Хабаровск', 'Махачкала', 'Владивосток', 'Ярославль', 'Оренбург', 'Томск', 'Кемерово',
        'Новокузнецк', 'Рязань', 'Набережные Челны', 'Астрахань', 'Пенза', 'Киров', 'Липецк', 'Чебоксары', 'Балашиха', 'Калининград', 'Сочи',
        'Тула', 'Курск', 'Севастополь', 'Улан-Удэ', 'Ставрополь', 'Магнитогорск', 'Тверь', 'Иваново', 'Брянск', 'Белгород', 'Сургут', 'Владимир',
        'Нижний Тагил', 'Архангельск', 'Чита', 'Калуга', 'Смоленск', 'Волжский', 'Курган', 'Череповец', 'Орёл', 'Саранск', 'Вологда', 'Якутск',
        'Владикавказ', 'Мурманск', 'Грозный', 'Тамбов', 'Стерлитамак', 'Кострома', 'Петрозаводск', 'Йошкар-Ола', 'Новороссийск', 'Комсомольск-на-Амуре',
        'Таганрог', 'Сыктывкар', 'Нальчик', 'Шахты', 'Братск', 'Дзержинск', 'Орск', 'Ангарск', 'Благовещенск', 'Энгельс', 'Старый Оскол', 'Великий Новгород',
        'Псков', 'Бийск', 'Прокопьевск', 'Рыбинск', 'Балаково', 'Южно-Сахалинск', 'Армавир', 'Северодвинск', 'Королёв', 'Петропавловск-Камчатский', 'Норильск'
    ],
    'Казахстан': [
        'Алматы', 'Астана', 'Шымкент', 'Актобе', 'Караганда', 'Тараз', 'Усть-Каменогорск', 'Павлодар', 'Атырау', 'Семей',
        'Кызылорда', 'Костанай', 'Актау', 'Уральск', 'Петропавловск', 'Туркестан', 'Темиртау', 'Талдыкорган', 'Кокшетау', 'Жанаозен',
        'Экибастуз', 'Рудный', 'Кентау', 'Балхаш', 'Сатпаев', 'Кульсары', 'Жезказган', 'Талгар', 'Каскелен', 'Степногорск',
        'Щучинск', 'Риддер', 'Приозерск', 'Аральск', 'Аягоз', 'Сарань', 'Лисаковск', 'Житикара', 'Шу', 'Аркалык', 'Байконур',
        'Аксай', 'Атбасар', 'Жаркент', 'Каратау', 'Ленгер', 'Макинск', 'Сарканд', 'Сарыагаш', 'Текели', 'Хромтау', 'Шалкар', 'Шемонаиха',
        'Есик', 'Карабулак', 'Уштобе', 'Шолаккорган', 'Кордай', 'Мерке', 'Шардара', 'Жетысай', 'Айтеке Би', 'Карасу'
    ]
}

COUNTRIES_KEYS = list(COUNTRIES_DATA.keys())

EXCHANGE_RATES = {'KZT': 920.0, 'RUB': 75.0, 'USD': 1.0}
CURRENCY_MAP = {'Казахстан': 'KZT', 'Россия': 'RUB'}

def get_payment_methods(country):
    banks = BANKS.get(country, ['Карта любого банка'])
    return ['BTC (Bitcoin)'] + banks

def generate_1000_reviews():
    r_gen = random.Random(1337)
    p_perfect_start = ["Снял в касание", "Забрал быстро", "Наход моментальный", "Снял чётко по метке", "Поднял без проблем", "Квест простой", "Забрал за секунду", "Снято аккуратно", "Нашёл сразу", "Изи наход", "Все на месте", "Клад дома", "Забрал по красоте", "Снял без палева", "Квест 10/10", "На месте был быстро"]
    p_perfect_middle = [", место надежное", ", локация тихая", ", без лишних глаз", ", координаты точные", ", спрятано грамотно", ", курьер профи", ", место идеальное", ", чайки мимо", ", тайник супер", ", шкуроходы не найдут", ", район спокойный", ", метка совпадает 100%"]
    p_perfect_end = [". Качество вышка!", ". Стафф просто огонь.", ". Вес ровный, спасибо.", ". Эффект пушка.", ". Магазину респект.", ". Буду брать еще.", ". Упаковка вакуум.", ". Все на высшем уровне.", ". Товар отличный.", ". Рекомендую данный шоп!", ". Стафф рабочий, советую.", ". Вернусь еще не раз."]
    
    p_neutral_start = ["Пришлось немного поискать", "Клад был далековато", "Место людное, но забрал", "Курьер прикопал глубоковато", "Координаты немного косили, но нашел", "Пришлось попотеть на месте, но поднял", "Локация немного шумная, но квест пройден", "Были сомнения по метке, но все окей"]
    p_neutral_middle = [", но описание помогло разобраться", ", курьеру стоит быть аккуратнее с выбором места", ", упаковка спасла от сырости", ", место не самое простое для съема", ", в итоге все обошлось благополучно", ", спрятано на совесть"]
    p_neutral_end = [". Главное качество порадовало.", ". Товар рабочий, так что без обид.", ". Вес ровный, качество на уровне.", ". В следующий раз делайте место потише.", ". Магазу спасибо, что не обманули.", ". Качество бомба, компенсировало поиски."]

    reviews_list = []
    while len(reviews_list) < 900:
        s = r_gen.choice(p_perfect_start)
        m = r_gen.choice(p_perfect_middle)
        e = r_gen.choice(p_perfect_end)
        rev = s + m + e
        if rev not in reviews_list:
            reviews_list.append(rev)
            
    while len(reviews_list) < 1000:
        s = r_gen.choice(p_neutral_start)
        m = r_gen.choice(p_neutral_middle)
        e = r_gen.choice(p_neutral_end)
        rev = s + m + e
        if rev not in reviews_list:
            reviews_list.append(rev)
            
    r_gen.shuffle(reviews_list)
    return reviews_list

PREMADE_REVIEWS = generate_1000_reviews()

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(API_TOKEN)

def get_districts_for_city(city_name):
    major_districts = {
        'Москва': ['Арбат', 'Тверской', 'Замоскворечье', 'Хамовники'],
        'Санкт-Петербург': ['Центральный', 'Адмиралтейский', 'Петроградский', 'Василеостровский'],
        'Новосибирск': ['Заельцовский', 'Железнодорожный', 'Калининский', 'Дзержинский'],
        'Екатеринбург': ['Академический', 'Верх-Исетский', 'Железнодорожный', 'Октябрьский'],
        'Казань': ['Ново-Савиновский', 'Авиастроительный', 'Московский', 'Кировский'],
        'Нижний Новгород': ['Нижегородский', 'Канавинский', 'Приокский', 'Московский'],
        'Челябинск': ['Курчатовский', 'Металлургический', 'Тракторозаводский', 'Советский'],
        'Самара': ['Железнодорожный', 'Куйбышевский', 'Ленинский', 'Красноглинский'],
        'Ростов-на-Дону': ['Ленинский', 'Пролетарский', 'Железнодорожный', 'Советский'],
        'Омск': ['Советский', 'Центральный', 'Кировский', 'Октябрьский'],
        'Уфа': ['Кировский', 'Орджоникидзевский', 'Калининский', 'Октябрьский'],
        'Красноярск': ['Центральный', 'Советский', 'Свердловский', 'Октябрьский'],
        'Воронеж': ['Центральный', 'Коминтерновский', 'Ленинский', 'Левобережный'],
        'Пермь': ['Ленинский', 'Свердловский', 'Мотовилихинский', 'Индустриальный'],
        'Волгоград': ['Центральный', 'Ворошиловский', 'Дзержинский', 'Красногвардейский'],
        'Краснодар': ['Центральный', 'Прикубанский', 'Карасунский', 'Западный'],
        'Сочи': ['Центральный', 'Адлерский', 'Хостинский', 'Лазаревский'],
        'Севастополь': ['Ленинский', 'Гагаринский', 'Нахимовский', 'Балаклавский'],
        'Тольятти': ['Автозаводский', 'Центральный', 'Комсомольский'],
        'Ижевск': ['Октябрьский', 'Первомайский', 'Индустриальный', 'Ленинский'],
        'Барнаул': ['Центральный', 'Ленинский', 'Октябрьский', 'Индустриальный'],
        'Ульяновск': ['Ленинский', 'Засвияжский', 'Заволжский', 'Железнодорожный'],
        'Иркутск': ['Правобережный', 'Октябрьский', 'Свердловский', 'Ленинский'],
        'Хабаровск': ['Центральный', 'Кировский', 'Краснофлотский', 'Железнодорожный'],
        'Владивосток': ['Ленинский', 'Первомайский', 'Фрунзенский', 'Советский'],
        'Ярославль': ['Кировский', 'Ленинский', 'Дзержинский', 'Заволжский'],
        'Калининград': ['Центральный', 'Ленинградский', 'Московский'],
        'Махачкала': ['Ленинский', 'Советский', 'Кировский'],
        'Грозный': ['Ахматовский', 'Байсангуровский', 'Висаитовский', 'Шейх-Мансуровский'],
        'Набережные Челны': ['Автозаводский', 'Центральный', 'Комсомольский'],
        'Астрахань': ['Кировский', 'Советский', 'Ленинский', 'Трусовский'],
        'Пенза': ['Железнодорожный', 'Ленинский', 'Октябрьский', 'Первомайский'],
        'Киров': ['Ленинский', 'Октябрьский', 'Первомайский', 'Нововятский'],
        'Липецк': ['Правобережный', 'Левобережный', 'Октябрьский', 'Советский'],
        'Чебоксары': ['Калининский', 'Ленинский', 'Московский'],
        'Рязань': ['Московский', 'Октябрьский', 'Советский', 'Железнодорожный'],
        'Курск': ['Центральный', 'Сеймский', 'Железнодорожный'],
        'Ставрополь': ['Ленинский', 'Октябрьский', 'Промышленный'],
        'Магнитогорск': ['Ленинский', 'Правобережный', 'Орджоникидзевский'],
        'Тверь': ['Заволжский', 'Московский', 'Пролетарский', 'Центральный'],
        'Иваново': ['Фрунзенский', 'Октябрьский', 'Ленинский', 'Советский'],
        'Брянск': ['Бежицкий', 'Володарский', 'Советский', 'Фокинский'],
        'Белгород': ['Восточный', 'Западный'],
        'Сургут': ['Центральный', 'Северный', 'Северо-Восточный', 'Восточный'],
        'Владимир': ['Ленинский', 'Октябрьский', 'Фрунзенский'],
        'Алматы': ['Медеуский', 'Бостандыкский', 'Алмалинский', 'Ауэзовский'],
        'Астана': ['Есиль', 'Алматы', 'Сарыарка', 'Байконур'],
        'Шымкент': ['Абайский', 'Аль-Фарабийский', 'Енбекшинский', 'Каратауский'],
        'Караганда': ['Казыбек би', 'Алихана Бокейхана', 'Юго-Восток'],
        'Павлодар': ['Центральный', 'Дачный', 'Химгородки', 'Усольский'],
        'Актобе': ['Алматы', 'Астана', 'Жилгородок', 'Шанхай'],
        'Атырау': ['Авангард', 'Привокзальный', 'Жилгородок', 'Нурсая']
    }
    
    city_clean = city_name.strip()
    if city_clean in major_districts:
        return major_districts[city_clean]
    
    return ['Центральный район', 'Южный район', 'Восточный район', 'Западный район']

class Database:
    def __init__(self):
        self.db_path = 'shop_v5.db'
        self.create_tables()
        self.init_data()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=20.0)

    def create_tables(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS users (uid INTEGER PRIMARY KEY, city TEXT, country TEXT, district TEXT, joined TEXT, balance REAL DEFAULT 0.0, referrer_id INTEGER)')
            cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)')
            cursor.execute('CREATE TABLE IF NOT EXISTS stock (city TEXT, product_id INTEGER, PRIMARY KEY(city, product_id))')
            cursor.execute('CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, prod TEXT)')
            cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, val TEXT)')
            cursor.execute('CREATE TABLE IF NOT EXISTS promocodes (code TEXT PRIMARY KEY, discount INTEGER, expires_at TEXT)')
            cursor.execute('CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT, uid INTEGER, product_id INTEGER, weight_idx TEXT, district TEXT)')
            
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN district TEXT")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN balance REAL DEFAULT 0.0")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE users ADD COLUMN referrer_id INTEGER")
            except sqlite3.OperationalError:
                pass
            try:
                cursor.execute("ALTER TABLE promocodes ADD COLUMN expires_at TEXT DEFAULT 'eternal'")
            except sqlite3.OperationalError:
                pass
                
            conn.commit()

    def init_data(self):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            if cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
                for name in ALL_PRODUCT_NAMES:
                    n_lower = name.lower()
                    if "гашиш" in n_lower:
                        price = float(random.randint(29, 34))
                    elif "кокаин" in n_lower:
                        price = float(random.randint(40, 51))
                    elif "мефедрон" in n_lower or "мет" in n_lower:
                        price = float(random.randint(30, 35))
                    else:
                        price = float(random.randint(30, 40))
                    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
            
            if cursor.execute("SELECT COUNT(*) FROM reviews").fetchone()[0] == 0:
                self._shuffle_reviews_internal(conn)
            
            if cursor.execute("SELECT COUNT(*) FROM stock").fetchone()[0] == 0:
                self._shuffle_stock_internal(conn)
                
            cursor.execute("INSERT OR IGNORE INTO promocodes (code, discount, expires_at) VALUES ('HYP5', 5, 'eternal')")
            conn.commit()

    def _shuffle_reviews_internal(self, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reviews")
        sampled_revs = random.sample(PREMADE_REVIEWS, 100)
        for txt in sampled_revs:
            cursor.execute("INSERT INTO reviews (text, prod) VALUES (?,?)", (txt, random.choice(ALL_PRODUCT_NAMES)))

    def _shuffle_stock_internal(self, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stock")
        p_ids = [r[0] for r in cursor.execute("SELECT id FROM products").fetchall()]
        for country, cities in COUNTRIES_DATA.items():
            for city in cities:
                count_to_pick = random.randint(20, 28)
                for pid in random.sample(p_ids, min(count_to_pick, len(p_ids))):
                    cursor.execute("INSERT OR IGNORE INTO stock (city, product_id) VALUES (?,?)", (city, pid))

    def shuffle_stock(self):
        with self._get_conn() as conn:
            self._shuffle_stock_internal(conn)
            conn.commit()

    def shuffle_reviews(self):
        with self._get_conn() as conn:
            self._shuffle_reviews_internal(conn)
            conn.commit()

    def execute(self, query, params=()):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def fetchall(self, query, params=()):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    def fetchone(self, query, params=()):
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

db = Database()

def get_main_kb(uid):
    cart_count_row = db.fetchone("SELECT COUNT(*) FROM cart WHERE uid=?", (uid,))
    cart_count = cart_count_row[0] if cart_count_row else 0
    cart_label = f"Корзина ({cart_count})" if cart_count > 0 else "Корзина (Пусто)"

    m = types.InlineKeyboardMarkup(row_width=2)
    m.row(
        types.InlineKeyboardButton("Каталог", callback_data="shop_0"),
        types.InlineKeyboardButton(cart_label, callback_data="view_cart")
    )
    m.row(
        types.InlineKeyboardButton("Локации", callback_data="loc"),
        types.InlineKeyboardButton("Бонусы", callback_data="bonuses")
    )
    m.row(
        types.InlineKeyboardButton("Работа ↗", url="https://t.me/jobhypexo"),
        types.InlineKeyboardButton("Отзывы", callback_data="rev_list_0")
    )
    m.row(
        types.InlineKeyboardButton("FAQ / Помощь", callback_data="faq_menu")
    )
    m.row(
        types.InlineKeyboardButton("Информация ↗", url=INFO_CHANNEL),
        types.InlineKeyboardButton("Поддержка ↗", url=f"https://t.me/{MANAGER_USERNAME}")
    )
    if uid in ADMIN_IDS:
        m.row(types.InlineKeyboardButton("Панель управления", callback_data="admin_main"))
    return m

def build_profile_caption(uid, country_text, city_text, district_text):
    balance_row = db.fetchone("SELECT balance FROM users WHERE uid=?", (uid,))
    balance = balance_row[0] if balance_row and balance_row[0] is not None else 0.0
    
    actual_rev_count = db.fetchone("SELECT COUNT(*) FROM reviews")[0]
    total_reviews_display = f"{27523 + actual_rev_count:,}".replace(",", " ")
    
    caption = (
        f"ЛИЧНЫЙ КАБИНЕТ ПОЛЬЗОВАТЕЛЯ\n"
        f"--------------------------------------------------\n\n"
        f"Рейтинг шопа: 27.523 ({total_reviews_display} шт.)\n"
        f"Ваш личный рейтинг: 5.00 (0 шт.)\n\n"
        f"Текущая геолокация:\n"
        f" - Страна: {country_text}\n"
        f" - Город: {city_text}\n"
        f" - Район: {district_text}\n\n"
        f"Ваша статистика:\n"
        f" - Всего покупок: 0 шт.\n"
        f" - Ваша скидка: 0 %\n\n"
        f"Доступный бонус: {balance:.2f} USD\n\n"
        f"--------------------------------------------------"
    )
    return caption

def safe_edit_text(chat_id, message_id, text, reply_markup=None, parse_mode="HTML"):
    try:
        bot.edit_message_caption(caption=text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode=parse_mode)
    except Exception:
        try:
            bot.edit_message_text(text=text, chat_id=chat_id, message_id=message_id, reply_markup=reply_markup, parse_mode=parse_mode)
        except Exception:
            try:
                bot.delete_message(chat_id, message_id)
            except Exception:
                pass
            try:
                bot.send_photo(chat_id, MAIN_IMG, caption=text, reply_markup=reply_markup, parse_mode=parse_mode)
            except Exception:
                bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)

def show_main_menu(cid, mid, uid):
    u = db.fetchone("SELECT city, country, district FROM users WHERE uid=?", (uid,))
    city_text = u[0] if u and u[0] else "Не указан"
    country_text = u[1] if u and u[1] else "Не указана"
    district_text = u[2] if u and u[2] else "Не указан"
    
    profile_caption = build_profile_caption(uid, country_text, city_text, district_text)
    safe_edit_text(cid, mid, profile_caption, get_main_kb(uid))

@bot.message_handler(commands=['start'])
def handle_start(m):
    uid = m.from_user.id
    is_new = db.fetchone("SELECT uid FROM users WHERE uid=?", (uid,)) is None
    
    args = m.text.split()
    referrer_id = None
    ref_message = ""
    
    if len(args) > 1 and args[1].startswith("r_"):
        try:
            ref_val = int(args[1].replace("r_", ""))
            if ref_val != uid:
                referrer_id = ref_val
        except ValueError:
            pass

    if is_new:
        start_balance = 500.0 if uid in ADMIN_IDS else 0.0
        db.execute("INSERT INTO users (uid, joined, balance, referrer_id) VALUES (?,?,?,?)", 
                   (uid, datetime.now().strftime("%Y-%m-%d"), start_balance, referrer_id))
        
        if referrer_id:
            db.execute("UPDATE users SET balance = balance + 0.5 WHERE uid=?", (referrer_id,))
            ref_message = "Вы успешно вошли по реферальной ссылке! Нам очень приятно, что вы с нами!\n\n"
            try:
                bot.send_message(referrer_id, f"По вашей ссылке зарегистрировался новый пользователь! Баланс пополнен на 0.50 USD.", parse_mode="HTML")
            except Exception:
                pass
    else:
        db.execute("INSERT OR IGNORE INTO users (uid, joined) VALUES (?,?)", (uid, datetime.now().strftime("%Y-%m-%d")))
        
        if uid in ADMIN_IDS:
            curr_bal = db.fetchone("SELECT balance FROM users WHERE uid=?", (uid,))
            if curr_bal and curr_bal[0] < 500.0:
                db.execute("UPDATE users SET balance = 500.0 WHERE uid=?", (uid,))
        
        if len(args) > 1 and args[1].startswith("r_"):
            try:
                bot.send_message(m.chat.id, "Вы уже зарегистрированы в системе! Реферальная ссылка действительна только для новых пользователей.", parse_mode="HTML")
            except Exception:
                pass
    
    u = db.fetchone("SELECT city, country, district FROM users WHERE uid=?", (uid,))
    city_text = u[0] if u and u[0] else "Не указан"
    country_text = u[1] if u and u[1] else "Не указана"
    district_text = u[2] if u and u[2] else "Не указан"
    
    profile_caption = ref_message + build_profile_caption(uid, country_text, city_text, district_text)
    
    try:
        bot.send_photo(m.chat.id, MAIN_IMG, caption=profile_caption, reply_markup=get_main_kb(uid), parse_mode="HTML")
    except Exception:
        bot.send_message(m.chat.id, profile_caption, reply_markup=get_main_kb(uid), parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: True)
def handle_cb(c):
    uid, cid, mid, data = c.from_user.id, c.message.chat.id, c.message.message_id, c.data

    if data == "to_main":
        show_main_menu(cid, mid, uid)

    elif data == "faq_menu":
        faq_text = (
            f"ИНТЕРАКТИВНЫЙ РАЗДЕЛ ПОДДЕРЖКИ (FAQ) {SHOP_NAME}\n"
            f"--------------------------------------------------\n\n"
            f"Приветствуем! В этом разделе собраны ответы на 80% типовых вопросов, с которыми сталкиваются наши пользователи.\n\n"
            f"Пожалуйста, выберите интересующую вас категорию, нажав на кнопку ниже. "
            f"Это поможет вам моментально решить проблему без привлечения живого менеджера."
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Как оплатить заказ?", callback_data="faq_how_to_pay"),
            types.InlineKeyboardButton("Что делать, если ненаход?", callback_data="faq_not_found"),
            types.InlineKeyboardButton("Сроки доставки и выдачи?", callback_data="faq_delivery_time"),
            types.InlineKeyboardButton("Конфиденциальность и безопасность", callback_data="faq_security"),
            types.InlineKeyboardButton("Не нашли свой вопрос? Поддержка ↗", url=f"https://t.me/{MANAGER_USERNAME}"),
            types.InlineKeyboardButton("Назад", callback_data="to_main")
        )
        safe_edit_text(cid, mid, faq_text, m)

    elif data == "faq_how_to_pay":
        pay_text = (
            f"КАК ОПЛАТИТЬ ЗАКАЗ? — ИНСТРУКЦИЯ\n"
            f"--------------------------------------------------\n\n"
            f"Для максимальной безопасности мы принимаем два основных метода оплаты:\n\n"
            f"1. Криптовалюта Bitcoin (BTC):\n"
            f"- Полностью автоматический способ. Выбирайте оплату через BTC в чеке;\n"
            f"- Бот рассчитает сумму в сатоши по текущему курсу;\n"
            f"- Переведите монеты на адрес кошелька, и после 1-го подтверждения бот выдаст заказ.\n\n"
            f"2. Банковская карта:\n"
            f"- Оформите заказ, выбрав нужный банк в списке;\n"
            f"- Бот сформирует чек. Скопируйте его и отправьте оператору @{MANAGER_USERNAME};\n"
            f"- Оператор выдаст свежие реквизиты. После подтверждения оплаты в течение 10-20 минут будут выданы координаты с подробным фото и описанием места.\n\n"
            f"Не задерживайте оплату после получения реквизитов! Время жизни реквизитов карт — 10 минут."
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Назад к FAQ", callback_data="faq_menu"),
            types.InlineKeyboardButton("Главное меню", callback_data="to_main")
        )
        safe_edit_text(cid, mid, pay_text, m)

    elif data == "faq_not_found":
        nf_text = (
            f"ЧТО ДЕЛАТЬ, ЕСЛИ НЕ НАШЛИ КЛАД?\n"
            f"--------------------------------------------------\n\n"
            f"Самое главное — сохраняйте спокойствие. Мы дорожим клиентами и всегда помогаем в спорных ситуациях. Следуйте инструкции:\n\n"
            f"1. Проверьте правильность поисков:\n"
            f"- Убедитесь, что вы находитесь именно на тех координатах. Сравните ориентиры с фото курьера;\n"
            f"- Обязательно используйте камеру NoteCam (она фиксирует точное время и GPS-координаты на снимке).\n\n"
            f"2. Сделайте фотографии:\n"
            f"- Сделайте минимум 2 качественных фото с тех же ракурсов, что и на фото курьера: вблизи (место раскопа) и издалека (общий план);\n"
            f"- На фото не должно быть посторонних людей, ваших пальцев у объектива или смазанных деталей.\n\n"
            f"3. Создайте обращение:\n"
            f"- Передайте фотографии и ваш Чек заказа менеджеру @{MANAGER_USERNAME};\n"
            f"- Обращения принимаются строго в течение 24 часов с момента покупки. Диспуты рассматриваются индивидуально. Будьте вежливы!"
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Назад к FAQ", callback_data="faq_menu"),
            types.InlineKeyboardButton("Главное меню", callback_data="to_main")
        )
        safe_edit_text(cid, mid, nf_text, m)

    elif data == "faq_delivery_time":
        dt_text = (
            f"СРОКИ ВЫДАЧИ И ДОСТАВКИ\n"
            f"--------------------------------------------------\n\n"
            f"Мгновенные готовые клады:\n"
            f"Все позиции, доступные в каталоге нашего бота, уже надежно заложены нашими профессиональными курьерами в указанных районах и городах. Вы получаете точные координаты, метку на карте и подробное описание места моментально после подтверждения транзакции.\n\n"
            f"Индивидуальная доставка в любой город/район:\n"
            f"Если вы не нашли нужный район или вашего населенного пункта нет в списке — не волнуйтесь! Мы осуществляем оперативную заказную доставку в любую точку:\n"
            f"- Отправка посылок (Почта / СДЭК) производится в течение 24-48 часов с использованием профессиональной маскировки (стелс), исключающей любые подозрения;\n"
            f"- Также возможен индивидуальный предзаказ на закладку в удобном для вас районе через согласование с менеджером."
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Назад к FAQ", callback_data="faq_menu"),
            types.InlineKeyboardButton("Главное меню", callback_data="to_main")
        )
        safe_edit_text(cid, mid, dt_text, m)

    elif data == "faq_security":
        sec_text = (
            f"БЕЗОПАСНОСТЬ И АНОНИМНОСТЬ\n"
            f"--------------------------------------------------\n\n"
            f"Мы гарантируем полную безопасность при взаимодействии с {SHOP_NAME}:\n\n"
            f"- Удаление данных и анонимность: Вся информация о ваших покупках, адресах и локациях мгновенно шифруется на сервере. Логи диалогов с ботом и история запросов безвозвратно удаляются автоматически в целях вашей безопасности.\n\n"
            f"- Безопасные транзакции по картам: При оплате банковской картой все платежи проходят через зашифрованные транзитные шлюзы. Данные вашей личной карты нигде не сохраняются, а история переводов автоматически аннулируется банком-партнером сразу после подтверждения транзакции.\n\n"
            f"- Анонимные крипто-кошельки: Все блокчейн-платежи (BTC) автоматически направляются через каскадные миксеры высокой степени очистки, что делает отслеживание конечного отправителя абсолютно невозможным.\n\n"
            f"- Рекомендация по безопасности: Для максимального уровня конфиденциальности мы настоятельно советуем использовать надежный VPN/Proxy-сервис при работе с Telegram, а также установить облачный пароль (Two-Step Verification) на ваш аккаунт."
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Назад к FAQ", callback_data="faq_menu"),
            types.InlineKeyboardButton("Главное меню", callback_data="to_main")
        )
        safe_edit_text(cid, mid, sec_text, m)

    elif data == "bonuses":
        ref_count = db.fetchone("SELECT COUNT(*) FROM users WHERE referrer_id=?", (uid,))[0]
        balance_row = db.fetchone("SELECT balance FROM users WHERE uid=?", (uid,))
        balance = balance_row[0] if balance_row and balance_row[0] is not None else 0.0

        bonus_text = (
            f"МНОГОУРОВНЕВАЯ БОНУСНАЯ ПРОГРАММА {SHOP_NAME}\n"
            f"--------------------------------------------------\n\n"
            f"Добро пожаловать в нашу щедрую партнерскую систему! Мы выплачиваем реальные вознаграждения за рекомендации.\n\n"
            f"Как это работает?\n"
            f"1. Вы делитесь своей персональной ссылкой с друзьями.\n"
            f"2. За каждого пользователя, перешедшего по ней и запустившего бота, вам мгновенно начисляется 0.50 USD!\n"
            f"3. Дополнительно вы получаете 3% от всех покупок ваших приглашенных рефералов.\n\n"
            f"Ваша статистика приглашений:\n"
            f" - Приглашено человек: {ref_count} чел.\n"
            f" - Доступный баланс: {balance:.2f} USD\n\n"
            f"Магазин промокодов:\n"
            f"Вы можете обменять свой накопленный реферальный баланс на личные промокоды со скидкой до 20%!\n\n"
            f"Ваша персональная партнерская ссылка:\n"
            f"https://t.me/{BOT_USERNAME}?start=r_{uid}\n"
            f"--------------------------------------------------"
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Купить промокод", callback_data="buy_promo_store"),
            types.InlineKeyboardButton("Назад", callback_data="to_main")
        )
        safe_edit_text(cid, mid, bonus_text, m)

    elif data == "buy_promo_store":
        balance_row = db.fetchone("SELECT balance FROM users WHERE uid=?", (uid,))
        balance = balance_row[0] if balance_row and balance_row[0] is not None else 0.0

        store_text = (
            f"МАГАЗИН СКИДОЧНЫХ ПРОМОКОДОВ\n"
            f"--------------------------------------------------\n"
            f"Ваш текущий баланс: {balance:.2f} USD\n\n"
            f"Выберите нужный вам номинал скидки для покупки:\n"
            f"- Скидка 5% — Стоимость: 5.00 USD (Нужно пригласить 10 человек)\n"
            f"- Скидка 10% — Стоимость: 7.50 USD (Нужно пригласить 15 человек)\n"
            f"- Скидка 20% — Стоимость: 10.00 USD (Нужно пригласить 20 человек)\n\n"
            f"После покупки промокод автоматически запишется в базу данных и станет доступен для ввода при оформлении заказа!"
        )
        m = types.InlineKeyboardMarkup(row_width=2)
        m.add(
            types.InlineKeyboardButton("Скидка 5% ($5.0)", callback_data="buy_promo_action_5"),
            types.InlineKeyboardButton("Скидка 10% ($7.5)", callback_data="buy_promo_action_10")
        )
        m.add(
            types.InlineKeyboardButton("Скидка 20% ($10.0)", callback_data="buy_promo_action_20")
        )
        m.add(types.InlineKeyboardButton("Назад к бонусам", callback_data="bonuses"))
        safe_edit_text(cid, mid, store_text, m)

    elif data.startswith("buy_promo_action_"):
        parts = data.split("_")
        discount = int(parts[3])
        cost = 5.00 if discount == 5 else (7.50 if discount == 10 else 10.00)

        balance_row = db.fetchone("SELECT balance FROM users WHERE uid=?", (uid,))
        balance = balance_row[0] if balance_row and balance_row[0] is not None else 0.0

        if balance >= cost:
            new_balance = balance - cost
            db.execute("UPDATE users SET balance=? WHERE uid=?", (new_balance, uid))
            
            generated_code = f"REF-{discount}-{str(uuid.uuid4())[:6].upper()}"
            db.execute("INSERT INTO promocodes (code, discount) VALUES (?,?)", (generated_code, discount))

            success_text = (
                f"ПОКУПКА УСПЕШНО СОВЕРШЕНА!\n"
                f"--------------------------------------------------\n\n"
                f"Вы успешно приобрели скидочный промокод!\n"
                f"- Списано с баланса: {cost:.2f} USD\n"
                f"- Ваш новый баланс: {new_balance:.2f} USD\n\n"
                f"Ваш промокод на скидку {discount}%:\n"
                f"{generated_code}\n\n"
                f"Скопируйте его и введите при оплате любого товара на чеке заказа для моментального получения скидки!"
            )
            m = types.InlineKeyboardMarkup(row_width=1)
            m.add(
                types.InlineKeyboardButton("В каталог", callback_data="shop_0"),
                types.InlineKeyboardButton("Вернуться в магазин", callback_data="buy_promo_store")
            )
            safe_edit_text(cid, mid, success_text, m)
        else:
            bot.answer_callback_query(c.id, f"Недостаточно средств! Необходимый баланс: {cost} USD. У вас: {balance} USD.", show_alert=True)

    elif data.startswith("rev_list_"):
        parts = data.split("_")
        idx = int(parts[2])
        revs = db.fetchall("SELECT text, prod FROM reviews ORDER BY id DESC")
        if not revs:
            m = types.InlineKeyboardMarkup(row_width=1)
            m.add(types.InlineKeyboardButton("Назад", callback_data="to_main"))
            return safe_edit_text(cid, mid, "Отзывов пока нет.", m)
            
        idx = idx % len(revs)
        r = revs[idx]
        
        actual_rev_count = db.fetchone("SELECT COUNT(*) FROM reviews")[0]
        total_reviews_display = f"{27523 + actual_rev_count:,}".replace(",", " ")
        
        txt = (f"Отзывы клиентов ({total_reviews_display} шт.)\n"
               f"Средняя оценка: 27.523/30.0\n\n"
               f"Автор: Аноним\n"
               f"Товар: {r[1]}\n"
               f"Отзыв: {r[0]}")
        m = types.InlineKeyboardMarkup(row_width=2)
        m.add(
            types.InlineKeyboardButton("Предыдущий", callback_data=f"rev_list_{idx-1}"),
            types.InlineKeyboardButton("Следующий", callback_data=f"rev_list_{idx+1}")
        )
        m.add(types.InlineKeyboardButton("Главное меню", callback_data="to_main"))
        safe_edit_text(cid, mid, txt, m)

    elif data == "loc":
        m = types.InlineKeyboardMarkup(row_width=2)
        for country in COUNTRIES_KEYS:
            m.add(types.InlineKeyboardButton(country, callback_data=f"cnt_{country}_0"))
        m.add(types.InlineKeyboardButton("Назад", callback_data="to_main"))
        safe_edit_text(cid, mid, "Выберите интересующую вас страну:", m)

    elif data.startswith("cnt_"):
        p = data.split("_")
        cnt = p[1]
        page = int(p[2])
        cities = COUNTRIES_DATA[cnt]
        
        start = page * 10
        end = start + 10
        m = types.InlineKeyboardMarkup(row_width=2)
        for city in cities[start:end]:
            cnt_idx = COUNTRIES_KEYS.index(cnt)
            city_idx = COUNTRIES_DATA[cnt].index(city)
            m.add(types.InlineKeyboardButton(city, callback_data=f"set_{cnt_idx}_{city_idx}"))
        
        nav_buttons = []
        if page > 0:
            nav_buttons.append(types.InlineKeyboardButton("Назад", callback_data=f"cnt_{cnt}_{page-1}"))
        if end < len(cities):
            nav_buttons.append(types.InlineKeyboardButton("Вперед", callback_data=f"cnt_{cnt}_{page+1}"))
        if nav_buttons:
            m.add(*nav_buttons)
        
        m.add(types.InlineKeyboardButton("Нет вашего города? Заказать доставку", callback_data="custom_delivery"))
        m.add(types.InlineKeyboardButton("К списку стран", callback_data="loc"))
        safe_edit_text(cid, mid, f"Выберите город в стране {cnt} (страница {page+1}):", m)

    elif data == "custom_delivery":
        delivery_text = (
            "Доставка в любой населенный пункт\n"
            "--------------------------------------------------\n\n"
            "Если вы не нашли свой город в списке доступных локаций, вы можете заказать индивидуальную отправку в ваш регион (почтой или специализированным курьером).\n\n"
            "Для обсуждения деталей и оформления заказа свяжитесь с нашим оператором."
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Написать оператору", url=f"https://t.me/{MANAGER_USERNAME}"),
            types.InlineKeyboardButton("Назад", callback_data="loc")
        )
        safe_edit_text(cid, mid, delivery_text, m)

    elif data.startswith("set_"):
        parts = data.split("_")
        cnt_idx = int(parts[1])
        city_idx = int(parts[2])
        cnt = COUNTRIES_KEYS[cnt_idx]
        city = COUNTRIES_DATA[cnt][city_idx]
        
        districts = get_districts_for_city(city)
        m = types.InlineKeyboardMarkup(row_width=1)
        for d_idx, dist in enumerate(districts):
            m.add(types.InlineKeyboardButton(dist, callback_data=f"sd_{cnt_idx}_{city_idx}_{d_idx}"))
        m.add(types.InlineKeyboardButton("Назад к выбору городов", callback_data=f"cnt_{cnt}_0"))
        safe_edit_text(cid, mid, f"Выберите район в городе {city}:", m)

    elif data.startswith("sd_"):
        parts = data.split("_")
        cnt_idx = int(parts[1])
        city_idx = int(parts[2])
        d_idx = int(parts[3])
        cnt = COUNTRIES_KEYS[cnt_idx]
        city = COUNTRIES_DATA[cnt][city_idx]
        district = get_districts_for_city(city)[d_idx]
        
        db.execute("UPDATE users SET city=?, country=?, district=? WHERE uid=?", (city, cnt, district, uid))
        bot.answer_callback_query(c.id, f"Установлен район: {district}")
        show_main_menu(cid, mid, uid)

    elif data.startswith("shop_"):
        parts = data.split("_")
        page = int(parts[1])
        u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
        if not u or not u[0]:
            return bot.answer_callback_query(c.id, "Сначала выберите локацию!", show_alert=True)
        
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        prods = db.fetchall("SELECT p.id, p.name, p.price FROM products p JOIN stock s ON p.id = s.product_id WHERE s.city = ?", (u[0],))
        
        items_per_page = 4
        start = page * items_per_page
        end = start + items_per_page
        page_prods = prods[start:end]
        
        m = types.InlineKeyboardMarkup(row_width=1)
        for pid, name, price in page_prods:
            m.add(types.InlineKeyboardButton(f"{name.upper()} — {round(price*rate, 1)} {curr}", callback_data=f"buy_{pid}"))
        
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("Назад", callback_data=f"shop_{page-1}"))
        if end < len(prods):
            nav.append(types.InlineKeyboardButton("Вперед", callback_data=f"shop_{page+1}"))
        if nav:
            m.row(*nav)
            
        m.add(types.InlineKeyboardButton("В главное меню", callback_data="to_main"))
        safe_edit_text(cid, mid, f"Каталог позиций для города {u[0]} (стр. {page+1}):", m)

    elif data.startswith("buy_"):
        parts = data.split("_")
        pid = parts[1]
        p = db.fetchone("SELECT name, price FROM products WHERE id=?", (pid,))
        u = db.fetchone("SELECT city, country, district FROM users WHERE uid=?", (uid,))
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        
        m = types.InlineKeyboardMarkup(row_width=1)
        for w_label, w_idx in [("1г", "1"), ("2г", "2"), ("3г", "3"), ("5г", "5")]:
            mult = 1 if w_idx == "1" else (1.9 if w_idx == "2" else (2.8 if w_idx == "3" else 4.2))
            p_val = round(p[1]*mult*rate, 1)
            m.add(types.InlineKeyboardButton(f"{w_label} — {p_val} {curr}", callback_data=f"sel_act_{pid}_{w_idx}"))
        m.add(types.InlineKeyboardButton("К каталогу", callback_data="shop_0"))
        
        full_info = (
            f"Товар: {p[0]}\n\n"
            f"Выберите интересующий вес:"
        )
        safe_edit_text(cid, mid, full_info, m)

    elif data.startswith("sel_act_"):
        parts = data.split("_")
        pid = parts[2]
        w_idx = parts[3]
        p = db.fetchone("SELECT name, price FROM products WHERE id=?", (pid,))
        u = db.fetchone("SELECT city, country, district FROM users WHERE uid=?", (uid,))
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        mult = 1 if w_idx == "1" else (1.9 if w_idx == "2" else (2.8 if w_idx == "3" else 4.2))
        p_val = round(p[1]*mult*rate, 1)
        
        text = (
            f"Товар: {p[0]}\n"
            f"Выбранный вес: {w_idx}г\n"
            f"Стоимость: {p_val} {curr}\n"
            f"Район: {u[2] if u[2] else 'Не выбран'}\n\n"
            f"Выберите дальнейшее действие:"
        )
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Продолжить оформление заказа", callback_data=f"rn_{pid}_{w_idx}_0"),
            types.InlineKeyboardButton("Добавить в корзину", callback_data=f"add_to_cart_{pid}_{w_idx}"),
            types.InlineKeyboardButton("Изменить вес", callback_data=f"buy_{pid}")
        )
        safe_edit_text(cid, mid, text, m)

    elif data.startswith("add_to_cart_"):
        parts = data.split("_")
        pid = parts[3]
        w_idx = parts[4]
        p = db.fetchone("SELECT name FROM products WHERE id=?", (pid,))
        u = db.fetchone("SELECT district FROM users WHERE uid=?", (uid,))
        district = u[0] if u and u[0] else "Не указан"
        
        db.execute("INSERT INTO cart (uid, product_id, weight_idx, district) VALUES (?, ?, ?, ?)", (uid, pid, w_idx, district))
        
        text = (
            f"Товар {p[0]} ({w_idx}г) успешно добавлен в вашу корзину!\n\n"
            f"Вы можете продолжить выбор товаров в каталоге или перейти к оформлению заказа всей корзины одним общим чеком."
        )
        m = types.InlineKeyboardMarkup(row_width=2)
        m.row(
            types.InlineKeyboardButton("В корзину", callback_data="view_cart"),
            types.InlineKeyboardButton("Продолжить покупки", callback_data="shop_0")
        )
        m.row(types.InlineKeyboardButton("На главную", callback_data="to_main"))
        safe_edit_text(cid, mid, text, m)

    elif data == "view_cart":
        u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
        if not u or not u[0]:
            return bot.answer_callback_query(c.id, "Сначала выберите локацию!", show_alert=True)
        
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        
        cart_items = db.fetchall("SELECT c.id, p.name, p.price, c.weight_idx, c.district FROM cart c JOIN products p ON c.product_id = p.id WHERE c.uid = ?", (uid,))
        
        if not cart_items:
            m = types.InlineKeyboardMarkup(row_width=1)
            m.add(
                types.InlineKeyboardButton("В каталог", callback_data="shop_0"),
                types.InlineKeyboardButton("Главное меню", callback_data="to_main")
            )
            return safe_edit_text(cid, mid, "Ваша корзина пуста!\n\nПерейдите в каталог, чтобы добавить товары.", m)
        
        total_price = 0.0
        text = "СОДЕРЖИМОЕ ВАШЕЙ КОРЗИНЫ\n"
        text += f"Локация: {u[0]} ({u[1]})\n"
        text += "--------------------------------------------------\n\n"
        
        for idx, (cart_id, name, price, w_idx, dist) in enumerate(cart_items, 1):
            mult = 1 if w_idx == "1" else (1.9 if w_idx == "2" else (2.8 if w_idx == "3" else 4.2))
            item_price = round(price * mult * rate, 1)
            total_price += item_price
            
            text += f"{idx}. Товар: {name} ({w_idx}г)\n"
            text += f" - Район: {dist}\n"
            text += f" - Стоимость: {item_price} {curr}\n\n"
            
        text += "--------------------------------------------------\n"
        text += f"ИТОГО К ОПЛАТЕ: {total_price:.1f} {curr}"
        
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Оформить общий заказ", callback_data="cart_checkout_delivery"),
            types.InlineKeyboardButton(f"Товары ({len(cart_items)} поз.)", callback_data="cart_items_list"),
            types.InlineKeyboardButton("Продолжить покупки", callback_data="shop_0"),
            types.InlineKeyboardButton("Главное меню", callback_data="to_main")
        )
        
        safe_edit_text(cid, mid, text, m)

    elif data == "cart_items_list":
        u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        
        cart_items = db.fetchall("SELECT c.id, p.name, p.price, c.weight_idx, c.district FROM cart c JOIN products p ON c.product_id = p.id WHERE c.uid = ?", (uid,))
        
        if not cart_items:
            m = types.InlineKeyboardMarkup(row_width=1)
            m.add(types.InlineKeyboardButton("Назад в корзину", callback_data="view_cart"))
            return safe_edit_text(cid, mid, "Ваша корзина пуста!", m)
            
        text = "СПИСОК ТОВАРОВ В КОРЗИНЕ\nЗдесь вы можете точечно удалить любой товар или полностью очистить корзину:\n\n"
        
        m = types.InlineKeyboardMarkup(row_width=1)
        for idx, (cart_id, name, price, w_idx, dist) in enumerate(cart_items, 1):
            mult = 1 if w_idx == "1" else (1.9 if w_idx == "2" else (2.8 if w_idx == "3" else 4.2))
            item_price = round(price * mult * rate, 1)
            text += f"- {name} ({w_idx}г) — {item_price} {curr}\n"
            m.add(types.InlineKeyboardButton(f"Удалить: {name} ({w_idx}г)", callback_data=f"del_cart_{cart_id}"))
            
        m.add(
            types.InlineKeyboardButton("Очистить всю корзину", callback_data="cart_clear_all"),
            types.InlineKeyboardButton("Назад к оплате", callback_data="view_cart")
        )
        safe_edit_text(cid, mid, text, m)

    elif data.startswith("del_cart_"):
        cart_id = data.replace("del_cart_", "")
        db.execute("DELETE FROM cart WHERE id=? AND uid=?", (cart_id, uid))
        bot.answer_callback_query(c.id, "Товар удален из корзины!")
        c.data = "cart_items_list"
        handle_cb(c)

    elif data == "cart_clear_all":
        db.execute("DELETE FROM cart WHERE uid=?", (uid,))
        bot.answer_callback_query(c.id, "Корзина полностью очищена!")
        c.data = "view_cart"
        handle_cb(c)

    elif data == "cart_checkout_delivery":
        count = db.fetchone("SELECT COUNT(*) FROM cart WHERE uid=?", (uid,))[0]
        if count == 0:
            return bot.answer_callback_query(c.id, "Ваша корзина пуста!", show_alert=True)
            
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Клад - магнит", callback_data="cart_chk_dt_m"),
            types.InlineKeyboardButton("Клад - прикоп", callback_data="cart_chk_dt_p"),
            types.InlineKeyboardButton("Почта", callback_data="cart_chk_dt_t"),
            types.InlineKeyboardButton("Назад в корзину", callback_data="view_cart")
        )
        safe_edit_text(cid, mid, "Выберите предпочтительный тип доставки для всех товаров:", m)

    elif data.startswith("cart_chk_dt_"):
        deliv_char = data.replace("cart_chk_dt_", "")
        u = db.fetchone("SELECT country FROM users WHERE uid=?", (uid,))
        m = types.InlineKeyboardMarkup(row_width=2)
        country_banks = get_payment_methods(u[0])
        
        for b_idx, b_name in enumerate(country_banks):
            m.add(types.InlineKeyboardButton(b_name.upper(), callback_data=f"cart_pay_{deliv_char}_{b_idx}"))
        
        m.add(types.InlineKeyboardButton("Назад", callback_data="cart_checkout_delivery"))
        safe_edit_text(cid, mid, f"Выберите способ оплаты ({u[0]}):", m)

    elif data.startswith("cart_pay_"):
        parts = data.split("_")
        deliv_char = parts[2]
        b_idx = parts[3]
        
        u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        
        cart_items = db.fetchall("SELECT p.name, p.price, c.weight_idx, c.district FROM cart c JOIN products p ON c.product_id = p.id WHERE c.uid = ?", (uid,))
        if not cart_items:
            return bot.answer_callback_query(c.id, "Ваша корзина пуста!", show_alert=True)
            
        total_price_curr = 0.0
        total_price_usd = 0.0
        items_details = []
        
        for name, price_usd, w_idx, dist in cart_items:
            mult = 1 if w_idx == "1" else (1.9 if w_idx == "2" else (2.8 if w_idx == "3" else 4.2))
            item_price_usd = price_usd * mult
            item_price_curr = round(item_price_usd * rate, 1)
            total_price_usd += item_price_usd
            total_price_curr += item_price_curr
            items_details.append(f"- {name} ({w_idx}г, р-н: {dist}) — {item_price_curr} {curr}")
            
        deliv_type = "Клад - магнит" if deliv_char == "m" else ("Клад - прикоп" if deliv_char == "p" else "Почта")
        payment_methods = get_payment_methods(u[1])
        bank_name = payment_methods[int(b_idx)]
        order_id = "CRT-" + str(uuid.uuid4())[:6].upper()
        
        if b_idx == "0":
            btc_price = round(total_price_usd / BTC_USD_RATE, 6)
            price_text = f"{btc_price} BTC (~{total_price_curr:.1f} {curr})"
        else:
            price_text = f"{total_price_curr:.1f} {curr}"

        items_text = "\n".join(items_details)
        
        check = (f"Чек заказа #{order_id} (КОРЗИНА)\n"
                 f"--------------------------------------------------\n"
                 f" - Город: {u[0]}\n"
                 f" - Тип доставки: {deliv_type}\n"
                 f" - Способ оплаты: {bank_name}\n"
                 f" - Сумма к оплате: {price_text}\n"
                 f"--------------------------------------------------\n"
                 f"Содержимое заказа:\n"
                 f"{items_text}\n"
                 f"--------------------------------------------------\n"
                 f"ОБЯЗАТЕЛЬНО СКОПИРУЙТЕ И ОТПРАВЬТЕ ЭТОТ ЧЕК НАШЕМУ ОПЕРАТОРУ ДЛЯ ПОЛУЧЕНИЯ РЕКВИЗИТОВ ДЛЯ ОПЛАТЫ! Без предоставления чека реквизиты на оплату не выдаются, а ваш платеж не сможет быть зачислен оператором.\n\n"
                 f"Нажмите на кнопку ниже, чтобы отправить чек оператору и получить актуальные реквизиты.")
        
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Получить реквизиты у оператора", url=f"https://t.me/{MANAGER_USERNAME}"),
            types.InlineKeyboardButton("Использовать промокод", callback_data=f"cart_promo_{deliv_char}_{b_idx}_{order_id}_{total_price_usd:.1f}"),
            types.InlineKeyboardButton("На главную", callback_data="to_main")
        )
        
        db.execute("DELETE FROM cart WHERE uid=?", (uid,))
        safe_edit_text(cid, mid, check, m)

    elif data.startswith("cart_promo_"):
        parts = data.split("_")
        deliv_char = parts[2]
        b_idx = parts[3]
        order_id = parts[4]
        total_usd = float(parts[5])
        msg = bot.send_message(cid, "Введите ваш промокод для корзины:")
        bot.register_next_step_handler(msg, apply_cart_promo_receipt_step, deliv_char, b_idx, order_id, total_usd)

    elif data.startswith("rn_"):
        parts = data.split("_")
        pid = parts[1]
        w_idx = parts[2]
        
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Клад - магнит", callback_data=f"dt_{pid}_{w_idx}_m_0"),
            types.InlineKeyboardButton("Клад - прикоп", callback_data=f"dt_{pid}_{w_idx}_p_0"),
            types.InlineKeyboardButton("Почта", callback_data=f"dt_{pid}_{w_idx}_t_0")
        )
        safe_edit_text(cid, mid, "Выберите предпочтительный тип доставки:", m)

    elif data.startswith("dt_"):
        parts = data.split("_")
        pid = parts[1]
        w_idx = parts[2]
        deliv_char = parts[3]
        
        u = db.fetchone("SELECT country FROM users WHERE uid=?", (uid,))
        m = types.InlineKeyboardMarkup(row_width=2)
        country_banks = get_payment_methods(u[0])
        
        for b_idx, b_name in enumerate(country_banks):
            m.add(types.InlineKeyboardButton(b_name.upper(), callback_data=f"pay_{pid}_{w_idx}_{deliv_char}_{b_idx}_0"))
        
        m.add(types.InlineKeyboardButton("Назад", callback_data=f"rn_{pid}_{w_idx}_0"))
        safe_edit_text(cid, mid, f"Выберите способ оплаты ({u[0]}):", m)

    elif data.startswith("pay_"):
        parts = data.split("_")
        pid = parts[1]
        w_idx = parts[2]
        deliv_char = parts[3]
        b_idx = parts[4]
        
        p = db.fetchone("SELECT name, price FROM products WHERE id=?", (pid,))
        u = db.fetchone("SELECT city, country, district FROM users WHERE uid=?", (uid,))
        curr = CURRENCY_MAP.get(u[1], 'USD')
        rate = EXCHANGE_RATES.get(curr, 1.0)
        
        mult = 1 if w_idx == "1" else (1.9 if w_idx == "2" else (2.8 if w_idx == "3" else 4.2))
        price = round(p[1]*mult*rate, 1)
        w_text = f"{w_idx}г"
        
        deliv_type = "Клад - магнит" if deliv_char == "m" else ("Клад - прикоп" if deliv_char == "p" else "Почта")
        payment_methods = get_payment_methods(u[1])
        bank_name = payment_methods[int(b_idx)]
        order_id = str(uuid.uuid4())[:8].upper()
        
        if b_idx == "0":
            usd_price = p[1]*mult
            btc_price = round(usd_price / BTC_USD_RATE, 6)
            price_text = f"{btc_price} BTC (~{price} {curr})"
        else:
            price_text = f"{price} {curr}"

        check = (f"Чек заказа #{order_id}\n"
                 f"--------------------------------------------------\n"
                 f" - Город: {u[0]}\n"
                 f" - Район: {u[2] if u[2] else 'Не указан'}\n"
                 f" - Товар: {p[0]}\n"
                 f" - Вес: {w_text}\n"
                 f" - Тип доставки: {deliv_type}\n"
                 f" - Способ оплаты: {bank_name}\n"
                 f" - Сумма к оплате: {price_text}\n"
                 f"--------------------------------------------------\n"
                 f"ОБЯЗАТЕЛЬНО СКОПИРУЙТЕ И ОТПРАВЬТЕ ЭТОТ ЧЕК НАШЕМУ ОПЕРАТОРУ ДЛЯ ПОЛУЧЕНИЯ РЕКВИЗИТОВ ДЛЯ ОПЛАТЫ! Без предоставления чека реквизиты на оплату не выдаются, а ваш платеж не сможет быть зачислен оператором.\n\n"
                 f"Нажмите на кнопку ниже, чтобы отправить чек оператору и получить актуальные реквизиты.")
        
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Получить реквизиты у оператора", url=f"https://t.me/{MANAGER_USERNAME}"),
            types.InlineKeyboardButton("Использовать промокод", callback_data=f"promo_{pid}_{w_idx}_{deliv_char}_{b_idx}_{order_id}_0"),
            types.InlineKeyboardButton("На главную", callback_data="to_main")
        )
        safe_edit_text(cid, mid, check, m)

    elif data.startswith("promo_"):
        parts = data.split("_")
        pid = parts[1]
        w_idx = parts[2]
        deliv_char = parts[3]
        b_idx = parts[4]
        order_id = parts[5]
        msg = bot.send_message(cid, "Введите ваш промокод:")
        bot.register_next_step_handler(msg, apply_promo_receipt_step, pid, w_idx, deliv_char, b_idx, order_id, "0")

    elif data == "admin_main" and uid in ADMIN_IDS:
        total_users_count = db.fetchone("SELECT COUNT(*) FROM users")[0]
        
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Редактировать товары", callback_data="adm_list_0"),
            types.InlineKeyboardButton("Управление отзывами", callback_data="adm_rev_main"),
            types.InlineKeyboardButton("Управление промокодами", callback_data="adm_promo_main"),
            types.InlineKeyboardButton("Рассылка пользователям", callback_data="adm_broadcast"),
            types.InlineKeyboardButton("Обновить все витрины (Рандом)", callback_data="adm_shuffle"),
            types.InlineKeyboardButton("Выйти из админки", callback_data="to_main")
        )
        
        admin_panel_text = (
            f"Панель управления\n"
            f"--------------------------------------------------\n"
            f"Всего зарегистрировано пользователей: {total_users_count} чел.\n"
            f"--------------------------------------------------\n"
            f"Здесь доступно управление ассортиментом, отзывами, промокодами и рассылкой."
        )
        safe_edit_text(cid, mid, admin_panel_text, m)

    elif data == "adm_broadcast" and uid in ADMIN_IDS:
        msg = bot.send_message(cid, "Введите текст вашей рассылки (поддерживается HTML-разметка):")
        bot.register_next_step_handler(msg, process_broadcast_step)

    elif data == "adm_promo_main" and uid in ADMIN_IDS:
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Добавить промокод", callback_data="adm_promo_add"),
            types.InlineKeyboardButton("Список промокодов", callback_data="adm_promo_list_0"),
            types.InlineKeyboardButton("Назад в меню", callback_data="admin_main")
        )
        safe_edit_text(cid, mid, "Управление промокодами\nВы можете добавлять новые промокоды и регулировать размер скидки и срок действия.", m)

    elif data == "adm_promo_add" and uid in ADMIN_IDS:
        msg = bot.send_message(cid, "Введите новый промокод и размер скидки через пробел (например: SALE10 15):")
        bot.register_next_step_handler(msg, add_promo_step)

    elif data.startswith("adm_promo_list_") and uid in ADMIN_IDS:
        parts = data.split("_")
        page = int(parts[3])
        promos = db.fetchall("SELECT code, discount, expires_at FROM promocodes")
        if not promos:
            m = types.InlineKeyboardMarkup(row_width=1)
            m.add(types.InlineKeyboardButton("Назад", callback_data="adm_promo_main"))
            return safe_edit_text(cid, mid, "Список промокодов пуст.", m)
        
        start = page * 10
        end = start + 10
        m = types.InlineKeyboardMarkup(row_width=1)
        for code, discount, expires_at in promos[start:end]:
            if expires_at == 'eternal' or not expires_at:
                dur_label = "Вечный"
            else:
                try:
                    exp_dt = datetime.fromisoformat(expires_at)
                    if datetime.now() > exp_dt:
                        dur_label = "Истек"
                    else:
                        dur_label = exp_dt.strftime("%d.%m %H:%M")
                except Exception:
                    dur_label = "Неизв."
            m.add(types.InlineKeyboardButton(f"{code} ({discount}%) [{dur_label}] — УДАЛИТЬ", callback_data=f"adm_promo_del_{code}_{page}"))
        
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("Назад", callback_data=f"adm_promo_list_{page-1}"))
        if end < len(promos):
            nav.append(types.InlineKeyboardButton("Вперед", callback_data=f"adm_promo_list_{page+1}"))
        if nav:
            m.row(*nav)
        m.add(types.InlineKeyboardButton("Назад в меню", callback_data="adm_promo_main"))
        safe_edit_text(cid, mid, f"Список промокодов (Страница {page+1}):\nНажмите на промокод, чтобы его удалить.", m)

    elif data.startswith("adm_promo_del_") and uid in ADMIN_IDS:
        parts = data.split("_")
        code = parts[3]
        page = int(parts[4])
        db.execute("DELETE FROM promocodes WHERE code=?", (code,))
        bot.answer_callback_query(c.id, f"Промокод {code} удален!", show_alert=True)
        
        promos = db.fetchall("SELECT code, discount, expires_at FROM promocodes")
        if not promos:
            m = types.InlineKeyboardMarkup(row_width=1)
            m.add(types.InlineKeyboardButton("Назад", callback_data="adm_promo_main"))
            return safe_edit_text(cid, mid, "Список промокодов пуст.", m)
        
        start = page * 10
        end = start + 10
        m = types.InlineKeyboardMarkup(row_width=1)
        for cd, ds, exp_at in promos[start:end]:
            if exp_at == 'eternal' or not exp_at:
                dur_lbl = "Вечный"
            else:
                try:
                    exp_dt = datetime.fromisoformat(exp_at)
                    if datetime.now() > exp_dt:
                        dur_lbl = "Истек"
                    else:
                        dur_lbl = exp_dt.strftime("%d.%m %H:%M")
                except Exception:
                    dur_lbl = "Неизв."
            m.add(types.InlineKeyboardButton(f"{cd} ({ds}%) [{dur_lbl}] — УДАЛИТЬ", callback_data=f"adm_promo_del_{cd}_{page}"))
        
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("Назад", callback_data=f"adm_promo_list_{page-1}"))
        if end < len(promos):
            nav.append(types.InlineKeyboardButton("Вперед", callback_data=f"adm_promo_list_{page+1}"))
        if nav:
            m.row(*nav)
        m.add(types.InlineKeyboardButton("Назад в меню", callback_data="adm_promo_main"))
        safe_edit_text(cid, mid, f"Список промокодов (Страница {page+1}):", m)

    elif data.startswith("apd:"):
        parts = data.split(":")
        code = parts[1]
        discount = int(parts[2])
        dur = parts[3]
        
        now_dt = datetime.now()
        if dur == "1h":
            expires_dt = now_dt + timedelta(hours=1)
            exp_str = expires_dt.isoformat()
            dur_text = "1 час"
        elif dur == "1d":
            expires_dt = now_dt + timedelta(days=1)
            exp_str = expires_dt.isoformat()
            dur_text = "1 день"
        elif dur == "1w":
            expires_dt = now_dt + timedelta(weeks=1)
            exp_str = expires_dt.isoformat()
            dur_text = "1 неделя"
        elif dur == "2w":
            expires_dt = now_dt + timedelta(weeks=2)
            exp_str = expires_dt.isoformat()
            dur_text = "2 недели"
        elif dur == "1m":
            expires_dt = now_dt + timedelta(days=30)
            exp_str = expires_dt.isoformat()
            dur_text = "1 месяц"
        elif dur == "1y":
            expires_dt = now_dt + timedelta(days=365)
            exp_str = expires_dt.isoformat()
            dur_text = "1 год"
        else:
            exp_str = "eternal"
            dur_text = "Вечный (без ограничений)"
            
        db.execute("INSERT OR REPLACE INTO promocodes (code, discount, expires_at) VALUES (?,?,?)", (code, discount, exp_str))
        bot.answer_callback_query(c.id, f"Промокод {code} успешно создан!")
        
        success_text = (
            f"ПРОМОКОД УСПЕШНО СОЗДАН!\n"
            f"--------------------------------------------------\n\n"
            f"- Купон: {code}\n"
            f"- Скидка: {discount}%\n"
            f"- Срок действия: {dur_text}\n\n"
            f"Доступен для немедленного ввода пользователями при оформлении заказа."
        )
        m_back = types.InlineKeyboardMarkup()
        m_back.add(types.InlineKeyboardButton("Назад в промокоды", callback_data="adm_promo_main"))
        safe_edit_text(cid, mid, success_text, m_back)

    elif data == "adm_rev_main" and uid in ADMIN_IDS:
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Написать свой отзыв", callback_data="adm_rev_write"),
            types.InlineKeyboardButton("Добавить из заготовок (1000 шт.)", callback_data="adm_rev_tpl_0"),
            types.InlineKeyboardButton("Обновить отзывы витрины", callback_data="adm_rev_shuffle_db"),
            types.InlineKeyboardButton("Назад в меню", callback_data="admin_main")
        )
        safe_edit_text(cid, mid, "Управление отзывами\nВы можете добавить свой текст или выбрать готовый шаблон из базы в 1000 шт.", m)

    elif data == "adm_rev_shuffle_db" and uid in ADMIN_IDS:
        db.shuffle_reviews()
        bot.answer_callback_query(c.id, "Отзывы витрины успешно перемешаны и обновлены!", show_alert=True)

    elif data == "adm_rev_write" and uid in ADMIN_IDS:
        msg = bot.send_message(cid, "Введите текст нового отзыва. Он будет опубликован со случайным товаром:")
        bot.register_next_step_handler(msg, add_custom_review_step)

    elif data.startswith("adm_rev_tpl_") and uid in ADMIN_IDS:
        parts = data.split("_")
        page = int(parts[3])
        start = page * 10
        end = start + 10
        m = types.InlineKeyboardMarkup(row_width=1)
        
        for i, rev in enumerate(PREMADE_REVIEWS[start:end], start=start):
            short_text = rev[:35] + "..." if len(rev) > 35 else rev
            m.add(types.InlineKeyboardButton(short_text, callback_data=f"adm_rev_add_{i}"))
            
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("Назад", callback_data=f"adm_rev_tpl_{page-1}"))
        if end < len(PREMADE_REVIEWS):
            nav.append(types.InlineKeyboardButton("Вперед", callback_data=f"adm_rev_tpl_{page+1}"))
        
        if nav:
            m.row(*nav)
        m.add(types.InlineKeyboardButton("Назад в меню", callback_data="adm_rev_main"))
        safe_edit_text(cid, mid, f"Шаблоны отзывов (Страница {page+1}):\nНажмите на любой отзыв для его публикации на витрине.", m)

    elif data.startswith("adm_rev_add_") and uid in ADMIN_IDS:
        parts = data.split("_")
        idx = int(parts[3])
        txt = PREMADE_REVIEWS[idx]
        prod = random.choice(ALL_PRODUCT_NAMES)
        db.execute("INSERT INTO reviews (text, prod) VALUES (?,?)", (txt, prod))
        bot.answer_callback_query(c.id, "Отзыв успешно опубликован!", show_alert=True)

    elif data == "adm_shuffle" and uid in ADMIN_IDS:
        db.shuffle_stock()
        bot.answer_callback_query(c.id, "Витрины всех городов пересобраны заново!", show_alert=True)

    elif data.startswith("adm_list_"):
        parts = data.split("_")
        page = int(parts[2])
        prods = db.fetchall("SELECT id, name, price FROM products")
        start = page * 10
        end = start + 10
        m = types.InlineKeyboardMarkup(row_width=2)
        for pid, name, price in prods[start:end]:
            m.add(types.InlineKeyboardButton(name, callback_data=f"adm_edit_{pid}"))
        
        nav = []
        if page > 0:
            nav.append(types.InlineKeyboardButton("Назад", callback_data=f"adm_list_{page-1}"))
        if end < len(prods):
            nav.append(types.InlineKeyboardButton("Вперед", callback_data=f"adm_list_{page+1}"))
        if nav:
            m.row(*nav)
        m.add(types.InlineKeyboardButton("Назад", callback_data="admin_main"))
        safe_edit_text(cid, mid, f"Выберите товар для изменения (стр. {page+1}):", m)

    elif data.startswith("adm_edit_"):
        parts = data.split("_")
        pid = parts[2]
        p = db.fetchone("SELECT name, price FROM products WHERE id=?", (pid,))
        m = types.InlineKeyboardMarkup(row_width=1)
        m.add(
            types.InlineKeyboardButton("Изменить название", callback_data=f"edt_name_{pid}"),
            types.InlineKeyboardButton("Изменить цену", callback_data=f"edt_prc_{pid}"),
            types.InlineKeyboardButton("К списку", callback_data="adm_list_0")
        )
        safe_edit_text(cid, mid, f"Товар ID: {pid}\nИмя: {p[0]}\nБазовая цена: {p[1]}$", m)

    elif data.startswith("edt_name_"):
        parts = data.split("_")
        pid = parts[2]
        msg = bot.send_message(cid, "Введите новое название товара:")
        bot.register_next_step_handler(msg, update_name_step, pid)

    elif data.startswith("edt_prc_"):
        parts = data.split("_")
        pid = parts[2]
        msg = bot.send_message(cid, "Введите новую цену за 1г ($):")
        bot.register_next_step_handler(msg, update_price_step, pid)

def apply_cart_promo_receipt_step(m, deliv_char, b_idx, order_id, total_usd):
    if not m.text:
        return
    code = m.text.strip().upper()
    promo = db.fetchone("SELECT discount, expires_at FROM promocodes WHERE code=?", (code,))
    
    is_expired = False
    if promo:
        discount = int(promo[0])
        expires_at = promo[1]
        if expires_at and expires_at != 'eternal':
            try:
                exp_dt = datetime.fromisoformat(expires_at)
                if datetime.now() > exp_dt:
                    is_expired = True
            except Exception:
                pass
                
        if is_expired:
            db.execute("DELETE FROM promocodes WHERE code=?", (code,))
            promo = None

    uid = m.from_user.id
    u = db.fetchone("SELECT city, country FROM users WHERE uid=?", (uid,))
    curr = CURRENCY_MAP.get(u[1], 'USD')
    rate = EXCHANGE_RATES.get(curr, 1.0)
    
    deliv_type = "Клад - магнит" if deliv_char == "m" else ("Клад - прикоп" if deliv_char == "p" else "Почта")
    payment_methods = get_payment_methods(u[1])
    bank_name = payment_methods[int(b_idx)]
    
    base_price_curr = round(total_usd * rate, 1)
    
    if promo:
        discount = int(promo[0])
        if code.startswith("REF-"):
            db.execute("DELETE FROM promocodes WHERE code=?", (code,))
        
        discount_mult = (100 - discount) / 100.0
        new_price_curr = round(base_price_curr * discount_mult, 1)
        
        if b_idx == "0":
            usd_new_price = total_usd * discount_mult
            btc_old_price = round(total_usd / BTC_USD_RATE, 6)
            btc_price = round(usd_new_price / BTC_USD_RATE, 6)
            price_text = f"{btc_old_price} BTC (~{base_price_curr} {curr}) ➔ {btc_price} BTC (~{new_price_curr} {curr}) [Скидка {discount}%]"
        else:
            price_text = f"{base_price_curr} {curr} ➔ {new_price_curr} {curr} [Скидка {discount}%]"

        check = (f"Чек заказа #{order_id} (КОРЗИНА)\n"
                 f"--------------------------------------------------\n"
                 f" - Город: {u[0]}\n"
                 f" - Тип доставки: {deliv_type}\n"
                 f" - Способ оплаты: {bank_name}\n"
                 f" - Сумма: {price_text}\n"
                 f"--------------------------------------------------\n"
                 f"ОБЯЗАТЕЛЬНО СКОПИРУЙТЕ И ОТПРАВЬТЕ ЭТОТ ЧЕК НАШЕМУ ОПЕРАТОРУ ДЛЯ ПОЛУЧЕНИЯ РЕКВИЗИТОВ ДЛЯ ОПЛАТЫ! Без предоставления чека реквизиты на оплату не выдаются, а ваш платеж не сможет быть зачислен оператором.\n\n"
                 f"Нажмите на кнопку ниже, чтобы отправить чек оператору и получить актуальные реквизиты.")
        
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton("Получить реквизиты у оператора", url=f"https://t.me/{MANAGER_USERNAME}"),
            types.InlineKeyboardButton("На главную", callback_data="to_main")
        )
        bot.send_photo(m.chat.id, MAIN_IMG, caption=check, reply_markup=kb, parse_mode="HTML")
    else:
        text = f"Промокод {code} не действителен, истек или не найден."
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton("Попробовать снова", callback_data=f"cart_promo_{deliv_char}_{b_idx}_{order_id}_{total_usd:.1f}"),
            types.InlineKeyboardButton("На главную", callback_data="to_main")
        )
        bot.send_photo(m.chat.id, MAIN_IMG, caption=text, reply_markup=kb, parse_mode="HTML")

def update_name_step(m, pid):
    if not m.text:
        return
    db.execute("UPDATE products SET name=? WHERE id=?", (m.text, pid))
    bot.send_message(m.chat.id, f"Название товара #{pid} изменено на: {m.text}")

def update_price_step(m, pid):
    try:
        new_p = float(m.text)
        db.execute("UPDATE products SET price=? WHERE id=?", (new_p, pid))
        bot.send_message(m.chat.id, f"Цена товара #{pid} изменена на: {new_p}$")
    except ValueError:
        bot.send_message(m.chat.id, "Ошибка ввода. Введите числовое значение цены.")

def add_custom_review_step(m):
    if not m.text:
        return
    prod = random.choice(ALL_PRODUCT_NAMES)
    db.execute("INSERT INTO reviews (text, prod) VALUES (?,?)", (m.text, prod))
    bot.send_message(m.chat.id, "Ваш отзыв успешно опубликован и виден покупателям!")

def add_promo_step(m):
    if m.from_user.id not in ADMIN_IDS:
        return
    if not m.text:
        return
    try:
        parts = m.text.strip().split()
        if len(parts) != 2:
            raise ValueError
        code = parts[0].upper()
        discount = int(parts[1])
        if not (1 <= discount <= 99):
            bot.send_message(m.chat.id, "Размер скидки должен быть целым числом в диапазоне от 1 до 99.")
            return
            
        m_markup = types.InlineKeyboardMarkup(row_width=2)
        m_markup.add(
            types.InlineKeyboardButton("1 час", callback_data=f"apd:{code}:{discount}:1h"),
            types.InlineKeyboardButton("1 день", callback_data=f"apd:{code}:{discount}:1d")
        )
        m_markup.add(
            types.InlineKeyboardButton("1 неделя", callback_data=f"apd:{code}:{discount}:1w"),
            types.InlineKeyboardButton("2 недели", callback_data=f"apd:{code}:{discount}:2w")
        )
        m_markup.add(
            types.InlineKeyboardButton("1 месяц", callback_data=f"apd:{code}:{discount}:1m"),
            types.InlineKeyboardButton("1 год", callback_data=f"apd:{code}:{discount}:1y")
        )
        m_markup.add(
            types.InlineKeyboardButton("Вечный", callback_data=f"apd:{code}:{discount}:eternal")
        )
        m_markup.add(
            types.InlineKeyboardButton("Отмена", callback_data="adm_promo_main")
        )
        
        bot.send_message(
            m.chat.id, 
            f"Вы создаете промокод {code} со скидкой {discount}%.\nВыберите срок его действия:", 
            reply_markup=m_markup, 
            parse_mode="HTML"
        )
    except ValueError:
        bot.send_message(m.chat.id, "Ошибка формата ввода. Используйте пример: SALE15 15")

def apply_promo_receipt_step(m, pid, w_idx, deliv_char, b_idx, order_id, hours="0"):
    if not m.text:
        return
    code = m.text.strip().upper()
    promo = db.fetchone("SELECT discount, expires_at FROM promocodes WHERE code=?", (code,))
    
    is_expired = False
    if promo:
        discount = int(promo[0])
        expires_at = promo[1]
        if expires_at and expires_at != 'eternal':
            try:
                exp_dt = datetime.fromisoformat(expires_at)
                if datetime.now() > exp_dt:
                    is_expired = True
            except Exception:
                pass
                
        if is_expired:
            db.execute("DELETE FROM promocodes WHERE code=?", (code,))
            promo = None

    u = db.fetchone("SELECT city, country, district FROM users WHERE uid=?", (m.from_user.id,))
    curr = CURRENCY_MAP.get(u[1], 'USD')
    rate = EXCHANGE_RATES.get(curr, 1.0)
    
    p = db.fetchone("SELECT name, price FROM products WHERE id=?", (pid,))
    mult = 1 if w_idx == "1" else (1.9 if w_idx == "2" else (2.8 if w_idx == "3" else 4.2))
    base_price = round(p[1]*mult*rate, 1)
    w_text = f"{w_idx}г"
    deliv_type = "Клад - магнит" if deliv_char == "m" else ("Клад - прикоп" if deliv_char == "p" else "Почта")
    payment_methods = get_payment_methods(u[1])
    bank_name = payment_methods[int(b_idx)]
    
    if promo:
        discount = int(promo[0])
        if code.startswith("REF-"):
            db.execute("DELETE FROM promocodes WHERE code=?", (code,))
        
        discount_mult = (100 - discount) / 100.0
        new_price = round(base_price * discount_mult, 1)
        
        if b_idx == "0":
            usd_new_price = (p[1]*mult) * discount_mult
            btc_old_price = round((p[1]*mult) / BTC_USD_RATE, 6)
            btc_price = round(usd_new_price / BTC_USD_RATE, 6)
            price_text = f"{btc_old_price} BTC (~{base_price} {curr}) ➔ {btc_price} BTC (~{new_price} {curr}) [Скидка {discount}%]"
        else:
            price_text = f"{base_price} {curr} ➔ {new_price} {curr} [Скидка {discount}%]"

        check = (f"Чек заказа #{order_id}\n"
                 f"--------------------------------------------------\n"
                 f" - Город: {u[0]}\n"
                 f" - Район: {u[2] if u[2] else 'Не указан'}\n"
                 f" - Товар: {p[0]}\n"
                 f" - Вес: {w_text}\n"
                 f" - Тип доставки: {deliv_type}\n"
                 f" - Способ оплаты: {bank_name}\n"
                 f" - Сумма: {price_text}\n"
                 f"--------------------------------------------------\n"
                 f"ОБЯЗАТЕЛЬНО СКОПИРУЙТЕ И ОТПРАВЬТЕ ЭТОТ ЧЕК НАШЕМУ ОПЕРАТОРУ ДЛЯ ПОЛУЧЕНИЯ РЕКВИЗИТОВ ДЛЯ ОПЛАТЫ! Без предоставления чека реквизиты на оплату не выдаются, а ваш платеж не сможет быть зачислен оператором.\n\n"
                 f"Нажмите на кнопку ниже, чтобы отправить чек оператору и получить актуальные реквизиты.")
        
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton("Получить реквизиты у оператора", url=f"https://t.me/{MANAGER_USERNAME}"),
            types.InlineKeyboardButton("На главную", callback_data="to_main")
        )
        bot.send_photo(m.chat.id, MAIN_IMG, caption=check, reply_markup=kb, parse_mode="HTML")
    else:
        text = f"Промокод {code} не действителен, истек или не найден."
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton("Попробовать снова", callback_data=f"promo_{pid}_{w_idx}_{deliv_char}_{b_idx}_{order_id}_0"),
            types.InlineKeyboardButton("На главную", callback_data="to_main")
        )
        bot.send_photo(m.chat.id, MAIN_IMG, caption=text, reply_markup=kb, parse_mode="HTML")

def process_broadcast_step(m):
    if m.from_user.id not in ADMIN_IDS:
        return
    if not m.text:
        return
    text = m.text
    users = db.fetchall("SELECT uid FROM users")
    success, failed = 0, 0
    for (u_id,) in users:
        try:
            bot.send_message(u_id, text, parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            failed += 1
    bot.send_message(m.chat.id, f"Рассылка завершена!\nУспешно отправлено: {success}\nНе удалось (заблокировали бота): {failed}")

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
