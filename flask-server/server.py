from flask import Flask, request
import ESP_interactions
app = Flask(__name__)

@app.route('/read_DHT11', methods=['GET'])
def read_DHT11():
    esp_port = request.args.get("esp_port")
    response = ESP_interactions.read_sensor_data(esp_port)
    return response

if  __name__ == '__main__':
    app.run(debug=True)
