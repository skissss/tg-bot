import random
import telebot
import os
from dotenv import load_dotenv

from config import (
    BOT_GAME_LIST,
    GAME_CHOICES,
    HELLO_LIST,
    INFO_LIST,
    MISUNDERSTANDING_STICKERS,
)


load_dotenv()

API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(API_KEY)
predict_message = False


@bot.message_handler(commands=["start"])
def start(message):
    print("start called")
    bot.send_message(
        message.chat.id,
        "отправь мне что небудь:)"
        "\n(можешь написать (инфо) или просто поздароваться)"
        "\nдля игр: играть(орел или решка)"
        "\n /predict ну там увидишь",
    )


@bot.message_handler(commands=["predict"])
def predict_response(message):
    print("predict_response called")
    bot.send_message(
        message.chat.id, "задайте вопрос на который можно ответить да или нет"
    )
    bot.send_message(message.chat.id, "🪄")
    global predict_message
    predict_message = True


@bot.message_handler(func=lambda message: predict_message)
def get_user_question(message):
    print("get_user_question called")
    response = random.choice(GAME_CHOICES)
    bot.send_message(message.chat.id, response)
    global predict_message
    predict_message = False


@bot.message_handler(content_types=["text"])
def get_info(message):
    print("get_info called")
    lower_message = message.text.lower()

    if lower_message in INFO_LIST:
        bot.send_message(message.chat.id, f"id чата: {message.chat.id}")
        bot.send_message(message.chat.id, f"ваш юз: {message.chat.username}")
        bot.send_message(
            message.chat.id, f"ваше имя: {message.chat.first_name}"
        )
        # bot.send_message(message.chat.id, f"инфа про чат: {message.chat}")
    elif lower_message in HELLO_LIST:
        bot.send_message(message.chat.id, "привет")
    elif lower_message in BOT_GAME_LIST:
        bot.send_message(message.chat.id, "орел или решка?")
        bot.send_message(message.chat.id, "🪙")
        send = bot.send_message(message.chat.id, "твой вориант?:")
        bot.register_next_step_handler(send, game)
    else:
        bot.send_message(message.chat.id, "я покачто слишком глупи")
        bot.send_sticker(
            message.chat.id, random.choice(MISUNDERSTANDING_STICKERS)
        )


def game(message):
    result = random.choice(["орел", "решка"])
    if message.text.lower() in result:
        bot.send_message(message.chat.id, "правельно")
    else:
        bot.send_message(message.chat.id, f"не правельно, было: {result}")


print("bot starting...")

bot.polling(none_stop=True, interval=0)

print("bot stopped")
