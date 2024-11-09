from django.shortcuts import render
import json
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from .models import AudioRecord
from rest_framework.parsers import MultiPartParser
from .serializers import *
import requests
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
import base64
import os
from rest_framework import status
import json

# Set up URL and headers as constants
ASR_API_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
ASR_API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("BHASHINI_AUTHORIZATION")
}

ASR_API_URL = "https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
ASR_API_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": os.getenv("BHASHINI_AUTHORIZATION")
}

class ProcessAudioView(APIView):
    parser_classes = [MultiPartParser]  # Allows handling multipart form-data (for file uploads)

    @swagger_auto_schema(request_body=AudioRecordSerializer)  
    def post(self, request):
        # Use serializer to validate input data
        serializer = AudioRecordSerializer(data=request.data)
        print("request", request.data)
        print("request file", request.FILES)
        if not serializer.is_valid():
            return Response({"error": "File or language not provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract file and lang from validated data
        file = serializer.validated_data['file']
        lang = serializer.validated_data['lang']
        base64_audio = base64.b64encode(file.read()).decode('utf-8')
        service_id = "ai4bharat/conformer-multilingual-indo_aryan-gpu--t4" if lang != "en" else "ai4bharat/whisper-medium-en--gpu--t4"

        # Prepare the payload without base64 encoding
        payload = {
            "pipelineTasks": [{
                "taskType": "asr",
                "config": {
                    "preProcessors": ["vad"],
                    "language": {"sourceLanguage": lang},
                    "serviceId": service_id,
                    "audioFormat": "wav",
                    "samplingRate": 16000
                }
            }],
            "inputData": {
                "audio": [{"audioContent": base64_audio}]
            }
        }



        # Synchronous API request using requests library
        response = requests.post(ASR_API_URL, headers=ASR_API_HEADERS, data=json.dumps(payload))

        if response.status_code != 200:
            return Response({"error": "Failed to process audio"}, status=response.status_code)

        response_data = response.json()
        source_text = response_data['pipelineResponse'][0]['output'][0]['source']

        # Save audio record to database
        record = AudioRecord.objects.create(source=source_text, audio_file=file)

        return Response({"text": source_text, 'id': record.id}, status=status.HTTP_200_OK)
class SubmitAudioView(APIView):
    def post(self, request):
        data = request.data
        if 'id' not in data or 'text' not in data:
            return JsonResponse({'status': 'fail', 'message': 'Missing id or text'}, status=status.HTTP_400_BAD_REQUEST)

        record_id = data['id']
        text = data['text']

        # Update the audio record
        try:
            record = AudioRecord.objects.get(id=record_id)
            record.edit_source = text
            record.sentiment_analysis = 0
            record.save()

            return JsonResponse({'status': 'success', 'message': 'Record updated successfully'}, status=status.HTTP_200_OK)

        except AudioRecord.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)


class AccRatingView(APIView):
    def post(self, request):
        data = request.data
        if 'id' not in data or 'rating' not in data:
            return JsonResponse({'status': 'fail', 'message': 'Missing id or rating'}, status=status.HTTP_400_BAD_REQUEST)

        record_id = data['id']
        rating = data['rating']

        # Update rating synchronously
        try:
            record = AudioRecord.objects.get(id=record_id)
            record.rating = rating
            record.save()

            return JsonResponse({"status": "success", "message": "Rating updated successfully"}, status=status.HTTP_200_OK)

        except AudioRecord.DoesNotExist:
            return JsonResponse({'status': 'fail', 'message': 'Record not found'}, status=status.HTTP_404_NOT_FOUND)


class FetchAllAudioRecordsView(APIView):
    def get(self, request):
        # Fetch all audio records synchronously
        records = AudioRecord.objects.values('id', 'audio_file', 'source', 'edit_source', 'created_at', 'updated_at')
        return JsonResponse({"total_number": AudioRecord.objects.all().count(),"data":list(records)}, safe=False, status=status.HTTP_200_OK)


class Hello(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"hii":"hello"}, status=status.HTTP_200_OK)
    

# class ShowData(APIView):
#     def get(self, request, *args, **kwargs):
#         audio_records = AudioRecord.objects.all().order_by("id")
#         data = AudioRecord.objects.values()
#         return Response({ "total_number": AudioRecord.objects.all().count(),"response":data}, status=status.HTTP_200_OK)