from rest_framework import serializers
from .models import AudioRecord

class AudioRecordSerializer1(serializers.ModelSerializer):
    class Meta:
        model = AudioRecord
        fields = '__all__'


class AudioRecordSerializer(serializers.Serializer):
    file = serializers.FileField()
    lang = serializers.CharField()
