import pandas as pd
import numpy as np
import pickle
import re
from nltk.stem import PorterStemmer
from flask import Flask, request, render_template


app = Flask(__name__)


f1 = open('cvmodel', 'rb')
cv = pickle.load(f1)

f2 = open('lgmodel', 'rb')
model = pickle.load(f2)

f1.close()
f2.close()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    if request.method == 'POST':

        text = request.form['Review']

        # Preprocessing (same as training)
        text = text.lower()
        text = re.sub(r'[^A-Za-z\s]', '', text)

        ps = PorterStemmer()
        words = text.split()
        words = [ps.stem(word) for word in words]

        text = ' '.join(words)

        data = [text]

        vectorizer = cv.transform(data).toarray()

        prediction = model.predict(vectorizer)
        prediction = prediction[0]

    if prediction == 1:
        return render_template(
            'index.html',
            prediction_text='The review is Positive'
        )

    else:
        return render_template(
            'index.html',
            prediction_text='The review is Negative.'
        )


if __name__ == "__main__":
    app.run(debug=True)