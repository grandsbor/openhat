from telegram.ext import Updater, CommandHandler
import logging


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Я бот для игры в Шляпу, но я пока ничего не умею :(")


def read_token():
    with open('token') as fh:
        return fh.read().strip()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.INFO)

    updater = Updater(token=read_token(), use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
        main()
