from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler

MY_TOKEN = 'Убрано по просьбе gitguard'

keyboard = [
    ['/room1'],
    ['/room2'],
    ['/room3', '/room4']
]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)

room_states = {
    'room1': {
        'text': 'В данном зале представлена коллекция артефактов Российской империи. ',
        'next_rooms': ['room2', 'exit']
    },
    'room2': {
        'text': 'В данном зале представлена выставка достижений Российской Империи.',
        'next_rooms': ['room1', 'room3']
    },
    'room3': {
        'text': 'В данном зале представлена экспозиция, посвященная историческим событиям Российской империи.',
        'next_rooms': ['room2', 'room1', 'room4']
    },
    'room4': {
        'text': 'В данном зале представлены предметы быта Российской Империи',
        'next_rooms': ['room1', 'room3']
    }
}


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!',
                                   reply_markup=markup)
    await room1(update, context)


async def exit(update, context):
    current_room = context.user_data.get('current_room')
    if current_room == 'room1':
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!',
                                       reply_markup=ReplyKeyboardRemove())
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Выход находится только в первой комнате (room1).')


async def room1(update, context):
    context.user_data['current_room'] = 'room1'
    room = room_states['room1']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=room['text'])
    next_rooms = room['next_rooms']
    reply_keyboard = [[f'/{room}' for room in next_rooms]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Доступные комнаты:',
                                   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


async def room2(update, context):
    room = room_states['room2']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=room['text'])
    next_rooms = room['next_rooms']
    reply_keyboard = [[f'/{room}' for room in next_rooms]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Доступные комнаты:',
                                   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


async def room3(update, context):
    room = room_states['room3']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=room['text'])
    next_rooms = room['next_rooms']
    reply_keyboard = [[f'/{room}' for room in next_rooms]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Доступные комнаты:',
                                   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


async def room4(update, context):
    room = room_states['room4']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=room['text'])
    next_rooms = room['next_rooms']
    reply_keyboard = [[f'/{room}' for room in next_rooms]]
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Доступные комнаты:',
                                   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))


def main():
    application = Application.builder().token(MY_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    exit_handler = CommandHandler('exit', exit)
    application.add_handler(exit_handler)

    room1_handler = CommandHandler('room1', room1)
    application.add_handler(room1_handler)

    room2_handler = CommandHandler('room2', room2)
    application.add_handler(room2_handler)

    room3_handler = CommandHandler('room3', room3)
    application.add_handler(room3_handler)

    room4_handler = CommandHandler('room4', room4)
    application.add_handler(room4_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
