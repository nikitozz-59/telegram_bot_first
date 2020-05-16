import telebot
import requests

bot = telebot.TeleBot('1172370412:AAFjoR8RvgOQby1b0ZzZb9Y2smt3jZMMMKE')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def main():
    bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()