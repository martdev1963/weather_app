from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "ec6f7054139c2b23cc945f009ffb381a"

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
            
            # weather object...
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


if __name__ == '__main__':
    app.run(debug=True)


