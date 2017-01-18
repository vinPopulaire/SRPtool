from django.db import models

class Action(models.Model):
    action = models.CharField(max_length=50)
    importance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"

    def __str__(self):
        return self.action

