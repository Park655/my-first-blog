from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
class EffectCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
class Supplement(models.Model):
    name = models.CharField(max_length=100)
    effect = models.TextField()
    side_effect = models.TextField(blank=True)
    note = models.TextField(blank=True)

    categories = models.ManyToManyField(EffectCategory, blank=True, related_name='supplements')

    def __str__(self):
        return self.name
class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', '남자'),
        ('F', '여자'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}의 프로필"