from django.db import models


class Urls(models.Model):
    id_link = models.IntegerField(primary_key=True)
    short_link = models.SlugField(max_length=6)
    original_url = models.URLField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_url
