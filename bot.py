# from webbrowser import get
# import telebot
from io import BytesIO
import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, message
from PIL import Image, ImageDraw

BOT_KEY = config.API_BOT
# mybot = telebot.TeleBot(config.TOKEN)
mybot = Updater(BOT_KEY, use_context=True)
dp = mybot.dispatcher

def user_welcome(update, context):
    my_keyboard = ReplyKeyboardMarkup([['Поиск цвета', 'Распознание цвета'], ['Назад']], resize_keyboard=True)
    update.message.reply_text('Приветик. Я - бот-поисковик цветов. '
                              'Пока у меня нет каких либо навыков, но мы можем поиграть в эхо)',
                              reply_markup=my_keyboard)


def image_generate(update, context):
    colours = {"Красный": (255, 0, 0, 255), "Синий": (0, 0, 255, 255), "Зеленый": (0, 255, 0, 255)}
    user_text = update.message.text
    img = Image.new('RGBA', (100, 100), colours[user_text])
    chat_id=update.effective_chat.id
    with BytesIO() as bio:
        bio.name = '{chat_id}.png'
        img.save(bio, 'PNG')
        bio.seek(0)
        mybot.bot.send_photo(chat_id=chat_id, photo=bio)


def user_find_colour(update, context):
    my_keyboard = ReplyKeyboardMarkup([['Красный', 'Синий', 'Зеленый'], ['Назад']], resize_keyboard=True)
    update.message.reply_text('Выберите стартовый цвет', reply_markup=my_keyboard)
    # user_text = update.message.text
    # update.message.reply_text(user_text)


def generate_colour(update, context, telebot=None):
    # mybot = Updater(BOT_KEY, use_context=True)

    colours = {"Красный": (255, 0, 0, 255), "Синий": (0, 0, 255, 255), "Зеленый": (0, 255, 0, 255)}
    user_text = update.message.text
    img = Image.new('RGBA', (50, 50), colours[user_text])
    img.save('image.png')
    # mybot.send_photo(message.chat.id, get("D:\PycharmProjects\ProjectTwo\image.png").content)
    # mybot.send_photo(img)
    # update.message.send_photo(img)




def main():
    dp.add_handler(MessageHandler(Filters.text('Назад'), user_welcome))
    dp.add_handler(MessageHandler(Filters.text(['Красный', 'Синий', 'Зеленый']), image_generate))
    dp.add_handler(CommandHandler("start", user_welcome))
    dp.add_handler(MessageHandler(Filters.text('Поиск цвета'), user_find_colour))
    dp.add_handler(MessageHandler(Filters.text(['Красный', 'Синий', 'Зеленый']), generate_colour))
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
