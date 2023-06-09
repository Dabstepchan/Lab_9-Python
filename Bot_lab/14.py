import discord
import random

MY_TOKEN = 'Убрано по просьбе gitguard'


class DabstepBot(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self.smileys = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇"]
        self.score = 0
        self.is_playing = False

    async def on_ready(self):
        print('Готов к игре со смайликами!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content.lower()
        if content.startswith('/stop'):
            self.score = 0
            self.is_playing = False
            await message.channel.send('Игра прервана. Счёт обнулен.')
            return

        if content.startswith('!play'):
            if self.is_playing:
                await message.channel.send('Игра уже идёт!')
                return
            else:
                self.is_playing = True
                await self.start_game(message.channel)
                return

        if not self.is_playing:
            return

        try:
            number = int(content)
        except ValueError:
            return

        if number < 1:
            await message.channel.send('Некорректное число. Введите положительное число.')
            return

        current_smiley = self.get_current_smiley()
        user_smiley = self.get_user_smiley(number)

        self.score += self.compare_smileys(user_smiley, current_smiley)

        await self.send_game_status(message.channel, user_smiley, current_smiley)
        if self.is_game_over():
            winner = "Бот" if self.score < 0 else "Вы"
            await message.channel.send(f'Игра окончена! Победитель: {winner}!')
            self.score = 0
            self.is_playing = False

    async def start_game(self, channel):
        self.score = 0
        self.is_playing = True
        await channel.send('Игра начинается! Введите номер смайлика.')

    def get_current_smiley(self):
        return random.choice(self.smileys)

    def get_user_smiley(self, number):
        remaining = len(self.smileys)
        smiley_index = (number - 1) % remaining
        return self.smileys.pop(smiley_index)

    def compare_smileys(self, user_smiley, bot_smiley):
        return ord(user_smiley) - ord(bot_smiley)

    async def send_game_status(self, channel, user_smiley, bot_smiley):
        await channel.send(f'Ваш смайлик: {user_smiley}')
        await channel.send(f'Смайлик бота: {bot_smiley}')
        await channel.send(f'Текущий счёт: {self.score}')

    def is_game_over(self):
        return len(self.smileys) == 0


intents = discord.Intents.default()
intents.message_content = True
client = DabstepBot(intents=intents)
client.run(MY_TOKEN)
