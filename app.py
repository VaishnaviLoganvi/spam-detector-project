from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Home page
@app.route('/')
def home():
    return render_template("index.html")

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    text = request.form['email']

    vec = vectorizer.transform([text])
    result = model.predict(vec)

    if result[0] == 1:
        prediction = "Spam"
    else:
        prediction = "Not Spam"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)