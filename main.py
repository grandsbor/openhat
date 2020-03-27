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
/new - начать регистрацию на новую игру
/go 2 - стартовать игру, 2 круга
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text=HELP_MESSAGE)


def check_game_exists(context, update):
    if 'game' not in context.chat_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра не начата. Чтобы начать игру, скажите /new")
        return False
    return True


def new_game(update, context):
    if 'game' not in context.chat_data:
        context.chat_data['game'] = Game()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Начинаем новую игру. Чтобы зарегистрироваться, напишите '+', 'да' или 'я'")


def start_game(update, context):
    if check_game_exists(context, update):
        game = context.chat_data['game']
        if not game.started:
            try:
                game.start(context.args)
                players_list = ', '.join('@{}'.format(u) for u in game.players.values())
                context.bot.send_message(chat_id=update.effective_chat.id, text="Внимание, начинаем игру. Игроки: {}. Кругов: {}".format(players_list, game.rounds))
            except Exception as e:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось начать игру: {}".format(e))


def register(update, context):
    if check_game_exists(context, update):
        if context.chat_data['game'].add_player(update.message.from_user):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Записал, @{}".format(update.message.from_user.username))


def read_token():
    with open('token') as fh:
        return fh.read().strip()


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.DEBUG)

    updater = Updater(token=read_token(), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['start', 'help'], help))
    dispatcher.add_handler(CommandHandler('new', new_game))
    dispatcher.add_handler(CommandHandler('go', start_game))
    dispatcher.add_handler(MessageHandler(Filters.text(['+', 'да', 'я']), register))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
