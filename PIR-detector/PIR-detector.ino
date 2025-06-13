#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "ВАШ_WIFI_SSID";
const char* password = "ВАШ_WIFI_ПАРОЛЬ";
const char* serverUrl = "http://192.168.1.100:5000"; 
const char* getEndpoint = "/get_id";                 
const char* motionEndpoint = "/motion";
const int motionSensorPin = D1; 
unsigned long lastDetectionTime = 0;
const long detectionInterval = 30000;


String deviceId = "";

void setup() {
  Serial.begin(115200);
  pinMode(motionSensorPin, INPUT);
  
  connectToWiFi();
  
  deviceId = readMacAddress();
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

void readMacAddress(){
  uint8_t baseMac[6];
  esp_err_t ret = esp_wifi_get_mac(WIFI_IF_STA, baseMac);
  if (ret == ESP_OK) {
    char macAddress[17];
    snprintf(macAddress, sizeof(macAddress), "%02x:%02x:%02x:%02x:%02x:%02x", baseMac[0], baseMac[1], baseMac[2],
                  baseMac[3], baseMac[4], baseMac[5]);

    return macAddress;

  } else {
    Serial.println("Не удалось прочитать MAC адрес");
  }
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
