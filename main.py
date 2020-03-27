#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
import logging

from game import Game


def help(update, context):
    HELP_MESSAGE = """
Привет, я бот для игры в шляпу. Сам я играть не умею, но могу помочь вам.

Я знаю такие команды:
/help - показать это сообщение
/new - начать новую игру
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_MESSAGE)


def new_game(update, context):
    if 'game' not in context.chat_data:
        context.chat_data['game'] = Game()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Начинаем новую игру. Чтобы зарегистрироваться, напишите '+', 'да' или 'я'")


def register(update, context):
    if 'game' not in context.chat_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра не начата. Чтобы начать игру, скажите /new")
    if context.chat_data['game'].add_player(update.message.from_user.id):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Записал, @{}".format(update.message.from_user.username))


def read_token():
    with open('token') as fh:
        return fh.read().strip()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.DEBUG)

    updater = Updater(token=read_token(), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', help))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('new', new_game))
    dispatcher.add_handler(MessageHandler(Filters.text(['+', 'да', 'я']), register))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
