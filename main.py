import asyncio
import logging
import aiosqlite
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery, LabeledPrice, PreCheckoutQuery,
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage

# ============================================================
# НАСТРОЙКИ (ЗАМЕНИ НА СВОИ)
# ============================================================
BOT_TOKEN = "8237040076:AAHEpz01b8zJmjWrM4tmOdQEOZs2QECt2Qw"
# Реквизиты для оплаты:
PAYMENT_DETAILS = ""5599002124687536"
💳 <b>РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ</b>

Банк: Сбербанк
Карта: 2202 20XX XXXX XXXX
Получатель: Имя Фамилия

Или:

Банк: Т-Банк (Тинькофф)
Карта: 5536 91XX XXXX XXXX
Получатель: Имя Фамилия

Либо перевод по номеру телефона:
📱 +7 999 123-45-67

После оплаты пришли скриншот прямо сюда 👇
"""
ADMIN_IDS = [5062414502]  # Твой Telegram ID

# Премиум-стикеры (получи через @RawDataBot)
STICKER_WELCOME = "CAACAgIAAxkBAA..."
STICKER_THANKS = "CAACAgIAAxkBAA..."

# ============================================================
# ПРЕМИУМ-ЭМОДЗИ
# ============================================================
CUSTOM_EMOJI = {
    "services":        "5906975484054345026",
    "infoproducts":    "5906642705693284735",
    "faq":             "5906797358875681525",
    "support":         "5906991701850856372",
    "promo":           "5906716471756593520",
    "search":          "5906581476639513176",
    "bases":           "5906622905894050515",
    "search_5":        "5906581476639513176",
    "search_35":       "5906622905894050515",
    "search_70":       "5906581476639513176",
    "search_120":      "5906622905894050515",
    "extra_retouch":   "5906611897892870255",
    "extra_speed":     "5906975484054345026",
    "offer1":          "5906476035192396092",
    "offer2":          "5906840875484321836",
    "offer3":          "5906716471756593520",
    "confirm":         "5906986955911993888",
    "payment_btn":     "5904576890848419790",
    "success":         "5906852613629941703",
    "warning":         "5907027122446145395",
    "home":            "5906891238270834298",
    "back":            "5906891238270834298",
    "faq_q":           "5906630525166032796",
    "faq_info":        "5906884044200614612",
    "faq_tip":         "5906839307821259375",
    "faq_contact":     "5906991701850856372",
}

def emoji(name: str) -> str:
    eid = CUSTOM_EMOJI.get(name)
    if eid:
        return f'<tg-emoji emoji-id="{eid}">⚡</tg-emoji>'
    return "⭐"

# ============================================================
# БАЗА ДАННЫХ
# ============================================================

async def init_db():
    async with aiosqlite.connect("shop.db") as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                item_name TEXT,
                amount INTEGER,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        await db.commit()

async def add_user(user_id: int, username: str, first_name: str):
    async with aiosqlite.connect("shop.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name)
        )
        await db.commit()

async def add_order(user_id: int, item_name: str, amount: int, status: str = "paid"):
    async with aiosqlite.connect("shop.db") as db:
        await db.execute(
            "INSERT INTO orders (user_id, item_name, amount, status) VALUES (?, ?, ?, ?)",
            (user_id, item_name, amount, status)
        )
        await db.commit()

# ============================================================
# ТЕКСТЫ
# ============================================================

WELCOME = f"""
{emoji("services")} <b>Привет! Я бот-магазин WareonsmmBot.</b>

Помогаю дизайнерам инфографики находить клиентов без ручного поиска и выгорания.

Выбери раздел:
"""

# -- ИНФОПРОДУКТЫ --

INFOPRODUCTS_INTRO = f"""
{emoji("infoproducts")} <b>ИНФОПРОДУКТЫ</b>

Готовые инструменты для самостоятельного поиска клиентов. Усиливают рассылки и повышают конверсию.

{emoji("faq_tip")} Не заменяют систему, но кратно ускоряют результат при правильном использовании.
"""

OFFER1_DESC = f"""
{emoji("offer1")} <b>ЭФФЕКТИВНЫЙ ОФФЕР</b>
💰 <b>180 ₽</b>

Готовое решение для увеличения откликов. Тебе перестанут отвечать «я подумаю» и начнут спрашивать «сколько стоит?».

<b>Ты получаешь:</b>
• готовый оффер, который цепляет внимание
• проверенную структуру сообщения
• схему первого касания, вызывающую интерес

<b>Как использовать:</b> вставил свои данные → скопировал → отправил. 5 минут и ты уже в плюсе.

<b>Кому нужно:</b> не отвечают на сообщения, не знаешь что писать, хочешь больше откликов без тестов.
"""

OFFER2_DESC = f"""
{emoji("offer2")} <b>PSD ОБЛОЖКА ОФФЕРА</b>
💰 <b>290 ₽</b>

Сообщение с картинкой открывают в 3 раза чаще. Этот PSD-шаблон — твой визуальный крючок.

<b>Ты получаешь:</b>
• PSD-файл от дизайнера
• готовую структуру под твой контент

<b>Как использовать:</b> подставляешь свои работы → крепишь к офферу → рассылаешь.

<b>Кому нужно:</b> нет визуала под оффер, хочешь выделиться в ленте, поднять открываемость.
"""

OFFER3_DESC = f"""
{emoji("offer3")} <b>НАБОР «ОФФЕР + ИЗОБРАЖЕНИЕ»</b>
💰 <b>320 ₽</b> <s>470 ₽</s>

Полный комплект: текст, который продаёт + визуал, который притягивает взгляд.

<b>Ты получаешь:</b>
• готовый оффер со структурой
• PSD-шаблон обложки
• инструкцию по внедрению

<b>Кому нужно:</b> хочешь всё и сразу, без сборки по частям. Лучший стартовый набор.
"""

# -- УСЛУГИ --

SERVICES_INTRO = f"""
{emoji("services")} <b>УСЛУГИ</b>

Выбери, что тебе нужно:
"""

# Поиск клиентов под ключ
SEARCH_INTRO = f"""
{emoji("search")} <b>ПОИСК КЛИЕНТОВ ПОД КЛЮЧ</b>

Ты дизайнер, а не спамер. Мы берём поиск клиентов на себя.

<b>Что мы делаем:</b>
• Находим целевых селлеров под твою нишу
• Пишем им сами — грамотно, не шаблонно
• Делаем серию касаний до ответа
• Передаём тебе тёплых клиентов, готовых купить

Ты не пишешь «всем подряд». Ты не тратишь часы на пустые диалоги. Ты просто берёшь заказы.
"""

SEARCH_5_DESC = f"""
{emoji("search_5")} <b>5 КЛИЕНТОВ ЗА 3 ДНЯ</b>
💰 <b>1 200₽</b> или 700₽ + 30% с заказов

📤 600+ касаний
⏱ Срок: 3 дня
🎯 До 5 реальных клиентов

<b>Для кого:</b>
• Никогда не пробовал рассылки — протестируй систему
• Был простой — вернись в поток без риска
• Хочешь проверить наш подход перед крупным заказом

Первые отклики в день запуска. Твоя ниша жива — докажем.
"""

SEARCH_35_DESC = f"""
{emoji("search_35")} <b>35+ ОТКЛИКОВ В DIRECT</b>
💰 <b>4 200₽</b> или 2 000₽ + 30% с закрытых клиентов

📤 5 000+ касаний
⏱ Срок: 7 дней
🎯 От 35 откликов (часто 50–70)

<b>Что это даёт:</b>
• Ты перестаёшь искать клиентов — они приходят сами
• Формируешь лист ожидания из горячих селлеров
• Выходишь из 20к/мес в стабильные 70к+

Лучшее соотношение цена/результат. Одинаково мощно для одиночек и студий.
"""

SEARCH_70_DESC = f"""
{emoji("search_70")} <b>70+ ПЛАТЕЖЕСПОСОБНЫХ ЛИДОВ</b>
💰 <b>8 000₽</b> или 6 000₽ + 30%

👥 3 исполнителя
📤 7 000+ касаний
⏱ 2 недели
🎯 70+ откликов (до 120)

<b>Ключевое отличие:</b> мы ищем селлеров с бюджетом. Твой средний чек ×2.

<b>Для тех, кто:</b>
• Умеет продавать, но нужен поток горячих лидов
• Хочет забыть о ценовых возражениях
• Готов зарабатывать по рынку, а не демпинговать
"""

SEARCH_120_DESC = f"""
{emoji("search_120")} <b>120+ PREMIUM ЗАЯВОК</b>
💰 <b>13 800₽</b> или 10 000₽ + 30%

👥 5 рассыльщиков
📤 12 000+ касаний
⏱ 3–4 недели
🎯 120+ откликов (до 200+)

<b>Полноценный отдел продаж на аутсорсе.</b> Мы делаем всё — ты только выполняешь заказы.

<b>Для:</b> крупных студий и профи, готовых масштабироваться. Вопрос «где брать клиентов» исчезнет навсегда.
"""

EXTRA_RETOUCH_DESC = f"""
{emoji("extra_retouch")} <b>ПОВТОРНЫЕ КАСАНИЯ</b>
💰 <b>650₽</b> (50% базы) / <b>1 300₽</b> (100% базы)

Пишем тем, кто не ответил. Другой заход, другая логика. Конверсия вырастает в 1,5–2 раза.

Рекомендуем 100% — окупается с первого же закрытого клиента.
"""

EXTRA_SPEED_DESC = f"""
{emoji("extra_speed")} <b>УСКОРЕНИЕ РЕЗУЛЬТАТА</b>
💰 <b>1 500₽</b>

Сокращаем сроки на 45–60%. Подключаем +1–3 исполнителя.

Когда результат нужен «вчера», а каждый день ожидания — упущенная прибыль.
"""

# Базы селлеров
BASES_INTRO = f"""
{emoji("bases")} <b>БАЗЫ СЕЛЛЕРОВ</b>

Подбираем список потенциальных клиентов под твою нишу. Активные селлеры из открытых источников.

<b>Ты получаешь:</b>
• список активных продавцов
• сегментированную аудиторию
• готовую базу для немедленного запуска

{emoji("warning")} <b>ВАЖНО:</b>
• Данные из открытых источников, могут терять актуальность
• Не гарантируем ответ каждого — только объём и релевантность
• Результат зависит от оффера и подачи
• Возврата нет после выполнения
"""

BASES_1000_DESC = f"📦 <b>База 1 000 селлеров</b> — <b>160₽</b>\nОтличный старт для теста ниши."
BASES_5000_DESC = f"📊 <b>База 5 000 селлеров</b> — <b>490₽</b>\nЗолотая середина для стабильных заказов."
BASES_10000_DESC = f"📁 <b>База 10 000 селлеров</b> — <b>790₽</b>\nОбъём для системной работы."
BASES_20000_DESC = f"💼 <b>База 20 000 селлеров</b> — <b>1 290₽</b>\nМаксимальный охват всей ниши."

# FAQ
FAQ = f"""
{emoji("faq")} <b>ЧАСТЫЕ ВОПРОСЫ</b>

Выбери вопрос — я отвечу:
"""

FAQ_ANSWERS = {
    "faq_q1":  "Первые отклики чаще всего появляются уже в день запуска.",
    "faq_q2":  "Базы полностью законны и безопасны — сбор из открытых источников.",
    "faq_q3":  "Рассылки ведут профессионалы с опытом. Мы используем эффективные стратегии и повторные касания.",
    "faq_q4":  "Собираем из открытых источников. Никаких утечек и запрещённых методов.",
    "faq_q5":  "Работаем с нишами инфографики и графического дизайна.",
    "faq_q6":  "Не устроил результат — гарантируем отклики и заявки согласно тарифу.",
    "faq_q7":  "Скрытых доплат нет. Платишь только за выбранный товар или услугу.",
    "faq_q8":  "Офферы составлены профессионалами и многократно проверены в реальных рассылках.",
    "faq_q9":  "Используем обширные базы и сегментацию по нишам.",
    "faq_q10": "Да, работают. Доказано на своём опыте и кейсах клиентов.",
    "faq_q11": "Можем прислать скриншоты переписок по запросу.",
    "faq_q12": "Приводим тёплых лидов, готовых к покупке.",
    "faq_q13": "Зависит от тарифа, но часто цифра превышает гарантированный минимум.",
    "faq_q14": "Поиск клиентов для бизнеса через систему касаний, базы и рассылки.",
}

SUCCESS_PAYMENT = f"""
{emoji("success")} <b>ОПЛАТА ПРОШЛА!</b>

Спасибо за покупку. Товар уже готов.
"""

SUPPORT_MSG = f"""
{emoji("support")} <b>ПОДДЕРЖКА</b>

Напиши свой вопрос сюда — ответим в ближайшее время.
"""

# ============================================================
# КЛАВИАТУРЫ
# ============================================================

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text=f"{emoji('services')} Услуги"))
    builder.add(KeyboardButton(text=f"{emoji('infoproducts')} Инфопродукты"))
    builder.add(KeyboardButton(text=f"{emoji('faq')} FAQ"))
    builder.add(KeyboardButton(text=f"{emoji('support')} Поддержка"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def services_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔍 Поиск клиентов под ключ", callback_data="service_search"))
    builder.add(InlineKeyboardButton(text="📊 Базы селлеров", callback_data="service_bases"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def search_packages():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🎯 5 клиентов за 3 дня (1200₽)", callback_data="view_search_5"))
    builder.add(InlineKeyboardButton(text="👨‍💻 35+ откликов (4200₽)", callback_data="view_search_35"))
    builder.add(InlineKeyboardButton(text="💸 70+ лидов (8000₽)", callback_data="view_search_70"))
    builder.add(InlineKeyboardButton(text="🏭 120+ Premium (13800₽)", callback_data="view_search_120"))
    builder.add(InlineKeyboardButton(text="📜 Повторные касания", callback_data="view_retouch"))
    builder.add(InlineKeyboardButton(text="📃 Ускорение результата", callback_data="view_speed"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="services"))
    builder.adjust(1)
    return builder.as_markup()

def bases_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📦 1 000 шт (160₽)", callback_data="buy_bases_1000"))
    builder.add(InlineKeyboardButton(text="📊 5 000 шт (490₽)", callback_data="buy_bases_5000"))
    builder.add(InlineKeyboardButton(text="📁 10 000 шт (790₽)", callback_data="buy_bases_10000"))
    builder.add(InlineKeyboardButton(text="💼 20 000 шт (1290₽)", callback_data="buy_bases_20000"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="services"))
    builder.adjust(1)
    return builder.as_markup()

def infoproducts_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📄 Эффективный оффер (180₽)", callback_data="buy_offer1"))
    builder.add(InlineKeyboardButton(text="🖼 PSD обложка (290₽)", callback_data="buy_offer2"))
    builder.add(InlineKeyboardButton(text="🎁 Набор Оффер+Изображение (320₽)", callback_data="buy_offer3"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def faq_menu():
    builder = InlineKeyboardBuilder()
    questions = [
        ("Через сколько появляются отклики?", "faq_q1"),
        ("Законны ли базы селлеров?", "faq_q2"),
        ("Чем ваши рассылки лучше?", "faq_q3"),
        ("Как собираете базы?", "faq_q4"),
        ("С какими нишами работаете?", "faq_q5"),
        ("Что делать, если результат не устроит?", "faq_q6"),
        ("Есть ли скрытые доплаты?", "faq_q7"),
        ("Чем офферы лучше конкурентов?", "faq_q8"),
        ("Как выбираете кому писать?", "faq_q9"),
        ("Работают ли рассылки?", "faq_q10"),
        ("Можно увидеть пример переписки?", "faq_q11"),
        ("Доводите до оплаты или только лиды?", "faq_q12"),
        ("Сколько откликов я получу?", "faq_q13"),
        ("Что делает ваш сервис?", "faq_q14"),
    ]
    for text, callback in questions:
        builder.add(InlineKeyboardButton(text=text, callback_data=callback))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def buy_button(item_name: str, callback: str, back_callback: str = "main_menu"):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=f"💳 Купить — {item_name}", callback_data=callback))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data=back_callback))
    builder.adjust(1)
    return builder.as_markup()

def back_button(callback: str):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data=callback))
    return builder.as_markup()

# ============================================================
# ОБРАБОТЧИКИ
# ============================================================

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    if STICKER_WELCOME != "CAACAgIAAxkBAA...":
        await message.answer_sticker(STICKER_WELCOME)
    await message.answer(WELCOME, parse_mode='HTML', reply_markup=main_menu())

# -- Навигация --

@router.message(F.text == f"{emoji('services')} Услуги")
async def services(message: Message):
    await message.answer(SERVICES_INTRO, parse_mode='HTML', reply_markup=services_menu())

@router.message(F.text == f"{emoji('infoproducts')} Инфопродукты")
async def infoproducts(message: Message):
    await message.answer(INFOPRODUCTS_INTRO, parse_mode='HTML', reply_markup=infoproducts_menu())

@router.message(F.text == f"{emoji('faq')} FAQ")
async def faq(message: Message):
    await message.answer(FAQ, parse_mode='HTML', reply_markup=faq_menu())

@router.message(F.text == f"{emoji('support')} Поддержка")
async def support(message: Message):
    await message.answer(SUPPORT_MSG, parse_mode='HTML')

@router.callback_query(F.data == "main_menu")
async def back_main(call: CallbackQuery):
    await call.message.answer(WELCOME, parse_mode='HTML', reply_markup=main_menu())
    await call.answer()

@router.callback_query(F.data == "services")
async def back_services(call: CallbackQuery):
    await call.message.answer(SERVICES_INTRO, parse_mode='HTML', reply_markup=services_menu())
    await call.answer()

# -- Услуги: Поиск клиентов --

@router.callback_query(F.data == "service_search")
async def search_intro(call: CallbackQuery):
    await call.message.answer(SEARCH_INTRO, parse_mode='HTML', reply_markup=search_packages())
    await call.answer()

@router.callback_query(F.data.startswith("view_search_"))
async def view_search_package(call: CallbackQuery):
    texts = {
        "view_search_5":   SEARCH_5_DESC,
        "view_search_35":  SEARCH_35_DESC,
        "view_search_70":  SEARCH_70_DESC,
        "view_search_120": SEARCH_120_DESC,
    }
    text = texts.get(call.data, "Неизвестный пакет")
    back = "service_search"
    # Услуги под ключ — заявка админу
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🚀 Оставить заявку", callback_data=call.data.replace("view", "order")))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data=back))
    await call.message.answer(text, parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()

@router.callback_query(F.data.startswith("order_search_"))
async def order_search(call: CallbackQuery):
    await call.message.answer(
        f"{emoji('confirm')} <b>Отлично!</b>\n\nНапиши сюда:\n1. Твою нишу\n2. Ссылку на портфолио\n3. Контакт для связи\n\nЯ передам менеджеру.",
        parse_mode='HTML'
    )
    # Уведомление админу
    for admin_id in ADMIN_IDS:
        await call.bot.send_message(
            admin_id,
            f"📩 Новая заявка!\nПользователь: @{call.from_user.username} (ID {call.from_user.id})\nПакет: {call.data}",
        )
    await call.answer()

@router.callback_query(F.data == "view_retouch")
async def view_retouch(call: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📜 Заказать (650₽ / 1300₽)", callback_data="order_retouch"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="service_search"))
    await call.message.answer(EXTRA_RETOUCH_DESC, parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()

@router.callback_query(F.data == "order_retouch")
async def order_retouch(call: CallbackQuery):
    await call.message.answer(f"{emoji('confirm')} Напиши, какой объём базы (50% или 100%) и свои контакты. Передам менеджеру.", parse_mode='HTML')
    for admin_id in ADMIN_IDS:
        await call.bot.send_message(admin_id, f"📩 Заявка на повторные касания от @{call.from_user.username}")
    await call.answer()

@router.callback_query(F.data == "view_speed")
async def view_speed(call: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📃 Заказать ускорение (1500₽)", callback_data="order_speed"))
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="service_search"))
    await call.message.answer(EXTRA_SPEED_DESC, parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()

@router.callback_query(F.data == "order_speed")
async def order_speed(call: CallbackQuery):
    await call.message.answer(f"{emoji('confirm')} Напиши свои контакты — подключу ускорение.", parse_mode='HTML')
    for admin_id in ADMIN_IDS:
        await call.bot.send_message(admin_id, f"📩 Заявка на ускорение от @{call.from_user.username}")
    await call.answer()

# -- Услуги: Базы селлеров --

@router.callback_query(F.data == "service_bases")
async def bases_intro(call: CallbackQuery):
    await call.message.answer(BASES_INTRO, parse_mode='HTML', reply_markup=bases_menu())
    await call.answer()

@router.callback_query(F.data.startswith("buy_bases_"))
async def buy_bases(call: CallbackQuery):
    data = call.data
    bases = {
        "buy_bases_1000":  ("База 1000 селлеров", 160),
        "buy_bases_5000":  ("База 5000 селлеров", 490),
        "buy_bases_10000": ("База 10000 селлеров", 790),
        "buy_bases_20000": ("База 20000 селлеров", 1290),
    }
    title, price = bases.get(data, ("Неизвестно", 0))
    await call.message.answer_invoice(
        title=title,
        description="Подбор активных селлеров из открытых источников",
        payload=data,
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label=title, amount=price * 100)],
        start_parameter="bases",
    )
    await call.answer()

# -- Инфопродукты --

@router.callback_query(F.data.startswith("buy_offer"))
async def buy_offer(call: CallbackQuery):
    data = call.data
    offers = {
        "buy_offer1": ("Эффективный оффер", 180),
        "buy_offer2": ("PSD обложка оффера", 290),
        "buy_offer3": ("Набор Оффер+Изображение", 320),
    }
    title, price = offers.get(data, ("Неизвестно", 0))
    await call.message.answer_invoice(
        title=title,
        description="Готовый инструмент для увеличения откликов",
        payload=data,
        provider_token=PAYMENT_TOKEN,
        currency="RUB",
        prices=[LabeledPrice(label=title, amount=price * 100)],
        start_parameter="offer",
    )
    await call.answer()

# -- Оплата и выдача --

@router.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payload = message.successful_payment.invoice_payload
    user_id = message.from_user.id
    amount = message.successful_payment.total_amount // 100
    await add_order(user_id, payload, amount)

    if STICKER_THANKS != "CAACAgIAAxkBAA...":
        await message.answer_sticker(STICKER_THANKS)
    await message.answer(SUCCESS_PAYMENT, parse_mode='HTML')

    # Выдача товара
    if payload == "buy_offer1":
        await message.answer("📄 Вот твой оффер:\n\n[Сюда вставь текст оффера или файл]")
        # Upsell
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="🖼 Добавить PSD обложку (290₽)", callback_data="buy_offer2"))
        builder.add(InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu"))
        await message.answer("🎁 <b>Усиль эффект:</b> добавь PSD обложку к офферу и получи в 3 раза больше откликов.", parse_mode='HTML', reply_markup=builder.as_markup())

    elif payload == "buy_offer2":
        await message.answer_document(types.FSInputFile("placeholder.txt"))  # Замени на реальный файл
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="📄 Добавить оффер (180₽)", callback_data="buy_offer1"))
        builder.add(InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu"))
        await message.answer("🎁 <b>Добавь оффер к обложке</b> — и у тебя полный комплект.", parse_mode='HTML', reply_markup=builder.as_markup())

    elif payload == "buy_offer3":
        await message.answer("🎁 Вот твой набор (оффер + PSD):\n\n[Вставь ссылку или файлы]")
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="🚀 Хочу поиск клиентов под ключ", callback_data="service_search"))
        builder.add(InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu"))
        await message.answer("🔥 Готов протестировать профессиональный поиск клиентов?", parse_mode='HTML', reply_markup=builder.as_markup())

    elif payload.startswith("buy_bases_"):
        await message.answer("📊 Вот твоя база селлеров:\n\n[Вставь файл или ссылку]")
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="📄 Добавить оффер (180₽)", callback_data="buy_offer1"))
        builder.add(InlineKeyboardButton(text="🏠 В главное меню", callback_data="main_menu"))
        await message.answer("🎯 С этой базой лучше работает правильный оффер. Добавишь?", parse_mode='HTML', reply_markup=builder.as_markup())

    await message.answer(WELCOME, parse_mode='HTML', reply_markup=main_menu())

# -- FAQ --

@router.callback_query(F.data.startswith("faq_q"))
async def faq_answer(call: CallbackQuery):
    answer = FAQ_ANSWERS.get(call.data, "Ответ не найден.")
    await call.message.answer(f"{emoji('faq_info')} {answer}", parse_mode='HTML', reply_markup=back_button("faq_menu"))
    await call.answer()

@router.callback_query(F.data == "faq_menu")
async def back_faq(call: CallbackQuery):
    await call.message.answer(FAQ, parse_mode='HTML', reply_markup=faq_menu())
    await call.answer()

# -- Поддержка (пересылка админу) --

@router.message(F.text, lambda msg: msg.text not in [
    f"{emoji('services')} Услуги",
    f"{emoji('infoproducts')} Инфопродукты",
    f"{emoji('faq')} FAQ",
    f"{emoji('support')} Поддержка",
])
async def forward_to_admin(message: Message):
    for admin_id in ADMIN_IDS:
        await message.forward(admin_id)
    await message.answer(f"{emoji('confirm')} Твоё сообщение отправлено. Ответим в ближайшее время.", parse_mode='HTML')

# ============================================================
# ЗАПУСК
# ============================================================

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await init_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
