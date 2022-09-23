/*
 * Выберите LightToggleHandler или LEDToggleHandler, как обработчик.
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

ChangeHandler onButton;
ChangeHandler offButton;

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

    onButton.onChange(digitalRead(13), [](float state) {
        if (state) client.println(1);
    });

    offButton.onChange(digitalRead(12), [](float state) {
        if (state) client.println(0);
    });

    digitalWrite(27, LOW);
    digitalWrite(26, HIGH);
}