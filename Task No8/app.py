from flask import Flask, render_template, request
import requests
from wordcloud import WordCloud
import string
import nltk
from nltk.corpus import stopwords
import os

nltk.download("stopwords")

app = Flask(__name__)


if not os.path.exists("static"):
    os.makedirs("static")

@app.route("/", methods=["GET", "POST"])
def index():
    wordcloud_image = None

    if request.method == "POST":
        artist = request.form["artist"]
        music = request.form["music"]

        
        url = f"https://api.lyrics.ovh/v1/{artist}/{music}"
        response = requests.get(url).json()
        lyrics = response.get("lyrics", "")

        if lyrics:
            
            text = lyrics.lower()
            text = text.translate(str.maketrans("", "", string.punctuation))

            stop_words = set(stopwords.words("english"))
            words = [w for w in text.split() if w not in stop_words]
            clean_text = " ".join(words)

            
            wc = WordCloud(
                width=800,
                height=400,
                background_color="white"
            ).generate(clean_text)

            wc_file = os.path.join("static", "wordcloud.png")
            wc.to_file(wc_file)

            wordcloud_image = "wordcloud.png"

    return render_template("index.html", wordcloud_image=wordcloud_image)

if __name__ == "__main__":
    app.run(debug=True)
