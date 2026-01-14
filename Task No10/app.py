from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


UPLOAD_FOLDER = "static/upload"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/listing", methods=["GET", "POST"])
def listing():
    if request.method == "POST":
   
        title = request.form["title"]
        image = request.files["image"]

  
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

  
        return redirect(url_for("market"))

    return render_template("listing.html")


@app.route("/market")
def market():
    items = []  
    return render_template("market.html", items=items)

# Route to handle rent requests
@app.route("/request_rent", methods=["POST"])
def request_rent():
    item_id = request.form.get("item_id")
    # Here you can handle the rent request, e.g., save to database
    print(f"Rent requested for item {item_id}")
    return redirect(url_for("market"))

# Route to handle barter requests
@app.route("/request_barter", methods=["POST"])
def request_barter():
    item_id = request.form.get("item_id")
    # Handle barter request
    print(f"Barter requested for item {item_id}")
    return redirect(url_for("market"))


@app.route("/review/<int:item_id>", methods=["GET", "POST"])
def review(item_id):
    if request.method == "POST":
        rating = request.form["rating"]
        comment = request.form["comment"]  
        return redirect(url_for("market"))

    return render_template("review.html", item_id=item_id)
if __name__ == "__main__":
    app.run(debug=True)
