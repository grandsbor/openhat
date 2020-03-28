#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

from game import Game


START_BUTTON_TEXT = 'Поехали'


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
    # TODO check that chat is not 1-on-1 with bot
    if 'game' not in context.chat_data:
        context.chat_data['game'] = Game()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Начинаем новую игру. Чтобы зарегистрироваться, напишите '+', 'да' или 'я'")


def register(update, context):
    if check_game_exists(context, update):
        if context.chat_data['game'].add_player(update.message.from_user):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Записал, @{}".format(update.message.from_user.username))


def start_game(update, context):
    def broadcast(msg):
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg)

    if check_game_exists(context, update):
        game = context.chat_data['game']
        if game.started:
            return
        try:
            game.start(context.args)
            players_list = ', '.join('@{}'.format(u) for u in game.players.values())
            broadcast("Внимание, начинаем игру. Игроки: {}. Кругов: {}".format(players_list, game.rounds))
        except Exception as e:
            broadcast("Не удалось начать игру: {}".format(e))

        for explainer, guesser in game.next_turn():
            broadcast("Сейчас объясняет @{}, отгадывает @{}".format(explainer[1], guesser[1]))
            context.bot.send_message(chat_id=explainer[0],
                                     text="Твоя очередь объяснять, отгадывает @{}. Нажми кнопку по готовности.".format(guesser[1]),
                                     reply_markup=ReplyKeyboardMarkup.from_button(START_BUTTON_TEXT, resize_keyboard=True, one_time_keyboard=True),
                                    )


def start_explain(update, context):
    # TODO check that correct player pushed the button
    context.bot.send_message(chat_id=update.effective_chat.id, text="Здесь будут появляться слова и запускаться таймер.")
    context.game.finish()


def read_token(token):
    with open(token) as fh:
        return fh.read().strip()


def main(token):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                         level=logging.DEBUG)

    updater = Updater(token=read_token(token), use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['start', 'help'], help))
    dispatcher.add_handler(CommandHandler('new', new_game))
    dispatcher.add_handler(CommandHandler('go', start_game))
    dispatcher.add_handler(MessageHandler(Filters.text(['+', 'да', 'я']), register))
    dispatcher.add_handler(MessageHandler(Filters.text(START_BUTTON_TEXT), start_explain))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("run {} <token_file>\n".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
