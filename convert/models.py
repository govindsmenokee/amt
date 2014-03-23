from django.db import models

class Music(models.Model):
    wavfile = models.FileField(upload_to='wav')
