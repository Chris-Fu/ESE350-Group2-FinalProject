#pragma once

#include "mbed.h" 
#include "USBKeyboard.h"
#include "USBSerial.h"  
#include <stdlib.h> 

AnalogIn touch(p20);
AnalogIn light(p19);

DigitalOut touchLED(LED1);
DigitalOut lightLED(LED2);
DigitalOut clockLED(LED3);
DigitalOut latencyLED(LED4);

Timer t;
Timer t2;

Serial pc(USBTX, USBRX); // tx, rx
USBKeyboard keyboard;


// global variables
float light_thresh = 0.95;
float touch_thresh = 0.95;
float light_grad = 0.05;
float touch_grad = 0.1;

float tdiff = 0;
float tmbed = 0;
float clkratio = 0;

float serialLatency = 0;
float serialLatencySTD = 0;
float USBlatency = 0;
float USBlatencySTD = 0;
