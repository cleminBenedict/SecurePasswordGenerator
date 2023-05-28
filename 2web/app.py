from flask import Flask, render_template, request
import random
import string
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

def load_dataset():
    # Load the dataset from a file or database
    # In this example, we'll assume that the dataset is stored in a CSV file encoded in UTF-8
    dataset = []
    with open("passwords.csv", "r", encoding="utf-8") as f:
        header = f.readline() # Read and ignore the header row
        for line in f:
            password, strength = line.strip().split(",", 1)
            if strength == "2":  # Only include passwords with strength 2
                dataset.append(password)
    return dataset

def preprocess_dataset(dataset):
    features = []
    labels = []
    for password in dataset:
        # Convert each password into a feature vector
        feature_vector = [int(c in password) for c in string.ascii_letters + string.digits + string.punctuation]
        features.append(feature_vector)
        labels.append(1)  # All passwords in this example have strength 2, so label them as 1
    return features, labels

def train_model(dataset):
    features, labels = preprocess_dataset(dataset)
    model = RandomForestClassifier()
    model.fit(features, labels)
    return model

def generate_password(length):
    dataset = load_dataset()
    model = train_model(dataset)

    password = ""
    while len(password) < length:
        next_char = random.choice(string.ascii_letters + string.digits + string.punctuation)
        password += next_char

    password_chars = list(password)
    random.shuffle(password_chars)
    password = "".join(password_chars)

    return password

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_password", methods=["POST"])
def generate():
    length = int(request.form["password-length"])
    add_special_chars = request.form.get("add-special-chars") == "on"
    add_numbers = request.form.get("add-numbers") == "on"
    challenge = int(request.form["challenge"])
    if challenge != 4:  # Check if the challenge response is correct
        return "Incorrect challenge response. Try again."
    password = generate_password(length)
    if not add_special_chars:
        password = ''.join(char for char in password if char not in string.punctuation)
    if not add_numbers:
        password = ''.join(char for char in password if char not in string.digits)
    password_chars = list(password)
    random.shuffle(password_chars)
    password = "".join(password_chars)
    return render_template("password.html", password=password)

if __name__ == "__main__":
    app.run(debug=True)
