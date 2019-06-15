from server import Clericus
from config import parseConfig, connectToDB
from schemas import createCollections

import asyncio

settings = connectToDB(parseConfig())

loop = asyncio.get_event_loop()
loop.run_until_complete(createCollections(settings["db"]))

s = Clericus(settings=settings)
s.run_app()
