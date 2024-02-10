from django.db import models

class kwHistory(models.Model):
    keyword = models.CharField(max_length=10)
    datetime = models.IntegerField()
    rank = models.FloatField()

class kwRank(models.Model):
    keyword = models.CharField(max_length=10)
    rank = models.FloatField()

    def __str__(self):
        return self.title
