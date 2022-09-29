#include "headers/client.h"

WiFiClient client;

const IPAddress serverIP (192,168,1,79);
uint16_t serverPort =  62302;

#if defined (ESP32)
IPAddress local_IP(192, 168, 1, 87);
#else
IPAddress local_IP(192, 168, 1, 82);
#endif

IPAddress gateway(192, 168, 1, 254);
IPAddress subnet(255, 255, 255, 0);

Timer recvTimer;
Timer filterTimer;
Timer sendTimer;
Timer idleTimer;

ChangeHandler onButton;
ChangeHandler offButton;

const int ledPin = 5;

const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;

LowPassFilter filter;
byte newValue, brightness;

void setup() {
    Serial.begin(115200);

    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWORD); // SSID and PAfSSWORD must be defined in headers/env.h!

    pinMode(LED_BUILTIN, OUTPUT);

    #if defined (ESP32)

    // Configure LED PWM functionalitites
    ledcSetup(ledChannel, freq, resolution);

    // Attach the channel to the GPIO to be controlled
    ledcAttachPin(ledPin, ledChannel);
    #else
    pinMode(ledPin, OUTPUT);
    #endif

    #if defined (ESP32)
    pinMode(4, INPUT_PULLDOWN);
    pinMode(12, INPUT_PULLDOWN);
    #else
    pinMode(4, INPUT);
    pinMode(12, INPUT);
    #endif

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
}

void loop() {
    while (!client.connected()) {
        client.connect(serverIP, serverPort);
        digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));

        Serial.println("Trying to connect to the server...");
        recvTimer.reset(millis());
        delay(200);
    }

    if (!client.available()) recvTimer.reset(millis());

    if (recvTimer.isTime(20, millis())) {
        Client *c = &client;
        c->setTimeout(1);

        byte buffer[1];
        c->read(buffer, 1);

        newValue = buffer[0];
    }

    if (filterTimer.isTime(10, millis())) {
        brightness = filter.filter(newValue, 0.7);

        Serial.println((String)newValue + " " + brightness);

        #if defined (ESP32)
        ledcWrite(ledChannel, brightness);
        #else
        analogWrite(ledPin, brightness);
        #endif
    }

    if (idleTimer.isTime(1000, millis()))
        client.println("OK");

    if (sendTimer.isTime(20, millis())) {
        if (digitalRead(4))
            client.println(1);

        if (digitalRead(12))
            client.println(0);
    }

    digitalWrite(LED_BUILTIN, LOW);
}
