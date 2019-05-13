## Introduction
Most computers cannot accurately measure highly time-sensitive events due to its inherent latency. We built a way to calculate this latency, enabling regular PCs to be used for sensitive research. In particular, the Psychomotor Vigilance Test, which test a person's reaction time, requires an accuracy of measurement down to a few microseconds using a computer screen and keyboard for stimulation and response respectively.

## System Architecture
The test computer displays a stimulus which triggers a light sensor to directly activate a solenoid to press the spacebar. A force sensor is adhered to the spacebar such that it is triggered when the solenoid begins to depress the spacebar. An Mbed is used to measure each time at which the light sensor and force sensor is activated, and saves that information. After many trials to find a data distribution, the difference between what the computer records as the stimulus and response time and what the Mbed records as the stimulus and response time are used as the display and keyboard latency respectively.

## Code
Our code employs two parts: a C++ code section to run the Mbed as well as Python code to communicate with the Mbed and extract the necessary information to calculate the final latencies. Our code is designed that the Mbed can accept a specific group of commands, so one can easily edit the Python code to suit whatever arrangement of calculations they needed.
The first part of our code is a battery of clock calculations. We use PTP protocol along some clock ratio calibration to set our Mbed clock to be the same as our calibration computer. The next step is we run Cognition on the calibration computer and use our Mbed to log timestamps to accurately separate the delays within the computer's total latency.
