from rest_framework import serializers
from .models import AudioRecord

# class AudioRecordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AudioRecord
#         # fields = ['id', 'audio_base64', 'source', 'edit_source', 'sentiment_analysis', 'rating']
#         # fields = '__all__'
#         fields = ["file", "lang"]


class AudioRecordSerializer(serializers.Serializer):
    file = serializers.FileField()
    lang = serializers.CharField()
    