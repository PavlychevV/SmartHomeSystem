/*
 * Выберите LEDDimHandler, как обработчика.
 */

#include "headers/client.h"

int port = 8888;
WiFiServer server(port);
WiFiClient client;

const IPAddress serverIP (192,168,1,79);
uint16_t serverPort =  62302;

IPAddress local_IP(192, 168, 1, 87);
IPAddress gateway(192, 168, 1, 254);
IPAddress subnet(255, 255, 255, 0);

ChangeHandler onBrightness;
Timer stepTimer;
Timer sendTimer;
int brightness = 0;

void setup() {
    Serial.begin(115200);

    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWORD); // SSID and PASSWORD must be defined in env.h!

    pinMode(13, INPUT_PULLDOWN);
    pinMode(12, INPUT_PULLDOWN);

    pinMode(27, OUTPUT);
    pinMode(26, OUTPUT);

    if (!WiFi.config(local_IP, gateway, subnet)) {
        Serial.println("STA Failed to configure");
    }

    Serial.println((String)"Connecting to " + SSID);
    while (WiFi.status() != WL_CONNECTED) {   
        delay(500);
        digitalWrite(27, !digitalRead(27));
        digitalWrite(26, !digitalRead(26));
        Serial.print(".");
    }

    Serial.println((String)"\nConnected to " + SSID);

    Serial.println((String)"IP address: " + WiFi.localIP().toString());
    server.begin();
    Serial.print((String)"Open Telnet and connect to IP: " + WiFi.localIP().toString() + " on port " + port);

}

void loop() {

    while (!client.connected()) {
        client.connect(serverIP, serverPort);
        delay(500);
        digitalWrite(27, !digitalRead(27));
        digitalWrite(26, LOW);
    }

    if (stepTimer.isTime(500, micros())) {
        if (digitalRead(13))
            brightness++;

        if (digitalRead(12))
            brightness--;
    }

    if (brightness > 1023)
        brightness = 1023;

    if (brightness < 0)
        brightness = 0;

    if (sendTimer.isTime(50, millis()))
        onBrightness.onChange(brightness, [](float value) {
            client.println(brightness);
        });

    digitalWrite(27, LOW);
    digitalWrite(26, HIGH);
}