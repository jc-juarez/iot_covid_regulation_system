/*
 * This ESP32 code is created by esp32io.com
 *
 * This ESP32 code is released in the public domain
 *
 * For more detail (instruction and wiring diagram), visit https://esp32io.com/tutorials/esp32-lm35-temperature-sensor
 */

#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "iPhone de Juan Carlos";
const char* password = "hello123";

//Your Domain name with URL path or IP address with path
String serverName = "http://172.20.10.3:5000/backend-api/set-temperature/";

#define ADC_VREF_mV    3300.0 // in millivolt
#define ADC_RESOLUTION 4096.0
#define PIN_LM35       35 // ESP32 pin GIOP36 (ADC0) connected to LM35

void setup() {
  Serial.begin(115200); 

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {


  if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;

      int adcVal = analogRead(PIN_LM35);
      // convert the ADC value to voltage in millivolt
      float milliVolt = adcVal * (ADC_VREF_mV / ADC_RESOLUTION);
      // convert the voltage to the temperature in °C
      int tempC = (int)(milliVolt / 10);

      Serial.print("Temperature: ");
      Serial.print(tempC);   // print the temperature in °C
      Serial.println("°C");
      
      String serverPath = serverName + String(tempC);
      
      // Your Domain name with URL path or IP address with path
      http.begin(serverPath.c_str());
      
      // Send HTTP GET request
      int httpResponseCode = http.GET();

      http.end();

  }
  else{
    Serial.println("No conectado a WiFi");
  }
      
  delay(50);
  
}
