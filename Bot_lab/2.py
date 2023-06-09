import asyncio
import aiohttp


async def fetch_ip(session, url, service_name):
    async with session.get(url) as response:
        data = await response.json()
        ip = data['ip']
        return service_name, ip


async def get_ip():
    services = [
        ('https://api.ipify.org?format=json', 'ipify'),
        ('http://ip-api.com/json', 'ip-api'),
        ('https://checkip.amazonaws.com/', 'Amazon AWS'),
    ]

    async with aiohttp.ClientSession() as session:
        tasks = []
        for url, service_name in services:
            task = asyncio.create_task(fetch_ip(session, url, service_name))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if not isinstance(result, Exception):
                service_name, ip = result
                if ip:
                    print(f"IP адрес: {ip}")
                    print(f"Сервис: {service_name}")
                    break

    await asyncio.sleep(1)  # Добавляем паузу в 1 секунду
    await session.close()  # Закрываем сессию


asyncio.run(get_ip())
