from pathlib import Path
import os
import pickle

import numpy as np
from flask import Flask, render_template, request


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model.pkl"

app = Flask(__name__)


def load_model():
    if MODEL_PATH.exists():
        with MODEL_PATH.open("rb") as file:
            return pickle.load(file)
    return None


model = load_model()


def fallback_crop(values):
    n, p, k, temperature, humidity, ph, rainfall = values

    if rainfall >= 180 and humidity >= 75:
        return "rice"
    if k >= 120 and humidity >= 70:
        return "banana"
    if rainfall >= 140 and n >= 60:
        return "jute"
    if temperature >= 30 and rainfall < 90:
        return "cotton"
    if ph < 6.0 and humidity >= 70:
        return "orange"
    if temperature < 20 and p >= 50:
        return "chickpea"
    if n >= 80 and rainfall >= 90:
        return "maize"
    if humidity < 45 and rainfall < 80:
        return "mothbeans"
    return "coffee"


def predict_crop(values):
    if model is not None:
        prediction = model.predict(np.array(values).reshape(1, -1))
        return str(prediction[0])
    return fallback_crop(values)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/findyourcrop")
def findyourcrop():
    return render_template("findyourcrop.html")


@app.route("/predict", methods=["POST"])
def predict():
    fields = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    try:
        values = [float(request.form[field]) for field in fields]
        crop = predict_crop(values)
        return render_template("result.html", crop=crop, values=dict(zip(fields, values)))
    except (ValueError, KeyError):
        return render_template(
            "findyourcrop.html",
            error="Please enter valid numeric values for every field.",
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
