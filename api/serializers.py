from rest_framework import serializers
from . import models


class VideoSerializer(serializers.ModelSerializer):
    thumbnails = serializers.SerializerMethodField()

    def get_thumbnails(self, obj):
        return [
            VideoThumbNailSerializer(thumbnail).data
            for thumbnail in models.VideoThumbnail.objects.filter(video=obj)]

    class Meta:
        model = models.Video
        fields = '__all__'


class VideoThumbNailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VideoThumbnail
        fields = '__all__'
