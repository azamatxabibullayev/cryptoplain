from django.db import models

from users.models import CustomUser


class VideoLesson(models.Model):
    title = models.CharField(max_length=255)
    youtube_link = models.URLField()

    class Meta:
        db_table = 'video_lessons'

    def __str__(self):
        return self.title


class Information(models.Model):
    title = models.CharField(max_length=255)
    info_photo = models.ImageField(upload_to='main/info/')
    info_text = models.TextField()

    class Meta:
        db_table = 'Information'

    def __str__(self):
        return self.title

    def short_info(self):
        return self.info_text[:100] + '...'


class Birja(models.Model):
    birja_link = models.URLField()
    birja_photo = models.ImageField(upload_to='main/birja/')
    birja_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'birja'

    def __str__(self):
        return self.birja_name


class Advice(models.Model):
    advice_title = models.CharField(max_length=255)
    advice_text = models.TextField()

    class Meta:
        db_table = 'advice'

    def __str__(self):
        return self.advice_title


class Signal(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    signal_photo = models.ImageField(upload_to='main/signal')

    class Meta:
        db_table = 'signal'

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=255)
    news_text = models.TextField()
    news_photo = models.ImageField(upload_to='main/news/')

    class Meta:
        db_table = 'news'

    def __str__(self):
        return self.title


class Analysis(models.Model):
    ANALYSIS_TYPE_CHOICES = [
        ('normal', 'Normal'),
        ('standart', 'Standart'),
        ('pro', 'Pro'),
    ]

    title = models.CharField(max_length=255)
    analysis_text = models.TextField()
    analysis_photo = models.ImageField(upload_to='main/analyses/')
    analysis_type = models.CharField(max_length=20, choices=ANALYSIS_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analysis'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Note(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'note'

    def __str__(self):
        return self.title
