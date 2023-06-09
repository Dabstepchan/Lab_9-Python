import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from telegram.ext import Application, CommandHandler

MY_TOKEN = 'Убрано по просьбе gitguard'
BASE_URL = 'https://scrapingclub.com/exercise/list_basic/'


async def start(update, context):
    await update.message.reply_text("Привет! Я бот, который поможет найти нужный товар. "
                                    "Используй команду /price. Обязательно укажи цену после пробела.")

    try:
        context.user_data['products']
    except KeyError:
        context.user_data['products'] = []


async def product(update, context):
    request_base = 'https://scrapingclub.com'
    price = float(context.args[0])
    minimum_difference = 100
    closest_product = None

    for page_number in range(1, 9):
        request_url = f'https://scrapingclub.com/exercise/list_basic/?page={page_number}'

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(request_url) as response:
                    html_text = await response.text()
        except aiohttp.ClientError as err:
            await update.message.reply_text(f"Ошибка при выполнении HTTP-запроса: {err}")
            return

        soup = BeautifulSoup(html_text, "html.parser")

        for product_tag in soup.find_all('div', class_='card'):
            if product_tag.h5 is None:
                continue

            product_info = product_tag.find_all('a')

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(urljoin(request_base, product_info[0]['href'])) as response:
                        html_text1 = await response.text()
            except aiohttp.ClientError as err:
                await update.message.reply_text(f"Ошибка при выполнении HTTP-запроса: {err}")
                return

            info1 = BeautifulSoup(html_text1, "html.parser").find_all("meta")

            product_name = product_info[1].text.strip()
            product_description = info1[3]['content'].strip()
            product_photo = urljoin(request_base, product_info[0].find('img')['src'])
            product_price = float(product_tag.h5.text.replace('$', ''))

            context.user_data['products'].append([product_name, product_description, product_photo, product_price])

    context.user_data['products'].sort(key=lambda x: [x[0], x[3]])

    prices = [product[3] for product in context.user_data['products']]

    for product in context.user_data['products']:
        difference = abs(price - product[3])
        if difference == 0:
            closest_product = product
            break
        elif difference < minimum_difference:
            minimum_difference = difference
            closest_product = product

    if closest_product:
        message = f"Название: {closest_product[0]}\n"
        message += f"Описание: {closest_product[1]}\n"
        message += f"Цена: {closest_product[3]}\n"
        message += f"Фото: {closest_product[2]}"
    else:
        message = "Товар не найден."

    await update.message.reply_text(message)


def main():
    application = Application.builder().token(MY_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('price', product))
    application.run_polling()


if __name__ == '__main__':
    main()
