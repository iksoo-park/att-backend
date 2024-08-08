from att_project import settings

import requests

from naver_oauth.service.naver_oauth_service import NaverOauthService


class NaverOauthServiceImpl(NaverOauthService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.loginUrl = settings.NAVER['LOGIN_URL']
            cls.__instance.clientId = settings.NAVER['CLIENT_ID']
            cls.__instance.redirectUri = settings.NAVER['REDIRECT_URI']
            cls.__instance.clientSecret = settings.NAVER['CLIENT_SECRET']
            cls.__instance.tokenRequestUri = settings.NAVER['TOKEN_REQUEST_URI']
            cls.__instance.userinfoRequestUri = settings.NAVER['USERINFO_REQUEST_URI']

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def naverLoginAddress(self):
        print("naverLoginAddress()")
        return (f"{self.loginUrl}/oauth2.0/authorize?"
                f"client_id={self.clientId}&&response_type=code&redirect_uri={self.redirectUri}"
                )

    def requestAccessToken(self, naverAuthCode):
        print("request Naver AccessToken()")
        accessTokenRequestForm = {
            'grant_type': 'authorization_code',
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'redirect_uri': self.redirectUri,
            'code': naverAuthCode,
        }

        response = requests.post(self.tokenRequestUri, data=accessTokenRequestForm)
        return response.json()