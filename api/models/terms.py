from django.db import models

class Term(models.Model):
    term = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Term"
        verbose_name_plural = "Terms"

    def __str__(self):
        return super(Term, self).__str__()

