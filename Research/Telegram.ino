#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "contoh";  // Sesuaikan dengan nama WiFi (2.4 GHz)
const char* password = "contoh";  // Sesuaikan dengan password WiFi (2.4 GHz)
const char* serverURL = "http://192.168.0.0:5000/temperature";  // Sesuaikan dengan IP komputer yang menjalankan flask


const int TEMP_SENSOR_PIN = 34;
const unsigned long SEND_INTERVAL = 15000; 


unsigned long lastSendTime = 0;

void setup() {
  Serial.begin(115200);
  
  Serial.println("\nMemulai koneksi WiFi...");
  Serial.print("Menghubungkan ke: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("\nBerhasil terhubung ke WiFi!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

float readTemperature() {
  int sensorValue = analogRead(TEMP_SENSOR_PIN);
  float temperature = (sensorValue / 4095.0) * 100.0;
  return temperature;
}

void sendTemperature(float temperature) {
  HTTPClient http;

  String serverPath = String(serverURL) + "?temperature=" + String(temperature, 2);
  Serial.println("Mengirim ke: " + serverPath);
  
  http.begin(serverPath.c_str());
  int httpResponseCode = http.GET();
  
  Serial.print("HTTP Response code: ");
  Serial.println(httpResponseCode);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Response: " + response);
  }
  
  http.end();
}

void loop() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastSendTime >= SEND_INTERVAL) {
    if (WiFi.status() == WL_CONNECTED) {
      float temperature = readTemperature();
      
      Serial.print("Suhu: ");
      Serial.print(temperature);
      Serial.println(" °C");
      
      sendTemperature(temperature);
      lastSendTime = currentTime;
    } else {
      Serial.println("WiFi terputus, mencoba menghubungkan kembali...");
      WiFi.begin(ssid, password);
    }
  }
}
