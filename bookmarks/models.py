from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    added_time = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title
