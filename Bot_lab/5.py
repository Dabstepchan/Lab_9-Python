from telegram.ext import Application, CommandHandler

MY_TOKEN = 'Убрано по просьбе gitguard'


async def time(update, context):
    import datetime
    current_time = datetime.datetime.now().strftime('%H:%M:%S')
    await context.bot.send_message(chat_id=update.message.chat_id, text=f"Current time is {current_time}")


async def date(update, context):
    import datetime
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    await context.bot.send_message(chat_id=update.message.chat_id, text=f"Current date is {current_date}")


def main():
    application = Application.builder().token(MY_TOKEN).build()

    time_handler = CommandHandler('time', time)
    date_handler = CommandHandler('date', date)

    application.add_handler(time_handler)
    application.add_handler(date_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
