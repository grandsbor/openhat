#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

from game import Game


START_BUTTON_TEXT = 'Поехали'
WORD_EXPLAINED_BUTTON_TEXT = 'Отгадано'
WORD_SKIPPED_BUTTON_TEXT = 'Пропустить'


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
    if 'game' not in context.bot_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Игра не начата. Чтобы начать игру, скажите /new")
        return False
    return True


def broadcast(context, msg):
    context.bot.send_message(chat_id=context.bot_data['common_chat_id'], text=msg)


def new_game(update, context):
    # TODO check that chat is not 1-on-1 with bot
    if 'game' not in context.bot_data:
        chat_id = update.effective_chat.id
        context.bot_data['game'] = Game()
        context.bot_data['common_chat_id'] = chat_id
        context.bot.send_message(chat_id, text="Начинаем новую игру. Чтобы зарегистрироваться, напишите /reg")


def register(update, context):
    if check_game_exists(context, update):
        if context.bot_data['game'].add_player(update.message.from_user):
            broadcast(context, "Записал, @{}".format(update.message.from_user.username))


def next_turn(context):
    try:
        game = context.bot_data['game']
        explainer, guesser = game.next_turn()
        context.bot_data['explainer'] = explainer[0]
        broadcast(context, "Сейчас объясняет @{}, отгадывает @{}".format(explainer[1], guesser[1]))
        context.bot.send_message(chat_id=explainer[0],
                                 text="Твоя очередь объяснять, отгадывает @{}. Нажми кнопку по готовности.".format(guesser[1]),
                                 reply_markup=ReplyKeyboardMarkup.from_button(START_BUTTON_TEXT, resize_keyboard=True, one_time_keyboard=True),
                                )
    except StopIteration:
        finish_game(context)


def start_game(update, context):
    if check_game_exists(context, update):
        game = context.bot_data['game']
        if game.started:
            return
        try:
            game.start(context.args)
            players_list = ', '.join('@{}'.format(u) for u in game.players.values())
            broadcast(context, "Внимание, начинаем игру. Игроки: {}. Кругов: {}".format(players_list, game.rounds))
            next_turn(context)
        except Exception as e:
            broadcast(context, "Не удалось начать игру: {}".format(e))


def finish_game(context):
    game = context.bot_data['game']
    stats = game.finish()
    broadcast(context, "Всем спасибо, игра окончена.")
    # TODO write some stats
    del context.bot_data['game']


def end_explain(context):
    context.bot.send_message(context.job.context, text="Кончилось твоё время!", reply_markup=ReplyKeyboardRemove())
    # TODO hide buttons
    next_turn(context)


def explain_cb(update, context):
    # TODO check that current player is correct
    chat_id = update.effective_chat.id
    # the main part is here
    # TODO log ok/skip if present
    game = context.bot_data['game']
    word = game.next_word(chat_id)
    context.bot.send_message(chat_id,
                             text="Ваше слово - {}".format(word),
                             reply_markup=ReplyKeyboardMarkup([[WORD_EXPLAINED_BUTTON_TEXT, WORD_SKIPPED_BUTTON_TEXT]], resize_keyboard=True, one_time_keyboard=True))
    if len(context.job_queue.jobs()) == 0:
        context.job_queue.run_once(end_explain, 10, context=chat_id)


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
    dispatcher.add_handler(CommandHandler('reg', register))
    dispatcher.add_handler(MessageHandler(Filters.text([START_BUTTON_TEXT, WORD_EXPLAINED_BUTTON_TEXT, WORD_SKIPPED_BUTTON_TEXT]), explain_cb))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("run {} <token_file>\n".format(sys.argv[0]))
        sys.exit(1)
    main(sys.argv[1])
