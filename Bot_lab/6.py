from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler
from random import randint
import asyncio

MY_TOKEN = 'Убрано по просьбе gitguard'

keyboard = [
    ['/roll_dice', '/timer']
]

keyboard1 = [
    ['/roll_6_sided_dice', '/roll_two_6_sided_dice'],
    ['/roll_20_sided_dice', '/back']
]

keyboard2 = [
    ['/30_seconds', '/1_minute'],
    ['/5_minutes', '/back']
]

keyboard3 = [
    ['/close']
]

markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)
markup1 = ReplyKeyboardMarkup(keyboard1, one_time_keyboard=False)
markup2 = ReplyKeyboardMarkup(keyboard2, one_time_keyboard=False)
markup3 = ReplyKeyboardMarkup(keyboard3, one_time_keyboard=False)


async def start(update, context):
    await update.message.reply_text('I am a bot assistant for tabletop games. How can I help you?',
                                    reply_markup=markup)


async def roll_dice(update, context):
    await update.message.reply_text('OK', reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text('You can roll:\nOne 6-sided dice (/roll_6_sided_dice)\nTwo 6-sided dice '
                                    '(/roll_two_6_sided_dice)\nOne 20-sided dice (/roll_20_sided_dice)',
                                    reply_markup=markup1)


async def roll_6_sided_dice(update, context):
    await update.message.reply_text(randint(1, 6))


async def roll_two_6_sided_dice(update, context):
    await update.message.reply_text(f'{randint(1, 6)}, {randint(1, 6)}')


async def roll_20_sided_dice(update, context):
    await update.message.reply_text(randint(1, 20))


async def back(update, context):
    await update.message.reply_text('OK', reply_markup=ReplyKeyboardRemove())
    await start(update, context)


async def timer(update, context):
    await update.message.reply_text('OK', reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text('You can set a timer for:\n30 seconds (/30_seconds)\n1 minute (/1_minute)\n'
                                    '5 minutes (/5_minutes)', reply_markup=markup2)


async def set_timer(update, context):
    time = 30 if update.message.text == '/30_seconds' else (60 if update.message.text == '/1_minute' else 300)
    await update.message.reply_text('OK', reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(f'Set a timer for {time} seconds', reply_markup=markup3)
    await asyncio.sleep(time)
    await update.message.reply_text('OK', reply_markup=ReplyKeyboardRemove())
    await update.message.reply_text(f'{time} seconds have elapsed', reply_markup=markup2)


def main():
    application = Application.builder().token(MY_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    roll_dice_handler = CommandHandler('roll_dice', roll_dice)
    application.add_handler(roll_dice_handler)

    roll_6_sided_dice_handler = CommandHandler('roll_6_sided_dice', roll_6_sided_dice)
    application.add_handler(roll_6_sided_dice_handler)

    roll_two_6_sided_dice_handler = CommandHandler('roll_two_6_sided_dice', roll_two_6_sided_dice)
    application.add_handler(roll_two_6_sided_dice_handler)

    roll_20_sided_dice_handler = CommandHandler('roll_20_sided_dice', roll_20_sided_dice)
    application.add_handler(roll_20_sided_dice_handler)

    back_handler = CommandHandler('back', back)
    application.add_handler(back_handler)

    timer_handler = CommandHandler('timer', timer)
    application.add_handler(timer_handler)

    set_timer_handler = CommandHandler('30_seconds', set_timer)
    application.add_handler(set_timer_handler)

    set_timer_handler = CommandHandler('1_minute', set_timer)
    application.add_handler(set_timer_handler)

    set_timer_handler = CommandHandler('5_minutes', set_timer)
    application.add_handler(set_timer_handler)

    application.run_polling()
    application.idle()


if __name__ == '__main__':
    main()
