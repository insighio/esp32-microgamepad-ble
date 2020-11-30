# esp32-microgamepad-ble
Dual analog joystick on ESP32 over BLE (Nordic UART Service - NUS) using micropython

The purpose of this project is to create a dual-joystick analog gamepad that will be transmitting over BLE the values using an ESP32 device. 
It is an ideal controller for robot projects. Joystick 1 is used for steering and Joystick 2 is used for controlling camera movement. 

# Components
* ESP32 with micropython firmware
    * ideally use one of the latest firmwares as BLE was recently supported. Tested with: esp32-idf4-20200902-v1.13.bin
* Breadboard / Prototyping board
* Resistor 10κΩ x2
* Analog Joystick 5-Pin x2

![img](https://github.com/insighio/esp32-microgamepad-ble/blob/main/analog_joystick.jpeg)

# Wiring
Allthough the analog joysticks label the input as 5V, they perfectly work with 3.3V which will be used in our schematic. Also J1, J2 will be abreviations for Joystick 1 and Joystick 2. 

To enable the digital input of the button click when the joystick is pressed, a resistor of 10kΩ is connected to the 3.3V of the ESP32 one the one hand, and to the respective GPIO where the SW pins of the joystics are connected (GPIO25, GPIO26)

| Component PIN | ESP PIN |
| ------------- | ------- |
| J1 5V | 3.3V |
| J2 5V | 3.3V |
| Resistor 1 | 3.3V |
| Resistor 2 | 3.3V |
| J2 GND | GND |
| J1 GND | GND |
| J1 VRx | GPIO34 |
| J1 VRy | GPIO35 |
| J1 SW | GPIO25 |
| J2 VRx | GPIO32 |
| J2 VRy | GPIO33 |
| J2 SW | GPIO26 |
| Resistor 1 | GPIO25 |
| Resistor 2 | GPIO26 |

![complete schematic](https://github.com/insighio/esp32-microgamepad-ble/blob/main/schematics.png)

# On Raspberri Pi
An interesting alternative on how to read the analog values of the Joysticks is the use of a Raspberry Pi with an MCP3008 analog-to-digital converter.

link: https://tutorials-raspberrypi.com/raspberry-pi-joystick-with-mcp3008/

# references
* https://medium.com/@codeyourventurefree/diy-iot-joytick-to-play-online-claw-machines-175206679fc9
* https://esp32.com/viewtopic.php?t=14803
* https://docs.micropython.org/en/latest/library/ubluetooth.html
* https://github.com/micropython/micropython/tree/master/examples/bluetooth
