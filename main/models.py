from django.db import models

class HTMLPaster(models.Model):
    theme = models.CharField(max_length=255)
    content = models.TextField()

