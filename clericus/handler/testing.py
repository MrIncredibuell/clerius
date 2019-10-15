from aiohttp.test_utils import AioHTTPTestCase
from dataclasses import dataclass, field

from ..tests.test_case import unittest_run_loop


@dataclass
class TestRequest():
    path: str
    method: str = "GET"
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    body: str = None


@dataclass
class TestResponse():
    statusCode: int
    message: str = ""
    headers: dict = field(default_factory=dict)
    body: str = None


class HttpTest():
    def __init__(
        self,
        request,
        response,
        setUpAsync=None,
        tearDownAsync=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.request = request
        self.response = response
        self.setUpAsync = setUpAsync
        self.tearDownAsync = tearDownAsync

    def generateTestCase(self, appClass, settings):
        expectedRequest = self.request
        expectedResponse = self.response

        class TestCase(AioHTTPTestCase):
            async def get_application(self):
                return appClass(settings, logging=False)

            @unittest_run_loop
            async def testRequest(self):
                # print("in testRequest")
                response = await self.client.request(
                    method=expectedRequest.method,
                    path=expectedRequest.path,
                    data=expectedRequest.body,
                    headers=expectedRequest.headers,
                )
                print(await response.text())
                if expectedResponse.statusCode is not None:
                    self.assertEqual(
                        expectedResponse.statusCode,
                        response.status,
                    )
                return

        return TestCase