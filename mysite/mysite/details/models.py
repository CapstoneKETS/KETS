# models.py
from django.db import models


class newsData(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=50)
    reporter = models.CharField(max_length=10, blank=True)
    company = models.CharField(max_length = 10, blank=True)
    created_datetime = models.DateTimeField()
    updated_datetime = models.DateTimeField(auto_now=True)
    article = models.TextField()
    keywords = models.CharField(max_length=50)

    def __str__(self):
        return self.title

# Create your models here.