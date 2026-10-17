from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = ""

    if request.method == "POST":

        city = request.form.get("city", "").strip()

        if city == "":
            error = "Please enter a city name."

        else:

            url = "https://api.openweathermap.org/data/2.5/weather"

            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:

                response = requests.get(url, params=params)

                if response.status_code == 200:

                    data = response.json()

                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature": data["main"]["temp"],
                        "feels_like": data["main"]["feels_like"],
                        "humidity": data["main"]["humidity"],
                        "wind": data["wind"]["speed"],
                        "condition": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"]
                    }

                elif response.status_code == 404:

                    error = "City not found."

                elif response.status_code == 401:

                    error = "Invalid API key."

                else:

                    error = "Weather service error."

            except requests.exceptions.RequestException:

                error = "Please check your internet connection."

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)