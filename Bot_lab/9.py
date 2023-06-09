import requests
import os
from PIL import Image
from typing import Tuple, Optional
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, filters, MessageHandler, Application, CallbackContext
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR)

MY_TOKEN = 'Убрано по просьбе gitguard'
YANDEX_GEOCODER_API_KEY = 'Убрано по просьбе gitguard'


async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Добро пожаловать! Отправьте мне запрос для геокодирования.')


async def exit(update: Update, context: CallbackContext):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Всего доброго!')


async def geocode(query: str) -> Tuple[Optional[Image.Image], str]:
    api_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_GEOCODER_API_KEY}&geocode={query}&format=json"

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if 'response' in data and 'GeoObjectCollection' in data['response']:
            geo_objects = data['response']['GeoObjectCollection']['featureMember']
            if geo_objects:
                location = geo_objects[0]['GeoObject']['Point']['pos']
                lon, lat = map(float, location.split())

                map_url = f'https://static-maps.yandex.ru/1.x/?ll={lon},{lat}&size=500,400&z=12&l=map'

                map_image = Image.open(requests.get(map_url, stream=True).raw)

                annotation = f'**{query}**\n\n[Открыть на карте]({map_url})'

                return map_image, annotation

        print(f'Нет данных о месте: {query}')

    except requests.HTTPError as http_err:
        print(f'Произошла ошибка HTTP: {http_err}')
    except Exception as err:
        print(f'Произошла ошибка: {err}')

    return None, ''


async def process_text(update: Update, context: CallbackContext):
    query = update.message.text
    map_image, annotation = await geocode(query)

    if map_image is not None:
        map_image = map_image.convert('RGB')
        map_image_path = 'map_image.jpg'
        map_image.save(map_image_path)

        caption = annotation

        with open(map_image_path, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=caption,
                parse_mode=ParseMode.MARKDOWN
            )

        os.remove(map_image_path)
    else:
        print(f'Не удалось выполнить геокодирование для запроса: {query}')
        await update.message.reply_text('Ничего не найдено.')


def main():
    application = Application.builder().token(MY_TOKEN).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    exit_handler = CommandHandler('exit', exit)
    application.add_handler(exit_handler)

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, process_text)
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
