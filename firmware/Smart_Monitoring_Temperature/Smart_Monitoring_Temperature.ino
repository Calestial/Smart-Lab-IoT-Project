#include <WiFi.h>
#include <HTTPClient.h>

const int lm35Pin = 34; 
const char* ssid = "Xperia1-V";
const char* password = "Xperia1-V";
const char* serverName = "http://VNotch.pythonanywhere.com/api/data";

void setup() {
  Serial.begin(115200);
  
  // Konfigurasi resolusi ADC ESP32 (12-bit: 0-4095)
  analogReadResolution(12); 
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;

    // --- PROSES BACA SENSOR LM35 ---
    int adcVal = analogRead(lm35Pin);
    
    // Konversi ADC ke Milivolt
    // Rumus: (NilaiADC / ResolusiMax) * TeganganReferensi_mV
    float milliVolt = (adcVal / 4095.0) * 3300; 
    
    // Konversi Milivolt ke Celcius (LM35: 10mV = 1 Derajat C)
    float temperatureC = milliVolt / 10;
    
    // Karena LM35 tidak baca kelembapan, kita kirim 0 atau nilai dummy
    float humidity = 0.0; 

    Serial.print("ADC: "); Serial.print(adcVal);
    Serial.print(" | Temp: "); Serial.print(temperatureC); Serial.println(" C");

    // --- KIRIM DATA KE SERVER ---
    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    // Membuat JSON string
    String httpRequestData = "{\"temperature\":" + String(temperatureC) + ", \"humidity\":" + String(humidity) + "}";
    
    int httpResponseCode = http.POST(httpRequestData);

    Serial.print("Sending Payload: "); Serial.println(httpRequestData);
    
    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server Response: " + response);
    } else {
      Serial.print("Error code: "); Serial.println(httpResponseCode);
    }
    
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
  
  // Delay pengiriman (misal 10 detik)
  delay(10000);
}