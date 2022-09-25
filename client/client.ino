#include "headers/client.h"

int port = 8888;
WiFiServer server(port);
WiFiClient client;

const IPAddress serverIP (192,168,1,79);
uint16_t serverPort =  62302;

IPAddress local_IP(192, 168, 1, 82);
IPAddress gateway(192, 168, 1, 254);
IPAddress subnet(255, 255, 255, 0);

Timer sendTimer;
Timer idleTimer;

ChangeHandler onButton;
ChangeHandler offButton;

void setup() {
    Serial.begin(115200);

    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWORD); // SSID and PASSWORD must be defined in headers/env.h!

    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(5, OUTPUT);

    pinMode(4, INPUT);
    pinMode(12, INPUT);

    if (!WiFi.config(local_IP, gateway, subnet)) {
        Serial.println("STA Failed to configure");
    }

    Serial.println((String)"Connecting to " + SSID);
    while (WiFi.status() != WL_CONNECTED) {   
        delay(500);
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
        Serial.print(".");
    }

    Serial.println((String)"\nConnected to " + SSID);

    Serial.println((String)"IP address: " + WiFi.localIP().toString());
    server.begin();
    Serial.print((String)"Open Telnet and connect to IP: " + WiFi.localIP().toString() + " on port " + (String)port);
}

void loop() {
    while (!client.connected()) {
        client.connect(serverIP, serverPort);
        delay(200);
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));

        Serial.println("Trying to connect to the server...");
    }

    Client *c = &client;

    c->setTimeout(10);

    if (client.available()) {
        String line = c->readStringUntil('\n');
        bool value = line.toInt();
        digitalWrite(5, value);
        Serial.println(value);
    }

    if (idleTimer.isTime(100, millis())) {
        client.println("OK");
    }

    onButton.onChange(digitalRead(4), [](float state) {
        if (state) client.println(1);
    });

    offButton.onChange(digitalRead(12), [](float state) {
        if (state) client.println(0);
    });

    digitalWrite(LED_BUILTIN, LOW);
}