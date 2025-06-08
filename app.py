from flask import Flask, render_template, request
import requests

# instantiate a Flask object by calling the Flask constructor...
app = Flask(__name__)

# should hide the api key inside an environment variable to avoid 'Slacker' exploits...
API_KEY = "80189448ac9b9dfdace19c6e4e55b826"

"""
--------------------------------------------------------------------------------------------
                                    **FUNCTION ROUTES**

index() - sends request to API
weather_by_location() - sends request to API with user coords data
to get user's local weather forcast...

--------------------------------------------------------------------------------------------
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = {}
    if request.method == 'POST':
        city = request.form['city']
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # code refactor to include farenheit and celsius
            temp_c = data['main']['temp'] # celsius is the default...
            temp_f = round((temp_c * 9/5) + 32, 2) # convert to farenheit...
            
            # weather dict...(like a js object)
            weather = {
                'city': city,
                #'temperature': data['main']['temp'], <------ celsius is the default...
                # two lines of code below replacing above LOC...
                'temp_c': round(temp_c, 2),
                'temp_f': temp_f,
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon']
            }
        else:
            weather = {'error': 'City not found'}
    return render_template('index.html', weather=weather)        


# ----Code Refactor START----
# This function route is a new and improved index() function....its pulling the same index.html template file below...

@app.route('/weather')
def weather_by_location():
    lat = request .args.get('lat')
    lon = request .args.get('lon')
    print("→ Got lat/lon from request:", lat, lon)
    weather = {} # weather dict...
    
    # exploiting and/or using the other parameters the API offers; -----> lat={lat}&lon={lon}&appid={API_KEY}&units=metric...
    if lat and lon:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json() # convert to json object and parse the data below...
            print("→ Weather API response:", data)
            if 'main' in data and 'weather' in data:
                temp_c = data['main']['temp']
                temp_f = round((temp_c * 9/5) + 32, 2) #  convert to farenheit and round off to 2 decimal places...

                # fill the weather dict declared above with key : value pairs...
                weather = {
                    'city' : data['name'],
                    'temp_c' : round(temp_c, 2),  
                    'temp_f' : temp_f, 
                    'description' : data['weather'][0]['description'], 
                    'icon' : data['weather'][0]['icon'] 
                }
            else:
                print("⚠️ Weather API returned unexpected format.")
                weather = {'error': 'Unable to retrieve weather data.'}
        else:
            print("❌ API request failed:", response.status_code)
            weather = {'error': 'Location not found'}          
    else:
            print("⚠️ No lat/lon provided in request.")
            weather = {'error': 'Missing coordinates'}
    return render_template('index.html', weather=weather) # including the weather dict, passing it as a template keyword argument...            







# ----Code Refactor END----

# this code auto-restarts flask server after any new edits of code...
if __name__ == '__main__':
    app.run(debug=True)


