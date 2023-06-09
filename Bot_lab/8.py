import json
import random
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters

MY_TOKEN = 'Убрано по просьбе gitguard'

keyboard = [
    ['Начать', '/exit']
]

markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False)


async def to_exit(update, context):
    await update.message.reply_text("Спасибо за участие в опросе! Буду рад видеть вас снова. До свидания.",
                                    reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def start(update, context):
    with open("quiz.json", encoding="utf8") as file:
        quiz = json.load(file)
        questions = [[quiz['quiz'][i]['question'], quiz['quiz'][i]['response']] for i in range(len(quiz['quiz']))]
        random.shuffle(questions)

        context.user_data['questions'] = questions
        context.user_data['right'] = 0
        context.user_data['current_question'] = 0

    await update.message.reply_text("Начнём наш опрос?", reply_markup=markup)

    return 1


async def survey(update, context):
    user_answer = update.message.text.lower()
    current_question = context.user_data.get('current_question', 0)
    questions = context.user_data.get('questions', [])

    correct_answer = questions[current_question][1]

    if user_answer == correct_answer.lower():
        context.user_data['right'] += 1
        print(context.user_data['right'])

    context.user_data['current_question'] = current_question + 1

    if current_question < len(questions) - 1:
        await update.message.reply_text(questions[current_question + 1][0], reply_markup=ReplyKeyboardRemove())
        return 1

    await update.message.reply_text(f"Количество правильных ответов: {context.user_data['right']}. "
                                    f"Для ещё одного прохождения используйте команду /start.")
    return ConversationHandler.END


def main():
    application = Application.builder().token(MY_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, survey)]
        },
        fallbacks=[CommandHandler('exit', to_exit)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
