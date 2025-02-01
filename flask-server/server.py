from flask import Flask
import weather_info
app = Flask(__name__)

@app.route('/current_weather')
def get_current_weather():
    current, forecast = weather_info.get_weather()
    return {"current_weather": current, "forecast": forecast}

if  __name__ == '__main__':
    app.run(debug=True)
