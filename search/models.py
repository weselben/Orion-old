from django.db import models

# Create your models here.
class Click(models.Model):
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)