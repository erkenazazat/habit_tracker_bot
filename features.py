from datetime import datetime, timedelta
from models import HabitManager

manager = HabitManager()

EXTRA_LOCALIZATION = {
    "ru": {
        "help_text": "💡 *Руководство пользователя*\n\n1️⃣ Нажмите 'Добавить привычку'.\n2️⃣ Укажите время и выберите дни.\n3️⃣ Отмечайте выполнение.\n⚠️ Пропуск дня сбросит streak!",
        "sug_title": "💡 *Популярные привычки для вас:*",
        "profile_text": "👤 *Ваш профиль:*\n\n📊 Всего привычек: {0}\n🔥 Лучшая серия (Max Streak): {1} дн.",
        "remind": "⏰ *Напоминание!* Через 15 минут начнется привычка: "
    },
    "kk": {
        "help_text": "💡 *Қолданушы нұсқаулығы*\n\n1️⃣ 'Әдет қосу' батырмасын басыңыз.\n2️⃣ Уақыты мен күндерін таңдаңыз.\n3️⃣ Орындалуын белгілеңіз.\n⚠️ Бір күнді өткізіп алсаңыз, серияңыз күйеді!",
        "sug_title": "💡 *Сізге арналған танымал әдеттер:*",
        "profile_text": "👤 *Сіздің профиліңіз:*\n\n📊 Жалпы әдеттер саны: {0}\n🔥 Ең үздік серия (Max Streak): {1} күн",
        "remind": "⏰ *Ескерту!* 15 минуттан кейін әдет басталады: "
    },
    "en": {
        "help_text": "💡 *User Manual*\n\n1️⃣ Click 'Add Habit'.\n2️⃣ Set time and select target days.\n3️⃣ Check your daily progress.\n⚠️ Missing a day will reset your streak!",
        "sug_title": "💡 *Recommended habits for you:*",
        "profile_text": "👤 *Your Profile:*\n\n📊 Total habits: {0}\n🔥 Max Streak: {1} days",
        "remind": "⏰ *Reminder!* In 15 minutes your habit will start: "
    }
}


# Функция прямой обработки для вызова из handlers.py
def handle_features_direct(bot, message):
    uid = message.chat.id
    lang = manager.get_language(uid)

    # Свежие данные загружаем прямо из менеджера
    manager.data = manager._load_data()

    if message.text in ["👤 Профиль", "👤 Profile"]:
        total, streak = manager.get_profile_stats(uid)
        text = EXTRA_LOCALIZATION[lang]["profile_text"].format(total, streak)
        bot.send_message(uid, text, parse_mode="Markdown")

    elif message.text in ["💡 Идеи", "💡 Идеялар", "💡 Suggestions"]:
        suggestions = manager.load_suggestions(lang)
        sug_text = EXTRA_LOCALIZATION[lang]["sug_title"] + "\n\n" + "\n".join(suggestions)
        bot.send_message(uid, sug_text, parse_mode="Markdown")

    elif message.text in ["ℹ️ Помощь", "ℹ️ Көмек", "ℹ️ Help"]:
        bot.send_message(uid, EXTRA_LOCALIZATION[lang]["help_text"], parse_mode="Markdown")


def register_features(bot):
    @bot.message_handler(
        func=lambda msg: msg.text in ["👤 Профиль", "👤 Profile", "💡 Идеи", "💡 Идеялар", "💡 Suggestions", "ℹ️ Помощь",
                                      "ℹ️ Көмек", "ℹ️ Help"])
    def handle_features(message):
        handle_features_direct(bot, message)


# Функция планировщика для уведомлений
def Dynamic_Notification_Scheduler(bot):
    now = datetime.now()
    target_time = now + timedelta(minutes=15)
    target_time_str = target_time.strftime("%H:%M")
    current_day_index = now.weekday()

    # Перед запуском планировщика обновляем данные из файла json
    manager.data = manager._load_data()
    all_data = manager.data.get("users", {})
    for user_id, habits in all_data.items():
        lang = manager.get_language(user_id)
        for h in habits:
            if h["time_str"] == target_time_str and current_day_index in h["days_list"]:
                try:
                    text = f"{EXTRA_LOCALIZATION[lang]['remind']} *{h['name']}* ({h['time_str']})!"
                    bot.send_message(int(user_id), text, parse_mode="Markdown")
                except Exception as e:
                    print(f"Ошибка отправки: {e}")