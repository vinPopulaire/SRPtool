from django.db import models
from .terms import Term

class Enrichment(models.Model):
    enrichment_id = models.CharField(unique=True, max_length=50)
    enrichment_class = models.CharField(max_length=50)
    longName = models.CharField(max_length=250)
    dbpediaURL = models.CharField(max_length=150)
    wikipediaURL = models.CharField(max_length=150)
    description = models.TextField()
    thumbnail = models.CharField(max_length=150)
    time_added = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enrichment"
        verbose_name_plural = "Enrichments"

    def __str__(self):
        return self.enrichment_id


class EnrichmentContentScore(models.Model):
    enrichment = models.ForeignKey(Enrichment, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=6, decimal_places=3)

    class Meta:
        verbose_name = "EnrichmentContentScore"
        verbose_name_plural = "EnrichmentContentScores"

    def __str__(self):
        return self.score
