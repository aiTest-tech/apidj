# sentiment_analysis.py
from rest_framework.views import APIView
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from .serializers import AnalyzeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

model_name = "/mnt/c/Users/admin/Downloads/cardiff"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

class AnalyzeSentiment(APIView):
    def post(self, request, *args, **kwargs):
        serializer = AnalyzeSerializer(data = request.data)
        if serializer.is_valid():
            encoded_input = tokenizer(serializer.validated_data["text"], return_tensors='pt')
            output = model(**encoded_input)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            labels = ["Negative", "Neutral", "Positive"]
            sentiment = {label: score for label, score in zip(labels, scores)}
            print("brijesh sentiment is here====", sentiment)
            return Response(sentiment, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        