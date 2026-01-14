from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "12139c8081420d47a84b830b1be0858b"

def gc(city):
    try:
        url = f"https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={API_KEY}"
        response = requests.get(url).json()

       
        if not isinstance(response, list) or len(response) == 0:
            return None, None

        lat = response[0].get("lat")
        lon = response[0].get("lon")

        return lat, lon

    except Exception:
        return None, None

def classify(value, pollutant):
    limits = {
        "SO2": [(0,20),(20,80),(80,250),(250,350),(350,99999)],
        "NO2": [(0,40),(40,70),(70,150),(150,200),(200,99999)],
        "PM10": [(0,20),(20,50),(50,100),(100,200),(200,99999)],
        "PM25": [(0,10),(10,25),(25,50),(50,75),(75,99999)],
        "O3": [(0,60),(60,100),(100,140),(140,180),(180,99999)],
        "CO": [(0,4400),(4400,9400),(9400,12400),(12400,15400),(15400,99999)]
    }

    names = ["Good", "Fair", "Moderate", "Poor", "Very Poor"]

    for i, (low, high) in enumerate(limits[pollutant]):
        if low <= value < high:
            return names[i]


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        lat, lon = gc(city)


        if lat is None or lon is None:
            error = "City not found. Please enter a valid city name."
            return render_template("index.html", error=error)

        air_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        air = requests.get(air_url).json()

        components = air["list"][0]["components"]

        result = {
        "SO2": classify(components["so2"], "SO2"),
        "NO2": classify(components["no2"], "NO2"),
        "PM10": classify(components["pm10"], "PM10"),
        "PM25": classify(components["pm2_5"], "PM25"),  
        "O3": classify(components["o3"], "O3"),
        "CO": classify(components["co"], "CO")
        }


    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)
