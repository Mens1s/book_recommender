#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>

#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 22 // Reset pin
#define SS_PIN  5  // Slave select pin

MFRC522 rfid(SS_PIN, RST_PIN);

// Wi-Fi ağ bilgileri
const char* ssid = "Ahmet iPhone’u";  // Wi-Fi adınız
const char* password = "ahmet12345";  // Wi-Fi şifreniz

void sendGetRequest(String rfid) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // API'ye GET isteği gönder (RFID parametresi ekleniyor)
    String url = "https://book-recommender-6yyu.onrender.com/api/recommend/?id=" + rfid;
    http.begin(url.c_str());  // GET isteği yapılacak URL

    Serial.println("RFID Book Name POST'ed Via API Call");
    Serial.println("Getting Response from server...");
    int httpCode = http.GET();  // GET isteğini gönder

    if (httpCode > 0) {
      Serial.println("GET request sent successfully");
      String payload = http.getString(); 
      Serial.println("Received response: \n" + payload);
    } else {
      Serial.println("GET request failed");
    }
    http.end();  // HTTP bağlantısını kapat
  } else {
    Serial.println("WiFi not connected");
  }
}

void setup() {
  // Seri haberleşmeyi başlat
  Serial.begin(115200);
  
  // WiFi'ye bağlan
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected");
  
  // RFID modülünü başlat
  SPI.begin();  // SPI başlat
  rfid.PCD_Init();  // MFRC522 başlat
  Serial.println("RFID Ready to Read!");  
}

void loop() {
    //Serial.println("Checking card...");

    if (!rfid.PICC_IsNewCardPresent() || !rfid.PICC_ReadCardSerial()) {
        return;
    }
    Serial.println("RFID Card Readed...!");

    // Convert RFID UID to a string
    String rfidTag = "";
    for (byte i = 0; i < rfid.uid.size; i++) {
        rfidTag += String(rfid.uid.uidByte[i], HEX);  // Convert each byte to hexadecimal
    }

    // Pass the RFID string to the GET request function
    sendGetRequest(rfidTag);

    Serial.println("RFID Ready to Read!");
    
    rfid.PICC_HaltA(); // Halt PICC
}
