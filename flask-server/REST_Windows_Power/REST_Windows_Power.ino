#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "WIFI_CONFIG.h"

// Pin for transistor control (e.g., D4)
#define TRANSISTOR_PIN 2

// Create a web server instance on port 80
ESP8266WebServer server(80);

void setup() {
  Serial.begin(9600);
  delay(10);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);  //WiFi ssid and password defined in WIFI_CONFIG.h
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to Wi-Fi");

  // Print the IP address to Serial Monitor
  Serial.print("ESP8266 IP Address: ");
  Serial.println(WiFi.localIP());  // This gets the ESP8266's IP address

  // Initialize the transistor pin as an output and set it LOW initially
  pinMode(TRANSISTOR_PIN, OUTPUT);
  digitalWrite(TRANSISTOR_PIN, LOW);  // Make sure the transistor is LOW initially
  
  // Start the server
  server.begin();
  
  // Define the "button" endpoint that triggers the transistor for 0.5 seconds
  server.on("/button", HTTP_GET, []() {
    digitalWrite(TRANSISTOR_PIN, HIGH);
    delay(500);
    digitalWrite(TRANSISTOR_PIN, LOW);
    server.send(200, "application/json", "{\"status\":\"Transistor Pulsed\"}");
  });
}

void loop() {
  server.handleClient();  // Handle incoming client requests
}