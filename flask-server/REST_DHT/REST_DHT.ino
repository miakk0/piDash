#include <ESP8266WiFi.h>
#include <DHT.h>
#include <ESP8266WebServer.h>

#include "WIFI_CONFIG.h"


#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Create a web server instance on port 80
ESP8266WebServer server(80);

void setup() {
  Serial.begin(9600);
  delay(10);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD); //WiFi ssid and password defined in WIFI_CONFIG.h
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to Wi-Fi");

  // Print the IP address to Serial Monitor
  Serial.print("ESP8266 IP Address: ");
  Serial.println(WiFi.localIP());  // This gets the ESP8266's IP address

  // Start the server
  server.begin();
  
  // Define REST API endpoints
  server.on("/DHT11", HTTP_GET, []() {
    // Read temperature and humidity from DHT11 sensor
    delay(500);
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    if (isnan(temperature) || isnan(humidity)) {
      server.send(500, "application/json", "{\"error\":\"Failed to read sensor values\"}");
      return;
    }
    String response = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";
    server.send(200, "application/json", response);
    Serial.println(response);
  });
}

void loop() {
  delay(750);
  server.handleClient();  // Handle incoming client requests
  
}