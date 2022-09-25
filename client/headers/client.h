#if defined (ARDUINO_ARCH_ESP8266)
#include <ESP8266WiFi.h>
#elif defined (ESP32)
#include <WiFi.h>
#else
#error Architecture not supported.
#endif

#include "env.h"
#include "misc.h"
#include "ChangeHandler.h"
#include "Timer.h"
#include <Wire.h>
#include "Adafruit_SHT31.h"