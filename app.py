from flask import Flask, render_template, request, redirect, session
import pickle

app = Flask(__name__)
app.secret_key = "secret123"

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

USERNAME = "admin"
PASSWORD = "1234"


# 🔹 LOGIN PAGE
@app.route('/')
def login():
    return render_template("login.html")


# 🔹 LOGIN CHECK
@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    if username == USERNAME and password == PASSWORD:
        session['user'] = username
        return redirect('/home')
    else:
        return render_template("login.html", error="Invalid Credentials")


# 🔹 HOME PAGE
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template("index.html")


# 🔹 PREDICT
@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

    message = request.form['message']

    data = vectorizer.transform([message])
    prediction = model.predict(data)[0]

    result = "Spam" if prediction == 1 else "Not Spam"

    return render_template("index.html", result=result)


# 🔹 LOGOUT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run()
