import json
import random
import nltk
import string
import numpy as np
import pickle
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.layers import LSTM
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences

global responses, lemmatizer, tokenizer, le, model, input_shape
input_shape = 10

# Impor dataset jawaban
def load_response():
    global responses
    responses = {}
    with open('dataset/dataset.json') as file:
        data = json.load(file)
    for intent in data['intents']:
        responses[intent['tag']] = intent['responses']

# Impor model dan unduh file nltk
def preparation():
    load_response()
    global lemmatizer, tokenizer, le, model
    tokenizer = pickle.load(open('model/tokenizers.pkl', 'rb'))
    le = pickle.load(open('model/le.pkl', 'rb'))
    model = keras.models.load_model('model/chatbot_model.h5')
    lemmatizer = WordNetLemmatizer()
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

# Hapus tanda baca
def remove_punctuation(text):
    texts_p = []
    text = [letters.lower() for letters in text if letters not in string.punctuation]
    text = ''.join(text)
    texts_p.append(text)
    return texts_p

# Vectorisasi teks
def vectorization(texts_p):
    vector = tokenizer.texts_to_sequences(texts_p)
    vector = np.array(vector).reshape(-1)
    vector = pad_sequences([vector], maxlen=input_shape)
    return vector

# Klasifikasi pertanyaan pengguna
def predict(vector):
    output = model.predict(vector)
    output = output.argmax()
    response_tag = le.inverse_transform([output])[0]
    return response_tag

# Menghasilkan respons berdasarkan pertanyaan pengguna
def generate_response(text):
    texts_p = remove_punctuation(text)
    vector = vectorization(texts_p)
    response_tag = predict(vector)
    answer = random.choice(responses[response_tag])
    return answer