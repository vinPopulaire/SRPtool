from django.db import models
from .terms import Term
from .actions import Action
from .enrichments import Enrichment

class Video(models.Model):
    euscreen = models.CharField(unique=True, max_length=50)
    genre = models.CharField(max_length=50)
    topic = models.CharField(max_length=150)
    title = models.CharField(max_length=250)
    geographical_coverage = models.CharField(max_length=150)
    thesaurus_terms = models.CharField(max_length=250)
    summary = models.TextField()
    duration = models.IntegerField(default=0)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    score = models.ManyToManyField(Term, through="VideoContentScore")
    enrichements = models.ManyToManyField(Enrichment, through="VideoEnrichments")

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title


class VideoContentScore(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        verbose_name = "VideoContentScore"
        verbose_name_plural = "VideoContentScores"

    def __str__(self):
        return self.score


class VideoEnrichments(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    enrichment = models.ForeignKey(Enrichment, on_delete=models.CASCADE)
    time = models.IntegerField()
    height = models.DecimalField(max_digits=6, decimal_places=2)
    width = models.DecimalField(max_digits=6, decimal_places=2)
    x_min = models.DecimalField(max_digits=6, decimal_places=2)
    y_min = models.DecimalField(max_digits=6, decimal_places=2)


    class Meta:
        verbose_name = "VideoEnrichments"
        verbose_name_plural = "VideoEnrichmentss"

    def __str__(self):
        return super(VideoEnrichments, self).__str__()

