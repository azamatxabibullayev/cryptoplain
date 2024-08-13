from django.db import models


# Create your models here.


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
