import discord
import asyncio
import re

MY_TOKEN = 'Убрано по просьбе gitguard'


class DabstepBot(discord.Client):
    async def on_ready(self):
        print('Готов к установке напоминаний!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('set_time in'):
            time_str = re.findall(r'\d+', message.content)
            if len(time_str) != 2:
                await message.channel.send('Некорректный формат времени!')
                return

            hours = int(time_str[0])
            minutes = int(time_str[1])
            if hours < 0 or minutes < 0:
                await message.channel.send('Некорректное время!')
                return

            total_seconds = hours * 3600 + minutes * 60
            await message.channel.send('Есть установить таймер товарищ капитан!')
            await self.send_reminder(message.channel, total_seconds)

    async def send_reminder(self, channel, time):
        await asyncio.sleep(time)
        await channel.send(f'Время X наступило!')


intents = discord.Intents.default()
intents.message_content = True
client = DabstepBot(intents=intents)
client.run(MY_TOKEN)
