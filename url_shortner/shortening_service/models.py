from django.db import models

class ShortenedURL(models.Model):
    url         = models.URLField()
    shortCode   = models.CharField(max_length=20, unique=True)
    createdAt   = models.DateTimeField(auto_now_add=True)
    updatedAt   = models.DateTimeField(auto_now=True)
    accessCount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.shortCode} : {self.url}"