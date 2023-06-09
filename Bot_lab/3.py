import asyncio
import random


async def pests(plant):
    await asyncio.sleep(random.randint(1, 10) / 1000)
    print(f'8 Treatment of {plant[0]} from pests')
    await asyncio.sleep(5 / 1000)
    print(f'8 The {plant[0]} is treated from pests')


async def fertilizers(plant):
    await asyncio.sleep(random.randint(1, 10) / 1000)
    print(f'7 Application of fertilizers for {plant[0]}')
    await asyncio.sleep(3 / 1000)
    print(f'7 Fertilizers for the {plant[0]} have been introduced')


async def sow(plant):
    print(f'0 Beginning of sowing the {plant[0]} plant')
    print(f'1 Soaking of the {plant[0]} started')
    await asyncio.sleep(plant[1] / 1000)
    print(f'2 Soaking of the {plant[0]} is finished')
    pests_task = asyncio.create_task(pests(plant))
    fertilizers_task = asyncio.create_task(fertilizers(plant))
    print(f'3 Shelter of the {plant[0]} is supplied')
    await asyncio.sleep(plant[2] / 1000)
    print(f'4 Shelter of the {plant[0]} is removed')
    print(f'5 The {plant[0]} has been transplanted')
    await asyncio.sleep(plant[3] / 1000)
    print(f'6 The {plant[0]} has taken root')
    await pests_task
    await fertilizers_task
    print(f'9 The seedlings of the {plant[0]} are ready')


async def sowing(*args):
    tasks = []
    for arg in args:
        tasks.append(asyncio.create_task(sow(arg)))

    await asyncio.gather(*tasks)


async def main():
    data = [('carrot', 7, 18, 2), ('cabbage', 2, 6, 10), ('onion', 5, 12, 7)]
    await sowing(*data)


if __name__ == '__main__':
    asyncio.run(main())
