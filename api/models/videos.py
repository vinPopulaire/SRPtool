from django.db import models
from .users import User
from .terms import Term
from .actions import Action

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
    scores = models.ManyToManyField(Term, through="VideoContentScore")

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title


class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    liked = models.IntegerField()
    time_watched = models.DateTimeField(auto_now=True)
    interactions = models.ManyToManyField(Action, through="VideoInteractions")

    class Meta:
        verbose_name = "Watched"
        verbose_name_plural = "Watcheds"

    def __str__(self):
        return "user %s watched video %s" % (self.user, self.video)


class VideoContentScore(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        verbose_name = "VideoContentScore"
        verbose_name_plural = "VideoContentScores"

    def __str__(self):
        return self.score


class VideoInteractions(models.Model):
    watched = models.ForeignKey(Watched, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    time_action_performed = models.DateTimeField(auto_now=True)
    computed = models.BooleanField(default=0)

    class Meta:
        verbose_name = "VideoInteractions"
        verbose_name_plural = "VideoInteractionss"

    def __str__(self):
        return super(VideoInteractions, self).__str__()

