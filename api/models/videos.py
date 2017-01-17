from django.db import models
from . import User

class Video(models.Model):
    euscreen = models.CharField(unique=True, max_length=50)
    genre = models.CharField(max_length=50)
    topic = models.CharField(max_length=150)
    title = models.CharField(max_length=250)
    geographical_coverage = models.CharField(max_length=150)
    thesaurus_terms = models.CharField(max_length=250)
    summary = models.TextField()
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(User, through="Watched")


    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return title


class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    liked = models.IntegerField()
    time_watched = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Watched"
        verbose_name_plural = "Watcheds"

    def __str__(self):
        return super(Watched, self).__str__()

