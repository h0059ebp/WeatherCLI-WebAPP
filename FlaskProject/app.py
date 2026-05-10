from flask import Flask, render_template, request
import requests
app = Flask(__name__)

WEATHER_URL = "https://api.brightsky.dev/current_weather"


@app.route('/')
def load_webpage():  #This leads to the webpage
    return render_template('Homepage.html')

@app.route('/weather', methods=["GET", "POST"])
def start():  # This function gets the city name from the Homepage
    if request.method == "GET":
        return render_template('Homepage.html')

    city = request.form.get("city")  # Here you can enter the city name
    if not city:
        return render_template('Homepage.html', error="Bitte geben Sie eine Stadt ein.")

    try:
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json"

        location_response = requests.get(geocoding_url)
        location_response.raise_for_status()
        geocode = location_response.json()

        if not geocode.get('results'):
            raise ValueError("City not found")

        querystring = {
            "lat": geocode['results'][0]['latitude'],
            "lon": geocode['results'][0]['longitude']
        }
        return weather(querystring, city)
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return render_template('Homepage.html', error="Stadt nicht gefunden oder API-Fehler!")

def weather(querystring, city):  # This function gets the weather report from the weather api
    try:
        weather_response = requests.get(WEATHER_URL, params=querystring)
        weather_response.raise_for_status()
        data = weather_response.json()
        return weather_forecast(data, city)
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return render_template('Homepage.html', error="Wetterdaten konnten nicht geladen werden.")

def weather_forecast(data, city): #This function prints the weather report
    return render_template("Homepage.html",
                           city=city,
                           temperature=data['weather']['temperature'],
                           condition=data['weather']['condition'],
                           wind_speed=data['weather']['wind_speed_10']
                           )

# Run Code by: .venv/bin/python app.py



if __name__ == '__main__':
    app.run(debug=True)