#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ArduinoOTA.h>
#include <InfluxDbClient.h>
#include "HueySecrets.h"


// Create an instance of the ESP8266WiFiMulti class and InfluxDB client
ESP8266WiFiMulti wifiMulti;     
InfluxDBClient client(INFLUXDB_URL, INFLUXDB_DB_NAME);

// Data point
Point sensor("voltage");

int sensorPin = A0; 
float vOUT = 0.0;
float vIN = 0.0;
float R1 = 30000.0;
float R2 = 7500.0;

float R3 = 46760;
float R4 = 20540;

const char* ssid = STASSID;
const char* password = STAPSK;

void setup() {

  Serial.begin(115200);
  Serial.println("Booting");

  wifiMulti.addAP(ssid, password); 
  while (wifiMulti.run() != WL_CONNECTED) { 
    // Wait for the Wi-Fi to connect
    delay(250);
    Serial.print('.');
  }
  ArduinoOTA.setHostname(WEMOS_D1_A);

  ArduinoOTA.onStart([]() {
    String type;
    if (ArduinoOTA.getCommand() == U_FLASH) {
      type = "sketch";
    } else { // U_FS
      type = "filesystem";
    }

    // NOTE: if updating FS this would be the place to unmount FS using FS.end()
    Serial.println("Start updating " + type);
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("\nEnd");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) {
      Serial.println("Auth Failed");
    } else if (error == OTA_BEGIN_ERROR) {
      Serial.println("Begin Failed");
    } else if (error == OTA_CONNECT_ERROR) {
      Serial.println("Connect Failed");
    } else if (error == OTA_RECEIVE_ERROR) {
      Serial.println("Receive Failed");
    } else if (error == OTA_END_ERROR) {
      Serial.println("End Failed");
    }
  });
  ArduinoOTA.begin();
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Set InfluxDB 1 authentication params
  client.setConnectionParamsV1(INFLUXDB_URL, INFLUXDB_DB_NAME, INFLUXDB_USER, INFLUXDB_PASSWORD);

  // Add constant tags - only once
  sensor.addTag("circuit", "24V house");

  // Check server connection
  if (client.validateConnection()) {
    Serial.print("Connected to InfluxDB: ");
    Serial.println(client.getServerUrl());
  } else {
    Serial.print("InfluxDB connection failed: ");
    Serial.println(client.getLastErrorMessage());
  }
}

void loop() {
  ArduinoOTA.handle();

  // Store measured value into point
  sensor.clearFields();
  
  // read the input on analog pin 0:
  int sensorValue = analogRead(A0);
  
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 3.3V):
  float vOUT = sensorValue * (3.3 / 1023.0);
  vIN = vOUT / (R2 / (R1 + R2));
  vIN = (vIN / (R4 / (R3 + R4))) * 0.950;

  // s
  
  sensor.addField("voltage", vIN);
  // Print what are we exactly writing
  Serial.println("vOUT: ");
  Serial.println(vOUT);
  Serial.println("Writing: ");
  Serial.println(sensor.toLineProtocol());

  // Write point
  if (!client.writePoint(sensor)) {
    Serial.print("InfluxDB write failed: ");
    Serial.println(client.getLastErrorMessage());
  }
  
  //Wait 10s
  delay(10000);
}
