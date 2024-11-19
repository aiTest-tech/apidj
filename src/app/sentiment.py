# sentiment_analysis.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax

# Load tokenizer and model from Hugging Face's repository
model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def analyze_sentiment(text):
    # Tokenize and analyze the input text
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    # Define sentiment labels and return the sentiment with scores
    labels = ["Negative", "Neutral", "Positive"]
    sentiment = {label: score for label, score in zip(labels, scores)}
    return sentiment
