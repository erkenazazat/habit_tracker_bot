import telebot
from apscheduler.schedulers.background import BackgroundScheduler
import config
from handlers import register_handlers
from features import register_features, Dynamic_Notification_Scheduler

bot = telebot.TeleBot(config.TOKEN)

register_features(bot)
register_handlers(bot)

scheduler = BackgroundScheduler()
scheduler.add_job(Dynamic_Notification_Scheduler, 'interval', minutes=1, args=[bot])
scheduler.start()

if __name__ == "__main__":
    print("Модульный бот успешно запущен...")
    bot.infinity_polling()