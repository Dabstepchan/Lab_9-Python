import discord
import requests

MY_TOKEN = 'Убрано по просьбе gitguard'
API_KEY = 'Убрано по просьбе gitguard'


class Dabstep_bot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.api_key = API_KEY
        self.location = None

    async def on_ready(self):
        print('Готов к отображению погоды!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content.lower()
        if content.startswith('/help_bot'):
            await self.send_help_message(message.channel)

        if content.startswith('/place'):
            location = content.replace('/place', '').strip()
            if location == '':
                await message.channel.send('Укажите место для прогноза погоды.')
                return
            self.location = location
            await message.channel.send(f'Место прогноза установлено: {location}')

        if content.startswith('/current'):
            if self.location is None:
                await message.channel.send('Место прогноза не указано. Используйте команду /place для задания места.')
                return

            weather_data = self.get_current_weather(self.location)
            if weather_data is not None:
                await self.send_current_weather(message.channel, self.location, weather_data)
            else:
                await message.channel.send(
                    'Не удалось получить данные о погоде. Проверьте правильность указанного места.')

        if content.startswith('/forecast'):
            if self.location is None:
                await message.channel.send('Место прогноза не указано. Используйте команду /place для задания места.')
                return

            days = content.replace('/forecast', '').strip()
            if days == '':
                await message.channel.send('Укажите количество дней для прогноза.')
                return

            forecast_data = self.get_forecast(self.location, days)
            if forecast_data is not None:
                await self.send_forecast(message.channel, self.location, forecast_data)
            else:
                await message.channel.send(
                    'Не удалось получить прогноз погоды. Проверьте правильность указанного места или количество дней.')

    async def send_help_message(self, channel):
        message = 'Список команд бота:\n'
        message += '/help_bot - Показать список команд\n'
        message += '/place [место] - Задать место для прогноза погоды\n'
        message += '/current - Получить текущую погоду\n'
        message += '/forecast [количество дней] - Получить прогноз погоды на указанное количество дней\n'
        await channel.send(message)

    def get_current_weather(self, location):
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None

    async def send_current_weather(self, channel, location, weather_data):
        temperature = weather_data['main']['temp']
        pressure = weather_data['main']['pressure']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']
        wind_direction = weather_data['wind']['deg']

        message = f'Текущая погода в {location}:\n'
        message += f'Температура: {temperature}°C\n'
        message += f'Давление: {pressure} гПа\n'
        message += f'Влажность: {humidity}%\n'
        message += f'Скорость ветра: {wind_speed} м/с\n'
        message += f'Направление ветра: {wind_direction}°\n'
        await channel.send(message)

    def get_forecast(self, location, days):
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={self.api_key}' \
              f'&units=metric&cnt={days}'

        response = requests.get(url)
        if response.status_code == 200:
            forecast = response.json()['list']
            return forecast
        return None

    async def send_forecast(self, channel, location, forecast_data):
        forecast_by_day = {}

        for item in forecast_data:
            date = item['dt_txt'].split()[0]
            if date not in forecast_by_day:
                forecast_by_day[date] = []
            forecast_by_day[date].append(item)

        for date, items in forecast_by_day.items():
            message = f'Прогноз погоды в {location} на {date}:\n'
            for item in items:
                time = item['dt_txt'].split()[1]
                temperature = item['main']['temp']
                precipitation = item['pop']
                forecast_line = f'Время: {time}, Температура: {temperature}°C, Вероятность осадков: {precipitation}%\n'

                if len(message) + len(forecast_line) > 2000:
                    await channel.send(message)
                    message = ''

                message += forecast_line

            await channel.send(message)


intents = discord.Intents.default()
intents.message_content = True
client = Dabstep_bot(intents=intents)
client.run(MY_TOKEN)
