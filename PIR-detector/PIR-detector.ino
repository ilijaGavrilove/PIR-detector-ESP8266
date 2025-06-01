#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "ВАШ_WIFI_SSID";
const char* password = "ВАШ_WIFI_ПАРОЛЬ";
const char* serverUrl = "http://192.168.1.100:5000"; 
const char* getEndpoint = "/get_id";                 
const char* motionEndpoint = "/motion";              
const char* telegramToken = "ВАШ_TELEGRAM_BOT_TOKEN";
const char* chatId = "ВАШ_CHAT_ID";
const int motionSensorPin = D1; 
unsigned long lastDetectionTime = 0;
const long detectionInterval = 30000; 


String deviceId = "";

void setup() {
  Serial.begin(115200);
  pinMode(motionSensorPin, INPUT);
  
  connectToWiFi();
  
  deviceId = getDeviceId();
  if(deviceId != "") {
    Serial.println("ID устройства: " + deviceId);
  }
}

void loop() {
  bool motionDetected = digitalRead(motionSensorPin) == HIGH;
  
  if (motionDetected) {
    if (millis() - lastDetectionTime > detectionInterval) {
      Serial.println("Движение обнаружено! Отправка данных...");
      
      DynamicJsonDocument doc(256);
      doc["device_id"] = deviceId;
      
      String jsonData;
      serializeJson(doc, jsonData);
      
      sendMotionData(jsonData);
      
      lastDetectionTime = millis();
    }
  }
  
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }
  
  delay(500);
}

void connectToWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Подключение к Wi-Fi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\nПодключено! IP адрес: " + WiFi.localIP());
}

String getDeviceId() {
  if (WiFi.status() != WL_CONNECTED) return "";

  HTTPClient http;
  http.begin(serverUrl + String(getEndpoint));
  int httpCode = http.GET();
  
  String payload = "";
  
  if (httpCode == HTTP_CODE_OK) {
    payload = http.getString();
    
    // Парсим JSON ответ
    DynamicJsonDocument doc(256);
    deserializeJson(doc, payload);
    String id = doc["id"].as<String>();
    
    http.end();
    return id;
  } else {
    Serial.printf("Ошибка получения ID: %s\n", http.errorToString(httpCode).c_str());
    http.end();
    return "";
  }
}

void sendMotionData(String jsonData) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(serverUrl + String(motionEndpoint));
  http.addHeader("Content-Type", "application/json");
  
  int httpCode = http.POST(jsonData);
  
  if (httpCode == HTTP_CODE_OK) {
    Serial.println("Данные движения отправлены");
  } else {
    Serial.printf("Ошибка отправки данных: %d\n", httpCode);
    Serial.println("Ответ сервера: " + http.getString());
  }
  
  http.end();
}
