import asyncio


def read_from_file(file_name):
    """Reads text from file"""

    with open(file_name, 'r') as text:
        text = text.read()
    return text


async def sleep(tics=1):
    for tic in range(tics):
        await asyncio.sleep(0)
