from flask import Flask, render_template, request
import requests
app = Flask(__name__)

WEATHER_URL = "https://api.brightsky.dev/current_weather"


@app.route('/')
def load_webpage():  #This leads to the webpage
    return render_template('Homepage.html')

@app.route('/weather', methods=["POST"])
def start(): #This function gets the city name from the Homepage
    city = request.form.get("city")  # Here you can enter the city name
    try:
        geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json"  # This gets the latitude and longitude of the specified city

        location_response = requests.get(geocoding_url)
        geocode = location_response.json()

        querystring = {  # This stores the latitude and longitude to the weather api
            "lat": geocode['results'][0]['latitude'],
            "lon": geocode['results'][0]['longitude']
        }
        return weather(querystring, city)
    except Exception as e:
        print(f"Falsche stadt eingegeben! [{e}]")
        return render_template('Homepage.html', error="Falsche stadt eingegeben!")

def weather(querystring, city): #This function gets the weather report from the weather api
    weather_response = requests.get(WEATHER_URL, params=querystring)
    data = weather_response.json()
    return weather_forecast(data, city)

def weather_forecast(data, city): #This function prints the weather report
    return render_template("Homepage.html",
                           city=city,
                           temperature=data['weather']['temperature'],
                           condition=data['weather']['condition'],
                           wind_speed=data['weather']['wind_speed_10']
                           )


if __name__ == '__main__':
    app.run(debug=True)

