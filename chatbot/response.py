import pickle
import re
import nltk
import pandas as pd
from django.views.decorators.csrf import csrf_exempt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from textblob.sentiments import *


def dr_response(req):
    # Pre-processing
    req = re.sub(r'[^A-Za-z0-9\\s]', ' ', req.lower())

    # Encode the text to get embeddings
    model = SentenceTransformer('sentence-transformers/multi-qa-mpnet-base-cos-v1')
    req_embeddings = model.encode(req).reshape(1, -1)

    # Compute similarity

    qn_embeddings = pickle.load(open(r'model/stsb-embedding.pkl', 'rb'))
    cosine_sim = cosine_similarity(qn_embeddings, req_embeddings)
    cosine_sim = [(idx, item) for idx, item in enumerate(cosine_sim)]
    sim_scores = sorted(cosine_sim, key=lambda x: x[1], reverse=True)

    # Return response of the top most similar question
    top_score = sim_scores[0]
    qn_indice = top_score[0]

    df = pd.read_csv(r'model/cleaned_df.csv')

    if top_score[1][0] > .70:
        return df['Answers'].iloc[qn_indice]

    return "Could you please elaborate your situation more? I don't really understand."


greetings = ['hi', 'hey', 'hello', 'heyy', 'hi', 'hey', 'good evening', 'good morning', 'good afternoon', 'good',
             'fine', 'okay', 'great', 'could be better', 'not so great', 'very well thanks', 'fine and you',
             "i'm doing well", 'pleasure to meet you', 'hi whatsup']
happy_emotions = ['i feel good', 'life is good', 'life is great', "i've had a wonderful day", "i'm doing good"]
goodbyes = ['thank you', 'thank you', 'yes bye', 'bye', 'thanks and bye', 'ok thanks bye', 'goodbye', 'see ya later',
            'alright thanks bye', "that's all bye", 'nice talking with you', 'i’ve gotta go', 'i’m off', 'good night',
            'see ya', 'see ya later', 'catch ya later', 'adios', 'talk to you later', 'bye bye', 'all right then',
            'thanks', 'thank you', 'thx', 'thx bye', 'thnks', 'thank u for ur help', 'many thanks', 'you saved my day',
            'thanks a bunch', "i can't thank you enough", "you're great", 'thanks a ton', 'grateful for your help',
            'i owe you one', 'thanks a million', 'really appreciate your help', 'no', 'no goodbye']


def get_bot_response(question):
    cleanText = re.sub(r'[^A-Za-z0-9\\s]', ' ', question.lower())
    # check sentiment
    blob = TextBlob(question, analyzer=PatternAnalyzer())
    polarity = blob.sentiment.polarity

    if cleanText in greetings:
        return "Hello! How may I help you today?"
    elif polarity > 0.7:
        return "That's great! Do you still have any questions for me?"
    elif cleanText in happy_emotions:
        return "That's great! Do you still have any questions for me?"
    elif cleanText in goodbyes:
        return "Hope I was able to help you today! Take care, bye!"
    elif polarity < -0.4:
        return "Please be polite we are sorry for any issues caused to you."
    topic = dr_response(question)
    return topic