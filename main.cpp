#include "globals.hpp"
 
float recieveFloat() {
    wait(3); // after 3 seconds, we send the signal that we are ready to recieve
    pc.putc('r');
    wait(1);
    char buffer[10];
    pc.scanf(buffer); // first send is ratio
    return atof(buffer);
}

void sendFloat(float message) {
    pc.printf("%f\r\n", message);
    wait(0.25);
}

 
int getClockVars() {
    clockLED = 1; // signals to user that clock sync is underway
    
    if (pc.getc() == 'i') { // waits for ready signal from pc
        wait(1);
        pc.putc('i');
    }
    
    float data[30];
    for(int i = 0; i < 30; i++) {
        pc.getc();
        data[i] = t.read_us();
    }
    
    
    if (pc.getc() == 'd') { // sends over all data
        wait(1);
        
        for(int i = 0; i < 30; i++) {
            sendFloat(data[i]);
            wait(0.25);
        }
        
        wait(1);
        pc.putc('f');
    }
    
    
    // RECIEVES INFORMATION FROM COMPUTER
    clkratio = recieveFloat();
    tdiff = recieveFloat();
    tmbed = recieveFloat();
    
    
    clockLED = 0;
    return 0;
}




int getUSBLatency() {
    latencyLED = 1;
    
    while (pc.getc() == 'i') { // waits for ready signal from pc
        wait(1);
        keyboard._putc('i');
    }
    
    // SERIAL PINGS
    for (int i = 0; i < 30; i++) {
        pc.getc();
        pc.putc('p');
    }
    
    // USB PINGS
    for (int i = 0; i < 30; i++) {
        pc.getc();
        keyboard._putc(' ');
    }
    
    // RECIEVES INFORMATION FROM COMPUTER
    serialLatency = recieveFloat();
    serialLatencySTD = recieveFloat();
    USBlatency = recieveFloat();
    USBlatencySTD = recieveFloat();
    
    latencyLED = 0;
    return 0;
}


int cognitionRead() {
    lightLED = 1;
    touchLED = 1;
    float tStart = 0;
    // sends spacebar command to start when received spacebar command
    while(1) {
        char rec = pc.getc();
        if (rec == 'i') {
            break;
        }
    }
    keyboard._putc(' ');
    tStart = t.read_us(); // tracks start of cognition
    wait(0.25);
    sendFloat(tStart);
    
    while (1) {
        lightLED = 0;
        touchLED = 0;
        
        //// DEBUGGING
//        float light_sample = light.read();
//        pc.printf("%f\r\n", light_sample);
//        continue;
        
        // wait for light
        float light_sample = light.read();
        float light_data = 0;
        int debounce = 0;
        while (debounce < 3) { // LIGHT DEBOUNCING TIME = UNKNOWN
            while(light_sample > light_thresh) {
                wait(0.0001);
                //pc.printf("%f\r\n", light_sample);
                debounce = 0;
                light_sample = light.read();
            }
            
            if (debounce == 0) {
                light_data = t.read_us();
            }
            
            debounce += 1;
        }
        lightLED = 1;
        
        
        // wait for touch
        float touch_sample = touch.read();
        float touch_data = 0;
        debounce = 0;
        while (debounce < 3) {
            while(touch_sample < touch_thresh) {// - (debounce * touch_grad)) {
                wait(0.0001);
                //pc.printf("%f\r\n", touch_sample);
                debounce = 0;
                touch_sample = touch.read();
            }
            
            if (debounce == 0) {
                touch_data = t.read_us();
            }
            
            debounce += 1;
        }
        touchLED = 1;
        
        
        pc.printf("LIGHT\r\n");
        //sendFloat(light_sample);
        sendFloat(light_data);
        pc.printf("TOUCH\r\n");
        //sendFloat(touch_sample);
        sendFloat(touch_data);
        
        
        // wait for light to turn off
        light_sample = light.read();
        t2.reset();
        while(light_sample < light_thresh) {// && (t2.read() < 100)) {
            light_sample = light.read();
        }
        
        pc.printf("C\r\n");
        //if (t2.read() > 100) { // timout
//            pc.printf("I\r\n");
//        } else {
//            pc.printf("C\r\n");
//        }
        
        // checks if theres any message
        if (pc.readable() != 0) {
            if (pc.getc() == 'q') { // if there is a quit message
                break;
            }
        }
    }
    
    return 0;
}





void turnAllOn() {
    touchLED = 1;
    lightLED = 1;
    clockLED = 1;
    latencyLED = 1;
}

void turnAllOff() {
    touchLED = 0;
    lightLED = 0;
    clockLED = 0;
    latencyLED = 0;
}

void turnSomeOff() {
    touchLED = 1;
    lightLED = 0;
    clockLED = 1;
    latencyLED = 0;
}

void turnOthersOff() {
    touchLED = 0;
    lightLED = 1;
    clockLED = 0;
    latencyLED = 1;
}


 
int main() {
    pc.baud(115200);
    t.start();
    
    while(1){
        turnAllOn();
        char command = pc.getc();
        turnSomeOff();
        wait(0.1);
        turnOthersOff();
        wait(0.1);
        
        int check = 0;
        if (command == 'V'){ // CLOCK VAR SHIT
            wait(1);
            pc.putc('V');
            turnAllOff();
            check = getClockVars();
        } else if (command == 'U'){ // USB SHIT
            wait(1);
            pc.putc('U');
            turnAllOff();
            check = getUSBLatency();
        } else if (command == 'C'){ // COGNITION SHIT
            wait(1);
            pc.putc('C');
            turnAllOff();
            check = cognitionRead();
        } else if (command == 'S') { // SEND ALL VARS
            wait(1);
            pc.putc('S');
            turnAllOff();
            //check = sendAllData();
        }
        
        if (check != 0) {
            
        }
    }
}
