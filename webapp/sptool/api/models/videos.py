from django.db import models
from .terms import Term
from .enrichments import Enrichment


class Video(models.Model):
    euscreen = models.CharField(unique=True, max_length=50)
    genre = models.CharField(max_length=50, default='unknown')
    topic = models.CharField(max_length=150, default='unknown')
    title = models.CharField(max_length=250)
    geographical_coverage = models.CharField(max_length=150, default='unknown')
    thesaurus_terms = models.CharField(max_length=250, default='unknown')
    summary = models.TextField()
    source = models.CharField(max_length=150, default='unknown')
    path = models.CharField(max_length=150, default='unknown')
    tags = models.TextField(default='')
    annotations = models.TextField(default='')
    duration = models.IntegerField(default=0)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    score = models.ManyToManyField(Term, through="VideoContentScore")
    enrichments = models.ManyToManyField(Enrichment, through="VideoEnrichments")

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
        return "Video score: %s" % self.score


class VideoEnrichments(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    project_id = models.CharField(max_length=150,default='')
    enrichment = models.ForeignKey(Enrichment, on_delete=models.CASCADE)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=-1)
    x = models.DecimalField(max_digits=6, decimal_places=2)
    y = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        verbose_name = "VideoEnrichments"
        verbose_name_plural = "VideosEnrichments"

    def __str__(self):
        return super(VideoEnrichments, self).__str__()

