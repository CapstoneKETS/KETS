from django.db import models

class newsData(models.Model):
    title = models.CharField(max_length=50)
    reporter = models.CharField(max_length=10)
    company = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    article = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.title

# Create your models here.