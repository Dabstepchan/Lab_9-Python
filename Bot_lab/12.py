import discord
import aiohttp

MY_TOKEN = 'Убрано по просьбе gitguard'


class DabstepBot(discord.Client):
    async def on_ready(self):
        print('Готов показать пёсика, котика или лису!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower() == 'пёсик!':
            await self.send_dog_image(message.channel)

        elif message.content.lower() == 'котик!':
            await self.send_cat_image(message.channel)

        elif message.content.lower() == 'лисица!':
            await self.send_fox_image(message.channel)

    async def send_dog_image(self, channel):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as resp:
                data = await resp.json()

        if data['status'] == 'success':
            await channel.send(data['message'])

    async def send_cat_image(self, channel):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as resp:
                data = await resp.json()

        if resp.status == 200 and data:
            await channel.send(data[0]['url'])

    async def send_fox_image(self, channel):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://randomfox.ca/floof/') as resp:
                data = await resp.json()

        if resp.status == 200 and data['image']:
            await channel.send(data['image'])


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = DabstepBot(intents=intents)
client.run(MY_TOKEN)
