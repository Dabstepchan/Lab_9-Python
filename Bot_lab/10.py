import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters

MY_TOKEN = 'Убрано по просьбе gitguard'


def translate_text(text, source_lang, target_lang):
    url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}".format(
        source_lang, target_lang, text
    )
    response = requests.get(url)
    translation = response.json()[0][0][0]
    return translation


async def start(update: Update, context):
    keyboard = ReplyKeyboardMarkup(
        [[KeyboardButton("Русский -> Английский"), KeyboardButton("Английский -> Русский")]],
        resize_keyboard=True
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я бот-переводчик. Выбери направление перевода и введи сообщение.",
        reply_markup=keyboard
    )


async def translate(update: Update, context):
    text = update.message.text
    if text.startswith("/"):
        return

    if text == "Русский -> Английский":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Введите текст для перевода с русского на английский:")
        context.user_data['translation_direction'] = "ru_to_en"
    elif text == "Английский -> Русский":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Введите текст для перевода с английского на русский:")
        context.user_data['translation_direction'] = "en_to_ru"
    else:
        translation_direction = context.user_data.get('translation_direction')
        if translation_direction == "ru_to_en":
            source_lang = "ru"
            target_lang = "en"
        elif translation_direction == "en_to_ru":
            source_lang = "en"
            target_lang = "ru"
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Выберите направление перевода!")
            return

        translated_text = translate_text(text, source_lang, target_lang)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=translated_text)


def main():
    application = Application.builder().token(MY_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, translate))
    application.run_polling()


if __name__ == '__main__':
    main()
