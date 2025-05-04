from django.db import models

# Create your models here.
class Country(models.Model):
    name_common = models.CharField(max_length=200)
    name_official = models.CharField(max_length=200)
    cca2 = models.CharField(max_length=2, unique=True, db_index=True) 
    capital = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True)
    subregion = models.CharField(max_length=100, blank=True, null=True)
    languages = models.JSONField(blank=True, null=True) 
    population = models.BigIntegerField(default=0)
    timezones = models.JSONField(blank=True, null=True) 
    flags_svg = models.URLField(max_length=500, blank=True, null=True)
    flags_png = models.URLField(max_length=500, blank=True, null=True) 
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name_common'] 

    def __str__(self):
        return self.name_common