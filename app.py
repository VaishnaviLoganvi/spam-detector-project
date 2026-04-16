from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

history = []
spam_count = 0
not_spam_count = 0

@app.route('/')
def home():
    return render_template("index.html", spam=spam_count, notspam=not_spam_count)

@app.route('/predict', methods=['POST'])
def predict():
    global spam_count, not_spam_count

    message = request.form['message']

    data = vectorizer.transform([message])
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0]

    if prediction == 1:
        result = "Spam"
        confidence = round(probability[1]*100, 2)
        spam_count += 1
    else:
        result = "Not Spam"
        confidence = round(probability[0]*100, 2)
        not_spam_count += 1

    history.append((message, result))

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        history=history,
        spam=spam_count,
        notspam=not_spam_count
    )

if __name__ == "__main__":
    app.run()
