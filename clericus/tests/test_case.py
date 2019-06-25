import sys
sys.path.append(".")

from .. import Clericus
from ..config import defaultSettings, connectToDB

import unittest
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

import json
import faker
fake = faker.Faker()

from ..schemas import createCollections


class ClericusTestCase(AioHTTPTestCase):
    async def tearDownAsync(self):
        await self.db.client.drop_database(self.db.name)

    async def get_application(self) -> Clericus:
        settings = defaultSettings()
        settings["db"]["name"] = f"test{type(self).__name__}"
        settings = connectToDB(settings)
        await settings["db"].client.drop_database(settings["db"].name)
        self._settings = settings
        self.db = settings["db"]
        await createCollections(self.db)
        return Clericus(self._settings, logging=False)

    async def login(self):
        resp = await self.client.request("GET", "/me/")
        # not logged in
        self.assertEqual(resp.status, 401)
        data = await resp.json()

        user = {
            "username": fake.name(),
            "email": fake.email(),
            "password": fake.password(),
        }
        resp = await self.client.request(
            "POST",
            "/sign-up/",
            json=user,
        )
        resp = await self.client.request("GET", "/me/")
        data = await resp.json()
        return data["currentUser"]

    async def logout(self):
        resp = await self.client.request(
            "GET",
            "/log-out/",
        )
        resp = await self.client.request("GET", "/me/")
        return None