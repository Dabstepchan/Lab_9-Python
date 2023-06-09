from telegram.ext import Application, MessageHandler, filters

MY_TOKEN = 'Убрано по просьбе gitguard'


async def echo(update, context):
    await context.bot.send_message(chat_id=update.message.chat_id, text=f'Я получил сообщение {update.message.text}')


def main():
    application = Application.builder().token(MY_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT, echo)

    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
