from django.db import models

# Create your models here.


class Video(models.Model):
    video_id = models.TextField()
    video_title = models.TextField()
    published_datetime = models.DateTimeField()
    channel_title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.video_title


class VideoThumbnail(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, related_name="thumbnail")
    thumbnail_type = models.CharField(max_length=20)
    url = models.TextField()

    def __str__(self):
        return self.video.video_title


class APIKeys(models.Model):
    key = models.TextField()
    exhausted = models.BooleanField(default=False)

    def __str__(self):
        return self.key
