from django.db import models

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

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return username

