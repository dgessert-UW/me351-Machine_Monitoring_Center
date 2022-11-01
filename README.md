# me351-Machine_Monitoring_Center
The files in this repository are meant to communicate with LogicBus sensors using a raspberrypi through a waveshare usb converter.

LogicBus Temperature Sensor: https://www.logicbus.com/TST300v2_p_30453.html

Waveshare USB Converter: https://www.waveshare.com/usb-to-rs485.htm

Downloading and updating the repository on the PI

<img width="501" alt="image" src="https://user-images.githubusercontent.com/99203836/199290360-6ad1c96f-61c6-4fdb-92bd-58e1f1b33865.png">

# MMC_Modbus.py
This file handles all the communication between the pi and the sensors

We import just two outside modules for to complete the communication.

      from pymodbus.client.sync import ModbusSerialClient as ModbusClient
      import struct

ModbusSerialClient - has all the capabilities that me need to establish the modbus connection and then read the sensors
struct - we need this module to convert the sensor response from hex to a readable temperature value

# MMC_MQTT.py
This file handle the initial connection of the raspberrypi to the AWS server and then handles the publishing of the data to the server

We import just one module.

      from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
      
This is a package supported by amazon which has all the tools to complete communication. There are two major functions within this file:
      MQTT_connect()
      MQTT_publish()
MQTT_connect() function 
