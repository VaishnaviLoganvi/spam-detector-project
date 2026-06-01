from flask import Flask, render_template, request, redirect, session
import pickle

app = Flask(__name__)
app.secret_key = "secret123"

# Load Model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

USERNAME = "Vaishnavi"
PASSWORD = "Vaishu@31"


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

    return render_template(
        "login.html",
        error="Invalid Credentials"
    )


@app.route('/home')
def home():

    if 'user' not in session:
        return redirect('/')

    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():

    if 'user' not in session:
        return redirect('/')

    message = request.form['message'].lower()

    phishing_keywords = [
        "verify account",
        "login now",
        "password",
        "security alert",
        "bank account",
        "account blocked",
        "confirm identity"
    ]

    upi_keywords = [
        "upi",
        "kyc",
        "otp",
        "payment failed",
        "wallet blocked"
    ]

    lottery_keywords = [
        "lottery",
        "winner",
        "claim prize",
        "jackpot"
    ]

    job_keywords = [
        "work from home",
        "job offer",
        "registration fee",
        "hiring immediately"
    ]

    financial_keywords = [
        "investment",
        "double money",
        "guaranteed profit",
        "loan approved",
        "earn money fast"
    ]

    spam_keywords = [
        "free",
        "offer",
        "win",
        "prize",
        "urgent"
    ]

    score = 0
    category = "Normal Message"
    found_words = []

    for word in phishing_keywords:
        if word in message:
            category = "Phishing"
            score += 4
            found_words.append(word)

    for word in upi_keywords:
        if word in message:
            category = "UPI Fraud"
            score += 4
            found_words.append(word)

    for word in lottery_keywords:
        if word in message:
            category = "Lottery Scam"
            score += 4
            found_words.append(word)

    for word in job_keywords:
        if word in message:
            category = "Fake Job Offer"
            score += 4
            found_words.append(word)

    for word in financial_keywords:
        if word in message:
            category = "Financial Scam"
            score += 4
            found_words.append(word)

    for word in spam_keywords:
        if word in message:
            score += 2
            found_words.append(word)

    data = vectorizer.transform([message])
    prediction = model.predict(data)[0]

    if prediction == 1:
        score += 3

        if category == "Normal Message":
            category = "Spam"

    if score >= 12:
        threat_level = "Critical"
    elif score >= 8:
        threat_level = "High"
    elif score >= 4:
        threat_level = "Medium"
    else:
        threat_level = "Low"

    confidence = min(score * 10, 100)

    tips = []

    if category == "Phishing":
        tips = [
            "Do not click suspicious links.",
            "Never share passwords.",
            "Verify sender authenticity."
        ]

    elif category == "UPI Fraud":
        tips = [
            "Never share OTP.",
            "Verify payment requests.",
            "Contact your bank if unsure."
        ]

    elif category == "Lottery Scam":
        tips = [
            "Ignore unexpected prizes.",
            "Avoid paying processing fees.",
            "Do not share personal information."
        ]

    elif category == "Fake Job Offer":
        tips = [
            "Do not pay registration fees.",
            "Verify company details.",
            "Check official recruitment portals."
        ]

    elif category == "Financial Scam":
        tips = [
            "Research before investing.",
            "Avoid guaranteed profit schemes.",
            "Consult financial experts."
        ]

    elif category == "Spam":
        tips = [
            "Ignore suspicious messages.",
            "Avoid clicking unknown links.",
            "Block repeated senders."
        ]

    else:
        tips = [
            "Message appears safe.",
            "Continue normal precautions."
        ]

    return render_template(
        "index.html",
        category=category,
        threat_level=threat_level,
        confidence=confidence,
        words=found_words,
        tips=tips
    )


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)