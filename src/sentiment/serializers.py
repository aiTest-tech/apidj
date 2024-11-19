from rest_framework import serializers


class AnalyzeSerializer(serializers.Serializer):
    text = serializers.CharField(required = True)