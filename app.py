from flask import Flask, render_template, request, redirect, session
import pickle

app = Flask(__name__)
app.secret_key = "secret123"

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Login credentials
USERNAME = "Vaishnavi"
PASSWORD = "Vaishu@31"


# -------- LOGIN --------
@app.route('/')
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def do_login():
    username = request.form['username']
    password = request.form['password']

    if username == USERNAME and password == PASSWORD:
        session['user'] = username
        return redirect('/home')
    else:
        return render_template("login.html", error="Invalid Credentials")


# -------- HOME --------
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    return render_template("index.html")


# -------- PREDICT --------
@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect('/')

    message = request.form['message'].lower()

    # 🔥 spam keywords
    spam_words = [
        "win", "free", "claim", "offer", "prize",
        "urgent", "immediately", "act now", "limited",
        "verify", "account", "login", "password", "bank", "security", "alert",
        "earn", "money", "cash", "loan", "investment", "income", "profit",
        "click", "link", "http", "www"
    ]

    # 🔥 disguised spam
    suspicious_phrases = [
        "we tried reaching you",
        "important update",
        "please respond",
        "contact you",
        "important message",
        "account issue",
        "act quickly"
    ]

    score = 0
    found_words = []

    # rule scoring
    for word in spam_words:
        if word in message:
            score += 2
            found_words.append(word)

    for phrase in suspicious_phrases:
        if phrase in message:
            score += 3
            found_words.append(phrase)

    # ML prediction
    data = vectorizer.transform([message])
    prediction = model.predict(data)[0]

    if prediction == 1:
        score += 3

    # final decision
    if score >= 4:
        result = "Spam"
    else:
        result = "Not Spam"

    confidence = min(score * 20, 100)

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        words=found_words
    )


# -------- LOGOUT --------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)