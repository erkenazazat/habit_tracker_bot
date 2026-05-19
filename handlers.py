# handlers.py
from telebot import types
from datetime import datetime
from models import HabitManager, AdvancedHabit

manager = HabitManager()
user_states = {}

LOCALIZATION = {
    "ru": {
        "welcome": "Привет! Выберите действие в меню ниже 👇",
        "add_btn": "➕ Добавить привычку", "list_btn": "📋 Мои привычки",
        "profile_btn": "👤 Профиль", "sug_btn": "💡 Идеи", "help_btn": "ℹ️ Помощь", "lang_btn": "🌐 Тіл / Язык / Language",
        "enter_name": "Введите название привычки:", "enter_desc": "Введите описание привычки:",
        "enter_time": "Введите время уведомления (ЧЧ:ММ):", "select_days": "Выберите дни недели и нажмите 'Готово':",
        "done": "✅ Готово", "success_add": "Привычка успешно добавлена!", "no_habits": "У вас пока нет привычек.",
        "header": "🌳 *Ваши привычки:*", "btn_check": "🔥 Выполнено", "btn_del": "🗑 Удалить",
        "already_done": "Вы уже отмечали эту привычку сегодня!"
    },
    "kk": {
        "welcome": "Сәлем! Төмендегі мәзірден әрекетті таңдаңыз 👇",
        "add_btn": "➕ Әдет қосу", "list_btn": "📋 Менің әдеттерім",
        "profile_btn": "👤 Профиль", "sug_btn": "💡 Идеялар", "help_btn": "ℹ️ Көмек",
        "lang_btn": "🌐 Тіл / Язык / Language",
        "enter_name": "Әдеттің атауын енгізіңіз:", "enter_desc": "Әдеттің сипаттамасын енгізіңіз:",
        "enter_time": "Ескерту уақытын енгізіңіз (СС:ММ):", "select_days": "Апта күндерін таңдап, 'Дайын' басыңыз:",
        "done": "✅ Дайын", "success_add": "Әдет сәтті қосылды!", "no_habits": "Сізде әлі әдеттер жоқ.",
        "header": "🌳 *Сіздің әдеттеріңіз:*", "btn_check": "🔥 Орындалды", "btn_del": "🗑 Жою",
        "already_done": "Бұл әдетті бүгін белгілеп қойғансыз!"
    },
    "en": {
        "welcome": "Hello! Choose an action from the menu below 👇",
        "add_btn": "➕ Add Habit", "list_btn": "📋 My Habits",
        "profile_btn": "👤 Profile", "sug_btn": "💡 Suggestions", "help_btn": "ℹ️ Help",
        "lang_btn": "🌐 Тіл / Язык / Language",
        "enter_name": "Enter habit name:", "enter_desc": "Enter habit description:",
        "enter_time": "Enter notification time (HH:MM):", "select_days": "Select days of the week and click 'Done':",
        "done": "✅ Done", "success_add": "Habit successfully added!", "no_habits": "You don't have any habits yet.",
        "header": "🌳 *Your Habits:*", "btn_check": "🔥 Done", "btn_del": "🗑 Delete",
        "already_done": "You have already checked this habit today!"
    }
}

def get_main_keyboard(user_id):
    lang = manager.get_language(user_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(LOCALIZATION[lang]["add_btn"], LOCALIZATION[lang]["list_btn"])
    keyboard.add(LOCALIZATION[lang]["profile_btn"], LOCALIZATION[lang]["sug_btn"], LOCALIZATION[lang]["help_btn"])
    keyboard.add(LOCALIZATION[lang]["lang_btn"])
    return keyboard

def show_days_inline(bot, chat_id):
    lang = manager.get_language(chat_id)
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"] if lang == "ru" else (
        ["Дс", "Сс", "Ср", "Бс", "Жм", "Сб", "Жс"] if lang == "kk" else ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    buttons = [
        types.InlineKeyboardButton(f"{'✅ ' if i in user_states[chat_id]['days'] else ''}{d}", callback_data=f"day_{i}")
        for i, d in enumerate(days)]
    keyboard.add(*buttons)
    keyboard.add(types.InlineKeyboardButton(LOCALIZATION[lang]["done"], callback_data="day_done"))
    bot.send_message(chat_id, LOCALIZATION[lang]["select_days"], reply_markup=keyboard)

def show_habits(bot, chat_id):
    lang = manager.get_language(chat_id)
    habits = manager.get_user_habits(chat_id)
    if not habits:
        bot.send_message(chat_id, LOCALIZATION[lang]["no_habits"])
        return
    bot.send_message(chat_id, LOCALIZATION[lang]["header"], parse_mode="Markdown")
    for idx, h in enumerate(habits):
        obj = AdvancedHabit(h["name"], h["description"], h["time_str"], h["days_list"])
        obj.streak = h["streak"]
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(LOCALIZATION[lang]["btn_check"], callback_data=f"check_{idx}"),
                     types.InlineKeyboardButton(LOCALIZATION[lang]["btn_del"], callback_data=f"del_{idx}"))
        bot.send_message(chat_id, obj.get_info(lang), parse_mode="Markdown", reply_markup=keyboard)