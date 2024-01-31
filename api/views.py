from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view

# Create your views here.


class GetVideosfromDB(ListAPIView):
    """
        Class based view which fetches all saved videos from db in reverse chronological order
    """
    queryset = models.Video.objects.all().order_by('-published_datetime').distinct()
    serializer_class = serializers.VideoSerializer
    pagination_class = LimitOffsetPagination


@api_view(['POST'])
def save_key(request):
    """
        Saves the api_key to db

        Arguments:
            POST request containing "key" in body
    """
    api_key = request.POST["key"]
    api_key_object = models.APIKeys(key=api_key)
    api_key_object.save()
    return Response("Success")
