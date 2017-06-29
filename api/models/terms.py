from django.db import models


class Term(models.Model):
    term = models.CharField(max_length=50)
    long_name = models.CharField(max_length=150, default="TBA")

    class Meta:
        verbose_name = "Term"
        verbose_name_plural = "Terms"

    def __str__(self):
        return self.term

