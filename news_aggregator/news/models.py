# news/models.py
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

class SharedArticle(models.Model):
    email_1 = models.EmailField()
    name_1 = models.CharField(max_length=100)
    email_2 = models.EmailField()
    article_info = models.JSONField()

    class Meta:
        unique_together = ('email_1', 'email_2', 'article_info')
