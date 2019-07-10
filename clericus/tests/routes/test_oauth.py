import sys
sys.path.append(".")

import unittest
from aiohttp.test_utils import unittest_run_loop
from ..test_case import ClericusTestCase

from ...routes.authentication import generateOAuthEndpoint

import faker
fake = faker.Faker()


class OAuthTestCase(ClericusTestCase):
    async def get_application(self):
        app = await super().get_application()
        app.addEndpoint(
            "/oauth/test/",
            generateOAuthEndpoint(
                clientID="0oam3clat1k5dMe4m0h7",
                clientSecret="AwDqqDhjvYNCF3w6uePWPkmsDNlpvYybDzaOzqrY",
                redirectUri=
                "https://www.oauth.com/playground/authorization-code.html",
                responseType="code",
                grantType="authorization_code",
                scope="",
                authorizationUri=
                "https://dev-396343.oktapreview.com/oauth2/default/v1/authorize",
                tokenUri=
                "https://dev-396343.oktapreview.com/oauth2/default/v1/token",
            )
        )
        return app

    @unittest_run_loop
    async def testOauth(self):

        print(self.app)

        resp = await self.client.request("GET", "/oauth/test/")
        # self.assertEqual(resp.status, 401)
        # data = await resp.json()
        print(resp)
        # print(data)
        # user = {
        #     "username": fake.user_name(),
        #     "email": fake.email(),
        #     "password": fake.password(),
        # }

        # resp = await self.client.request(
        #     "POST",
        #     "/sign-up/",
        #     json=user,
        # )
        # self.assertEqual(resp.status, 200)

        # resp = await self.client.request("GET", "/me/")
        # self.assertEqual(resp.status, 200)
        # data = await resp.json()
        # self.assertEqual(data["currentUser"]["username"], user["username"])