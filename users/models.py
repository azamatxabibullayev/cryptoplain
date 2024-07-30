from random import random

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta
from django.utils import timezone


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('normal', 'Normal'),
        ('premium', 'Premium'),
    )

    user_type = models.CharField(max_length=7, choices=USER_TYPES, default='normal')
    email = models.EmailField(unique=True, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    id = models.CharField(max_length=12, primary_key=True, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.id = self.generate_unique_id()
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        while True:
            new_id = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            if not CustomUser.objects.filter(id=new_id).exists():
                return new_id

    def __str__(self):
        return f"{self.username} - {self.id}"


class PremiumUser(models.Model):
    PREMIUM_TYPES = (
        ('standart', 'Standart'),
        ('pro', 'Pro'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='premium_user')
    premium_type = models.CharField(max_length=8, choices=PREMIUM_TYPES)
    subscription_start = models.DateTimeField()
    subscription_end = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.subscription_start = timezone.now()
            self.subscription_end = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} - {self.premium_type} - {self.user.id}'
