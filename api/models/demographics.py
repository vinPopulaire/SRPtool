from django.db import models

# Create your models here.
class Gender(models.Model):
    gender = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Genders"

    def __str__(self):
        return self.gender

class Age(models.Model):
    age = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Age"
        verbose_name_plural = "Ages"

    def __str__(self):
        return self.age

class Country(models.Model):
    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countrys"

    def __str__(self):
        return self.country

class Occupation(models.Model):
    occupation = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Occupation"
        verbose_name_plural = "Occupations"

    def __str__(self):
        return self.occupation

class Education(models.Model):
    education = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Educations"

    def __str__(self):
        return self.education

