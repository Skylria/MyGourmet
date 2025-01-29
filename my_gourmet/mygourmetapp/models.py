from django.conf import settings
from django.db import models
from django.utils import timezone

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    review = models.ForeignKey

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name