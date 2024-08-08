from urllib import parse

from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from naver_oauth.serializer.naver_oauth_access_token_serializer import NaverOauthAccessTokenSerializer
from naver_oauth.serializer.naver_oauth_url_serializer import NaverOauthUrlSerializer
from naver_oauth.service.naver_oauth_service_impl import NaverOauthServiceImpl


class NaverOauthView(viewsets.ViewSet):
    naverOauthService = NaverOauthServiceImpl.getInstance()

    def naverOauthURI(self, request):
        url = self.naverOauthService.naverLoginAddress()
        print(f"url:", url)
        serializer = NaverOauthUrlSerializer(data={ 'url': url })
        serializer.is_valid(raise_exception=True)
        print(f"validated_data: {serializer.validated_data}")
        return Response(serializer.validated_data)

    def naverAccessTokenURI(self, request):
        serializer = NaverOauthAccessTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code']
        # auth_dict = serializer.validated_data
        # auth_code = parse.unquote(auth_dict['code'])
        # print(f"auth_code: {auth_code}")

        try:
            accessToken = self.naverOauthService.requestAccessToken(code)
            print(f"accessToken: {accessToken}")
            return JsonResponse({'accessToken': accessToken})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)