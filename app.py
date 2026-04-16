from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

history = []

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    message = request.form['message']

    data = vectorizer.transform([message])
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0]

    if prediction == 1:
        result = "Spam"
        confidence = round(probability[1]*100, 2)
    else:
        result = "Not Spam"
        confidence = round(probability[0]*100, 2)

    history.append((message, result))

    return render_template("index.html", result=result, confidence=confidence, history=history)

if __name__ == "__main__":
    app.run()
