from django.conf import settings

import telebot  # noqa

# Create your send telegram messages here.


# Send Telegram Message (data transaction processing user)
def send_message_telegram(message):
    bot = telebot.TeleBot(settings.BOT_TELEGRAM_TOKEN)
    bot.send_message(settings.BOT_TELEGRAM_ID, message)
