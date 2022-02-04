# Create your views here.
import os

import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from api.helpers import custom_permission
from api.models import FavoriteCharacter, FavoriteQuote
from api.serializers import FavoriteCharacterSerializer, FavoriteQuoteSerializer

ACCESS_TOKEN = os.environ.get("THE_ONE_ACCESS_TOKEN")


def ping(request):
    data = {"ping": "pong!"}
    return JsonResponse(data)


class CharacterList(APIView):
    """
    Get all LOR characters.
    """
    name = 'Character-list'

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        """Method to make the get request to THE ONE API.
         @cache_page: helps to cache the results for 2 hours.
         """
        headers: dict = {"Authorization": "Bearer " + ACCESS_TOKEN}
        endpoint: str = "https://the-one-api.dev/v2/character"
        try:
            resp = requests.get(endpoint, headers=headers)
            # use drf paginator for 100 results per page
            paginator = PageNumberPagination()
            paginator.page_size = 100
            if resp.status_code == 200:
                data = paginator.paginate_queryset(resp.json()['docs'], request)
                return paginator.get_paginated_response(data)
            elif resp.status_code == 429:
                return {'message': "Rate limited! Please wait for 15 minutes')"}

            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except requests.ConnectionError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)})


class CharacterQuoteDetail(APIView):
    """
    Get all quotes belonging a single character.
    """
    name = 'quote-list'

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, pk, format=None):
        headers: dict = {"Authorization": "Bearer " + ACCESS_TOKEN}
        endpoint: str = f"https://the-one-api.dev/v2/character/{pk}/quote"
        try:
            resp = requests.get(endpoint, headers=headers)
            paginator = PageNumberPagination()
            paginator.page_size = 100
            if resp.status_code == 200:
                data = paginator.paginate_queryset(resp.json()['docs'], request)
                return paginator.get_paginated_response(data)
            elif resp.status_code == 429:
                return Response({'message': "Rate limited! Please wait for 15 minutes"},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        except requests.ConnectionError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteCharacterView(APIView):
    """
    Class to add a character as a favorite.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,
                          custom_permission.IsCurrentUserOwnerOrReadOnly)

    def post(self, request, *args, **kwargs):
        # check if the id in url equals to what the user entered
        try:
            if request.data['character'] != self.kwargs['pk']:
                return Response({"error_message": "The character id you entered doesn't match the URL."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = FavoriteCharacterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteQuoteView(APIView):
    """
        Class to add a quote as a favorite.
        """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,
                          custom_permission.IsCurrentUserOwnerOrReadOnly)

    def post(self, request, *args, **kwargs):
        # check if the id in url equals to what the user entered
        try:
            if request.data['quote'] != self.kwargs['id']:
                return Response({"error_message": "The quote id you entered doesn't match the URL."},
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = FavoriteQuoteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteList(APIView):
    """
    Class to retrieve all favorited items.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,
                          custom_permission.IsCurrentUserOwnerOrReadOnly)

    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request, format=None):
        favorite_characters = FavoriteCharacter.objects.filter(user=self.request.user)  # no database activity
        favorite_quotes = FavoriteQuote.objects.filter(user=self.request.user)

        if not favorite_characters.exists():
            return Response({"error_message": "No favorite characters items yet"}, status=status.HTTP_404_NOT_FOUND)
        char_id_list = [char.character for char in favorite_characters]  # query the db and store results in cache

        if not favorite_quotes.exists():
            return Response({"error_message": "No favorite_characters items yet"}, status=status.HTTP_404_NOT_FOUND)
        quote_id_list = [quo.quote for quo in favorite_quotes]  # query the db and store results in cache

        headers: dict = {"Authorization": "Bearer " + ACCESS_TOKEN}
        char_list = []
        for char in char_id_list:
            endpoint: str = f"https://the-one-api.dev/v2/character/{char}"
            try:
                resp = requests.get(endpoint, headers=headers)
                if resp.status_code == 500:
                    return Response({"error_message": "You have entered one or more incorrect id."},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif resp.status_code == 429:
                    return Response({'message': "Rate limited! Please wait for 15 minutes'"})
                for i in resp.json()['docs']:
                    char_list.append(i)
            except requests.ConnectionError as e:
                return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        for qid in quote_id_list:
            endpoint: str = f"https://the-one-api.dev/v2/quote/{qid}"
            try:
                resp = requests.get(endpoint, headers=headers)
                if resp.status_code == 500:
                    return Response({"error_message": "You have entered one or more incorrect id."},
                                    status=status.HTTP_400_BAD_REQUEST)
                elif resp.status_code == 429:
                    return Response({'message': "Rate limited! Please wait for 15 minutes'"})
                for i in resp.json()['docs']:
                    char_list.append(i)
            except requests.ConnectionError as e:
                return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error_message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if resp.status_code == 200:
            return Response(char_list, status=status.HTTP_200_OK)

        return Response({"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class ApiRoot(GenericAPIView):
    """Navigate through the available endpoints"""
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'characters': reverse(CharacterList.name, request=request),
        })
