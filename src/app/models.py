from django.db import models
from base.models import BaseModel
# Create your models here.


class AudioRecord(models.Model):
    audio_file = models.FileField(upload_to='media/audio_files/', null=True, blank=True)
    source = models.TextField()
    edit_source = models.TextField(null=True, blank=True)
    sentiment_analysis = models.IntegerField(null =True, blank=True)
    
    def __str__(self):
        return f"Audio-recorder-{self.id}"


class RatingRecord(models.Model):
    audio_id = models.ForeignKey(AudioRecord, on_delete=models.CASCADE)
    rating = models.CharField(max_length=100)
    
    def __str__(self):
        return f"rating-{self.rating}, {self.audio_id}"