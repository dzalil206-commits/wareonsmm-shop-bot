import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.filters import CommandStart
from aiogram.types import (
    Message, CallbackQuery,
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.storage.memory import MemoryStorage

# ============================================================
# НАСТРОЙКИ (ЗАМЕНИ НА СВОИ)
# ============================================================
BOT_TOKEN = "8237040076:AAHEpz01b8zJmjWrM4tmOdQEOZs2QECt2Qw"
ADMIN_IDS = [5062414502]

STICKER_WELCOME = "CAACAgIAAxkBAAFJQYRqAAGSijY-HNc8OcmMNQc8kPlFKocAAm5bAAJFJjBJZsail57k1607BA"
STICKER_THANKS = "CAACAgIAAxkBAAFJQYxqAAGSpzX4vKAlryhAQeag0JN0zwIAAsVQAAIEyjFJrFlaKe6oapY7BA"

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
    "money":           "5904576890848419790",
    "package":         "5906476035192396092",
    "timer":           "5906975484054345026",
    "users":           "5906622905894050515",
    "message":         "5906611897892870255",
    "star":            "5906716471756593520",
}

def emoji(name: str) -> str:
    eid = CUSTOM_EMOJI.get(name)
    if eid:
        return '<tg-emoji emoji-id="' + eid + '">.</tg-emoji>'
    return "."

def e(name: str) -> str:
    return emoji(name)

# ============================================================
# БАЗА ДАННЫХ
# ============================================================
async def init_db():
    pass

async def add_user(user_id: int, username: str, first_name: str):
    pass

async def add_order(user_id: int, item_name: str, amount: int, status: str = "pending_verification"):
    pass

# ============================================================
# ТЕКСТЫ (без f-строк с тройными кавычками)
# ============================================================

PAYMENT_DETAILS = (
    e('payment_btn') + " <b>РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ</b>\n\n"
    "<pre>Банк: Юмани\n"
    "Карта: 5599002124687536\n"
    "После оплаты пришли скриншот прямо сюда"
)

def WELCOME():
    return (
        e('services') + " <b>Привет. Я бот-магазин WareonsmmBot.</b>\n\n"
        "Помогаю дизайнерам инфографики находить клиентов без ручного поиска и выгорания.\n\n"
        "Выбери раздел:"
    )

def INFOPRODUCTS_INTRO():
    return (
        e('infoproducts') + " <b>ИНФОПРОДУКТЫ</b>\n\n"
        "Готовые инструменты для самостоятельного поиска клиентов. Усиливают рассылки и повышают конверсию.\n\n"
        + e('faq_tip') + " Не заменяют систему, но кратно ускоряют результат при правильном использовании."
    )

def OFFER1_DESC():
    return (
        e('offer1') + " <b>ЭФФЕКТИВНЫЙ ОФФЕР</b>\n"
        + e('money') + " <b>180</b>\n\n"
        "Готовое решение для увеличения откликов. Тебе перестанут отвечать и начнут спрашивать.\n\n"
        + e('confirm') + " <b>Ты получаешь:</b>\n"
        "- готовый оффер, который цепляет внимание\n"
        "- проверенную структуру сообщения\n"
        "- схему первого касания, вызывающую интерес\n\n"
        + e('faq_info') + " <b>Как использовать:</b> вставил свои данные - скопировал - отправил. Пять минут и ты уже в плюсе.\n\n"
        + e('star') + " <b>Кому нужно:</b> не отвечают на сообщения, не знаешь что писать, хочешь больше откликов без тестов."
    )

def OFFER2_DESC():
    return (
        e('offer2') + " <b>PSD ОБЛОЖКА ОФФЕРА</b>\n"
        + e('money') + " <b>290</b>\n\n"
        "Сообщение с картинкой открывают в три раза чаще. Этот PSD-шаблон - твой визуальный крючок.\n\n"
        + e('confirm') + " <b>Ты получаешь:</b>\n"
        "- PSD-файл от дизайнера\n"
        "- готовую структуру под твой контент\n\n"
        + e('faq_info') + " <b>Как использовать:</b> подставляешь свои работы - крепишь к офферу - рассылаешь.\n\n"
        + e('star') + " <b>Кому нужно:</b> нет визуала под оффер, хочешь выделиться в ленте, поднять открываемость."
    )

def OFFER3_DESC():
    return (
        e('offer3') + " <b>НАБОР \"ОФФЕР + ИЗОБРАЖЕНИЕ\"</b>\n"
        + e('money') + " <b>320</b>\n\n"
        "Полный комплект: текст, который продаёт + визуал, который притягивает взгляд.\n\n"
        + e('confirm') + " <b>Ты получаешь:</b>\n"
        "- готовый оффер со структурой\n"
        "- PSD-шаблон обложки\n"
        "- инструкцию по внедрению\n\n"
        + e('star') + " <b>Кому нужно:</b> хочешь всё и сразу, без сборки по частям. Лучший стартовый набор."
    )

def SERVICES_INTRO():
    return (
        e('services') + " <b>УСЛУГИ</b>\n\n"
        "Выбери, что тебе нужно:"
    )

def SEARCH_INTRO():
    return (
        e('search') + " <b>ПОИСК КЛИЕНТОВ ПОД КЛЮЧ</b>\n\n"
        "Ты дизайнер, а не спамер. Мы берём поиск клиентов на себя.\n\n"
        + e('confirm') + " <b>Что мы делаем:</b>\n"
        "- Находим целевых селлеров под твою нишу\n"
        "- Пишем им сами - грамотно, не шаблонно\n"
        "- Делаем серию касаний до ответа\n"
        "- Передаём тебе тёплых клиентов, готовых купить\n\n"
        "Ты не пишешь всем подряд. Ты не тратишь часы на пустые диалоги. Ты просто берёшь заказы."
    )

def SEARCH_5_DESC():
    return (
        e('search_5') + " <b>5 КЛИЕНТОВ ЗА 3 ДНЯ</b>\n"
        + e('money') + " <b>1 200</b> или 700 + 30% с заказов\n\n"
        + e('message') + " 600+ касаний\n"
        + e('timer') + " Срок: 3 дня\n"
        + e('star') + " До 5 реальных клиентов\n\n"
        "<b>Для кого:</b>\n"
        "- Никогда не пробовал рассылки - протестируй систему\n"
        "- Был простой - вернись в поток без риска\n"
        "- Хочешь проверить наш подход перед крупным заказом\n\n"
        "Первые отклики в день запуска. Твоя ниша жива - докажем."
    )

def SEARCH_35_DESC():
    return (
        e('search_35') + " <b>35+ ОТКЛИКОВ В DIRECT</b>\n"
        + e('money') + " <b>4 200</b> или 2 000 + 30% с закрытых клиентов\n\n"
        + e('message') + " 5 000+ касаний\n"
        + e('timer') + " Срок: 7 дней\n"
        + e('star') + " От 35 откликов (часто 50-70)\n\n"
        "<b>Что это даёт:</b>\n"
        "- Ты перестаёшь искать клиентов - они приходят сами\n"
        "- Формируешь лист ожидания из горячих селлеров\n"
        "- Выходишь из 20к/мес в стабильные 70к+\n\n"
        "Лучшее соотношение цена/результат. Одинаково мощно для одиночек и студий."
    )

def SEARCH_70_DESC():
    return (
        e('search_70') + " <b>70+ ПЛАТЕЖЕСПОСОБНЫХ ЛИДОВ</b>\n"
        + e('money') + " <b>8 000</b> или 6 000 + 30%\n\n"
        + e('users') + " 3 исполнителя\n"
        + e('message') + " 7 000+ касаний\n"
        + e('timer') + " 2 недели\n"
        + e('star') + " 70+ откликов (до 120)\n\n"
        "<b>Ключевое отличие:</b> мы ищем селлеров с бюджетом. Твой средний чек x2.\n\n"
        "<b>Для тех, кто:</b>\n"
        "- Умеет продавать, но нужен поток горячих лидов\n"
        "- Хочет забыть о ценовых возражениях\n"
        "- Готов зарабатывать по рынку, а не демпинговать"
    )

def SEARCH_120_DESC():
    return (
        e('search_120') + " <b>120+ PREMIUM ЗАЯВОК</b>\n"
        + e('money') + " <b>13 800</b> или 10 000 + 30%\n\n"
        + e('users') + " 5 рассыльщиков\n"
        + e('message') + " 12 000+ касаний\n"
        + e('timer') + " 3-4 недели\n"
        + e('star') + " 120+ откликов (до 200+)\n\n"
        "<b>Полноценный отдел продаж на аутсорсе.</b> Мы делаем всё - ты только выполняешь заказы.\n\n"
        "<b>Для:</b> крупных студий и профи, готовых масштабироваться. Вопрос \"где брать клиентов\" исчезнет навсегда."
    )

def EXTRA_RETOUCH_DESC():
    return (
        e('extra_retouch') + " <b>ПОВТОРНЫЕ КАСАНИЯ</b>\n"
        + e('money') + " <b>650</b> (50% базы) / <b>1 300</b> (100% базы)\n\n"
        "Пишем тем, кто не ответил. Другой заход, другая логика. Конверсия вырастает в 1,5-2 раза.\n\n"
        "Рекомендуем 100% - окупается с первого же закрытого клиента."
    )

def EXTRA_SPEED_DESC():
    return (
        e('extra_speed') + " <b>УСКОРЕНИЕ РЕЗУЛЬТАТА</b>\n"
        + e('money') + " <b>1 500</b>\n\n"
        "Сокращаем сроки на 45-60%. Подключаем +1-3 исполнителя.\n\n"
        "Когда результат нужен вчера, а каждый день ожидания - упущенная прибыль."
    )

def BASES_INTRO():
    return (
        e('bases') + " <b>БАЗЫ СЕЛЛЕРОВ</b>\n\n"
        "Подбираем список потенциальных клиентов под твою нишу. Активные селлеры из открытых источников.\n\n"
        + e('confirm') + " <b>Ты получаешь:</b>\n"
        "- список активных продавцов\n"
        "- сегментированную аудиторию\n"
        "- готовую базу для немедленного запуска\n\n"
        + e('warning') + " <b>ВАЖНО:</b>\n"
        "- Данные из открытых источников, могут терять актуальность\n"
        "- Не гарантируем ответ каждого - только объём и релевантность\n"
        "- Результат зависит от оффера и подачи\n"
        "- Возврата нет после выполнения"
    )

def BASES_1000_DESC():
    return e('package') + " <b>База 1 000 селлеров</b> - " + e('money') + " <b>160</b>\nОтличный старт для теста ниши."

def BASES_5000_DESC():
    return e('bases') + " <b>База 5 000 селлеров</b> - " + e('money') + " <b>490</b>\nЗолотая середина для стабильных заказов."

def BASES_10000_DESC():
    return e('package') + " <b>База 10 000 селлеров</b> - " + e('money') + " <b>790</b>\nОбъём для системной работы."

def BASES_20000_DESC():
    return e('bases') + " <b>База 20 000 селлеров</b> - " + e('money') + " <b>1 290</b>\nМаксимальный охват всей ниши."

def FAQ():
    return (
        e('faq') + " <b>ЧАСТЫЕ ВОПРОСЫ</b>\n\n"
        "Выбери вопрос - я отвечу:"
    )

FAQ_ANSWERS = {
    "faq_q1":  "Первые отклики чаще всего появляются уже в день запуска.",
    "faq_q2":  "Базы полностью законны и безопасны - сбор из открытых источников.",
    "faq_q3":  "Рассылки ведут профессионалы с опытом. Мы используем эффективные стратегии и повторные касания.",
    "faq_q4":  "Собираем из открытых источников. Никаких утечек и запрещённых методов.",
    "faq_q5":  "Работаем с нишами инфографики и графического дизайна.",
    "faq_q6":  "Не устроил результат - гарантируем отклики и заявки согласно тарифу.",
    "faq_q7":  "Скрытых доплат нет. Платишь только за выбранный товар или услугу.",
    "faq_q8":  "Офферы составлены профессионалами и многократно проверены в реальных рассылках.",
    "faq_q9":  "Используем обширные базы и сегментацию по нишам.",
    "faq_q10": "Да, работают. Доказано на своём опыте и кейсах клиентов.",
    "faq_q11": "Можем прислать скриншоты переписок по запросу.",
    "faq_q12": "Приводим тёплых лидов, готовых к покупке.",
    "faq_q13": "Зависит от тарифа, но часто цифра превышает гарантированный минимум.",
    "faq_q14": "Поиск клиентов для бизнеса через систему касаний, базы и рассылки.",
}

def SUCCESS_PAYMENT():
    return (
        e('success') + " <b>СКРИНШОТ ПОЛУЧЕН.</b>\n\n"
        "Менеджер проверит оплату и выдаст товар. Обычно это до 15 минут."
    )

def SUPPORT_MSG():
    return (
        e('support') + " <b>ПОДДЕРЖКА</b>\n\n"
        "Напиши свой вопрос сюда - ответим в ближайшее время."
    )

# ============================================================
# КЛАВИАТУРЫ
# ============================================================
def main_menu_kb():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Услуги"))
    builder.add(KeyboardButton(text="Инфопродукты"))
    builder.add(KeyboardButton(text="FAQ"))
    builder.add(KeyboardButton(text="Поддержка"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

def services_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Поиск клиентов под ключ", callback_data="service_search"))
    builder.add(InlineKeyboardButton(text="Базы селлеров", callback_data="service_bases"))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def search_packages():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="5 клиентов за 3 дня (1200)", callback_data="view_search_5"))
    builder.add(InlineKeyboardButton(text="35+ откликов (4200)", callback_data="view_search_35"))
    builder.add(InlineKeyboardButton(text="70+ лидов (8000)", callback_data="view_search_70"))
    builder.add(InlineKeyboardButton(text="120+ Premium (13800)", callback_data="view_search_120"))
    builder.add(InlineKeyboardButton(text="Повторные касания", callback_data="view_retouch"))
    builder.add(InlineKeyboardButton(text="Ускорение результата", callback_data="view_speed"))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="services"))
    builder.adjust(1)
    return builder.as_markup()

def bases_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="1 000 шт (160)", callback_data="checkout_bases_1000"))
    builder.add(InlineKeyboardButton(text="5 000 шт (490)", callback_data="checkout_bases_5000"))
    builder.add(InlineKeyboardButton(text="10 000 шт (790)", callback_data="checkout_bases_10000"))
    builder.add(InlineKeyboardButton(text="20 000 шт (1290)", callback_data="checkout_bases_20000"))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="services"))
    builder.adjust(1)
    return builder.as_markup()

def infoproducts_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Эффективный оффер (180)", callback_data="checkout_offer1"))
    builder.add(InlineKeyboardButton(text="PSD обложка (290)", callback_data="checkout_offer2"))
    builder.add(InlineKeyboardButton(text="Набор Оффер+Изображение (320)", callback_data="checkout_offer3"))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="main_menu"))
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
    builder.add(InlineKeyboardButton(text="Назад", callback_data="main_menu"))
    builder.adjust(1)
    return builder.as_markup()

def back_button(callback: str):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Назад", callback_data=callback))
    return builder.as_markup()

# ============================================================
# ОБРАБОТЧИКИ
# ============================================================
router = Router()

@router.message(F.text == "тест")
async def test_emoji(message: Message):
    await message.answer('<tg-emoji emoji-id="5906975484054345026">.</tg-emoji> проверка премиум эмодзи', parse_mode='HTML')
    
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_sticker(STICKER_WELCOME)
    await message.answer("Привет. Я бот-магазин.", reply_markup=main_menu_kb())

@router.message(F.text == "Услуги")
async def services(message: Message):
    await message.answer(SERVICES_INTRO(), parse_mode='HTML', reply_markup=services_menu())

@router.message(F.text == "Инфопродукты")
async def infoproducts(message: Message):
    await message.answer(INFOPRODUCTS_INTRO(), parse_mode='HTML', reply_markup=infoproducts_menu())

@router.message(F.text == "FAQ")
async def faq(message: Message):
    await message.answer(FAQ(), parse_mode='HTML', reply_markup=faq_menu())

@router.message(F.text == "Поддержка")
async def support(message: Message):
    await message.answer(SUPPORT_MSG(), parse_mode='HTML')

@router.callback_query(F.data == "main_menu")
async def back_main(call: CallbackQuery):
    await call.message.answer(WELCOME(), parse_mode='HTML', reply_markup=main_menu_kb())
    await call.answer()

@router.callback_query(F.data == "services")
async def back_services(call: CallbackQuery):
    await call.message.answer(SERVICES_INTRO(), parse_mode='HTML', reply_markup=services_menu())
    await call.answer()

@router.callback_query(F.data == "service_search")
async def search_intro(call: CallbackQuery):
    await call.message.answer(SEARCH_INTRO(), parse_mode='HTML', reply_markup=search_packages())
    await call.answer()

@router.callback_query(F.data.startswith("view_search_"))
async def view_search_package(call: CallbackQuery):
    texts = {
        "view_search_5":   SEARCH_5_DESC,
        "view_search_35":  SEARCH_35_DESC,
        "view_search_70":  SEARCH_70_DESC,
        "view_search_120": SEARCH_120_DESC,
    }
    text = texts.get(call.data, lambda: "Неизвестный пакет")()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Оставить заявку", callback_data=call.data.replace("view", "order")))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="service_search"))
    await call.message.answer(text, parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()

@router.callback_query(F.data.startswith("order_search_"))
async def order_search(call: CallbackQuery):
    msg = e('confirm') + " <b>Отлично.</b>\n\nНапиши сюда:\n1. Твою нишу\n2. Ссылку на портфолио\n3. Контакт для связи\n\nЯ передам менеджеру."
    await call.message.answer(msg, parse_mode='HTML')
    for admin_id in ADMIN_IDS:
        await call.bot.send_message(
            admin_id,
            "Новая заявка.\nПользователь: @" + str(call.from_user.username) + " (ID " + str(call.from_user.id) + ")\nПакет: " + call.data
        )
    await call.answer()

@router.callback_query(F.data == "view_retouch")
async def view_retouch(call: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Заказать (650 / 1300)", callback_data="order_retouch"))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="service_search"))
    await call.message.answer(EXTRA_RETOUCH_DESC(), parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()

@router.callback_query(F.data == "order_retouch")
async def order_retouch(call: CallbackQuery):
    await call.message.answer(e('confirm') + " Напиши, какой объём базы (50% или 100%) и свои контакты. Передам менеджеру.", parse_mode='HTML')
    for admin_id in ADMIN_IDS:
        await call.bot.send_message(admin_id, "Заявка на повторные касания от @" + str(call.from_user.username))
    await call.answer()

@router.callback_query(F.data == "view_speed")
async def view_speed(call: CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Заказать ускорение (1500)", callback_data="order_speed"))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="service_search"))
    await call.message.answer(EXTRA_SPEED_DESC(), parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()

@router.callback_query(F.data == "order_speed")
async def order_speed(call: CallbackQuery):
    await call.message.answer(e('confirm') + " Напиши свои контакты - подключу ускорение.", parse_mode='HTML')
    for admin_id in ADMIN_IDS:
        await call.bot.send_message(admin_id, "Заявка на ускорение от @" + str(call.from_user.username))
    await call.answer()

@router.callback_query(F.data == "service_bases")
async def bases_intro(call: CallbackQuery):
    await call.message.answer(BASES_INTRO(), parse_mode='HTML', reply_markup=bases_menu())
    await call.answer()

@router.callback_query(F.data.startswith("checkout_"))
async def checkout(call: CallbackQuery):
    data = call.data
    items = {
        "checkout_offer1":      ("Эффективный оффер", 180),
        "checkout_offer2":      ("PSD обложка оффера", 290),
        "checkout_offer3":      ("Набор Оффер+Изображение", 320),
        "checkout_bases_1000":  ("База 1000 селлеров", 160),
        "checkout_bases_5000":  ("База 5000 селлеров", 490),
        "checkout_bases_10000": ("База 10000 селлеров", 790),
        "checkout_bases_20000": ("База 20000 селлеров", 1290),
    }
    item_name, price = items.get(data, ("Неизвестный товар", 0))
    text = (
        PAYMENT_DETAILS + "\n\n"
        + e('package') + " <b>Твой заказ:</b> " + item_name + "\n"
        + e('money') + " <b>Сумма к оплате:</b> " + str(price) + "\n\n"
        + e('warning') + " <b>Важно:</b> в комментарии к переводу ничего не пиши.\n\n"
        "После оплаты пришли скриншот <b>одним сообщением</b> прямо в этот чат."
    )
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Я оплатил, прислать скриншот", callback_data="paid_" + data))
    builder.add(InlineKeyboardButton(text="Назад", callback_data="main_menu"))
    builder.adjust(1)
    await call.message.answer(text, parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()

@router.callback_query(F.data.startswith("paid_"))
async def ask_screenshot(call: CallbackQuery):
    await call.message.answer(e('confirm') + " Жду скриншот оплаты. Отправь его прямо сюда одним сообщением.", parse_mode='HTML')
    await call.answer()

@router.message(F.photo)
async def payment_screenshot(message: Message):
    user = message.from_user
    await add_order(user.id, "manual_checkout", 0, status="pending_verification")
    for admin_id in ADMIN_IDS:
        await message.forward(admin_id)
        caption = (
            "НОВЫЙ ПЛАТЕЖ НА ПРОВЕРКУ.\n"
            "Пользователь: @" + str(user.username) + " (ID: " + str(user.id) + ")\n"
            "Проверь скриншот и подтверди выдачу вручную."
        )
        await message.bot.send_message(admin_id, caption)
    await message.answer(SUCCESS_PAYMENT(), parse_mode='HTML', reply_markup=main_menu_kb())

@router.callback_query(F.data.startswith("faq_q"))
async def faq_answer(call: CallbackQuery):
    answer = FAQ_ANSWERS.get(call.data, "Ответ не найден.")
    await call.message.answer(e('faq_info') + " " + answer, parse_mode='HTML', reply_markup=back_button("faq_menu"))
    await call.answer()

@router.callback_query(F.data == "faq_menu")
async def back_faq(call: CallbackQuery):
    await call.message.answer(FAQ(), parse_mode='HTML', reply_markup=faq_menu())
    await call.answer()

@router.message(F.text, lambda msg: msg.text not in ["Услуги", "Инфопродукты", "FAQ", "Поддержка"])
async def forward_to_admin(message: Message):
    for admin_id in ADMIN_IDS:
        await message.forward(admin_id)
    await message.answer(e('confirm') + " Твоё сообщение отправлено. Ответим в ближайшее время.", parse_mode='HTML')

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
