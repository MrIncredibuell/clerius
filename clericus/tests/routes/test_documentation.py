import unittest
import asyncio
import json
from aiohttp.test_utils import make_mocked_request

from ...handler import newMethod, Endpoint
from ...parsing.fields import BoolField, StringField

from ..test_case import ClericusTestCase, unittest_run_loop


def async_test(f):
    def wrapper(self):
        return asyncio.run(f(self))

    return wrapper


class TestDocumentation(ClericusTestCase):
    async def get_application(self):
        app = await super().get_application()

        async def process(self, value):
            return {"result": value + " cow"}

        getMethod = newMethod(
            httpMethod="Get",
            description="This is a test handler",
            process=process,
            urlParameters={
                "value": StringField(description="A string to modify", ),
            },
            responseFields={
                "result": StringField(
                    description="The value with \"cow\" appended",
                ),
            },
        )

        class end(Endpoint):
            """
            An example endpoint.
            """
            Get = getMethod

        app.add_endpoint(
            "/stuff/{value}/",
            end,
        )
        return app

    @unittest_run_loop
    async def testDocumentation(self):
        resp = await self.client.request("GET", "/documentation/stuff/moo/")
        self.assertEqual(resp.status, 200)
        data = await resp.json()

        self.assertEqual(data["description"], "An example endpoint.")
        self.assertEqual(
            data["methods"]["get"]["description"],
            "This is a test handler",
        )

        print(data)
