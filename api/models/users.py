from django.db import models
from .videos import Video
from .actions import Action

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.ForeignKey(
        'Gender',
        on_delete=models.CASCADE
        )
    age = models.ForeignKey(
        'Age',
        on_delete=models.CASCADE
        )
    education = models.ForeignKey(
        'Education',
        on_delete=models.CASCADE
        )
    occupation = models.ForeignKey(
        'Occupation',
        on_delete=models.CASCADE
        )
    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE
        )
    video = models.ManyToManyField(Video, through="VideoWatched")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return username


class VideoWatched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    liked = models.IntegerField()
    time_watched = models.DateTimeField(auto_now=True)
    interactions = models.ManyToManyField(Action, through="VideoInteractions")

    class Meta:
        verbose_name = "VideoWatched"
        verbose_name_plural = "VideoWatcheds"

    def __str__(self):
        return "user %s watched video %s" % (self.user, self.video)


class VideoInteractions(models.Model):
    video_watched = models.ForeignKey(VideoWatched, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    time_action_performed = models.DateTimeField(auto_now=True)
    computed = models.BooleanField(default=0)

    class Meta:
        verbose_name = "VideoInteractions"
        verbose_name_plural = "VideoInteractionss"

    def __str__(self):
        return "user %s made action %s to video %s" % (self.user, self.action, self.video)

