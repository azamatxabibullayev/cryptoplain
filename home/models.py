from django.db import models


class FearGreedIndex(models.Model):
    image = models.ImageField(upload_to='main/home/feargreed/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Fear & Greed Index Image"
