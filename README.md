# me352-Machine_Monitoring_Center
The files in this repository are meant to communicate with LogicBus sensors using a raspberrypi through a waveshare usb converter.

LogicBus Temperature Sensor: https://www.logicbus.com/TST300v2_p_30453.html

Waveshare USB Converter: https://www.waveshare.com/usb-to-rs485.htm

# Wiring Diagram

Below is a diagram for the wiring of the sensors in our setup.

![Wiring](https://user-images.githubusercontent.com/99203836/206080425-6ecd5833-1759-4965-861d-9c5c9777b557.jpg)

# Connecting to the Raspberry PI

If you want to inferface with the Raspberry PI you can physically interface using a monitor and a micro HDMI to HDMI.

Otherwise you can connect with the Raspberry PI using VNC Viewer. In order to do this the PI as to be powered on an connected to the UWNet. Then with your computer connected to UWNet you can enter the following IP: 10.140.211.57 into the search bar. 

<img width="658" alt="MicrosoftTeams-image" src="https://user-images.githubusercontent.com/99203836/206081000-b17739b0-3ba0-4ddc-bc2a-8d40934d6164.png">

Hit enter and you will be prompted to log in for our device: username: pi password: MMC


# Downloading and updating the repository on the PI
Downloading:
To download the git hub code for the first time use the git clone command in the PI terminal:
<img width="373" alt="image" src="https://user-images.githubusercontent.com/99203836/199291117-dee23a14-e89f-4e3c-8d8d-8605040ed3f3.png">

Updating:
When you make changes to the code on the github side you can update the code on the PI using the "git pull" command in the PI terminal:

<img width="501" alt="image" src="https://user-images.githubusercontent.com/99203836/199290360-6ad1c96f-61c6-4fdb-92bd-58e1f1b33865.png">

When you make changes to the code on the PI side you can update the code on the github side using the "git push" command in the PI terminal.

# MMC_Modbus.py
This file handles all the communication between the pi and the sensors

We import just two outside modules for to complete the communication.

      from pymodbus.client.sync import ModbusSerialClient as ModbusClient
      import struct

Here's the documentation for the pymodbus client

https://pymodbus.readthedocs.io/en/latest/source/library/pymodbus.client.htmls

ModbusSerialClient - has all the capabilities that me need to establish the modbus connection and then read the sensors

struct - we need this module to convert the sensor response from hex to a readable temperature value

We've got two main functions in this code for reading the senors the first estalishes a connection through the waveshare usb converter:

      modbus_connect(parity = 'E',bytesize =8,baudrate =19200,stopbits = 1,port='/dev/ttyUSB0',method= 'rtu')

**parity,bytesize,baudrate,stopbits -** these are a defined by the requirements of the senors, the default values in the function will work with the logic bus sensor.

**port-** this value is determined by the port the converter is hooked up to, if it is the only serial converter connected on boot the port will be the default value listed

**method-** our setup utilizes serial protocols so it should always be the default

Function outputs: The modbus_connect function will either return a successfull connection or it will try multiple different usb ports and if it still can't connect it will return the boolean value of False, and it's set up that way so that the code will not crash if the USB converter is unpluged and then pluged back in.

The other major function is:

      modbus_read_holding_registers(client,address, count, slave_id)
      
"read holding registers" is a standard modbus function and for the logicbus senors it's what we use to communicate with the senors. 

**client -**  this is the connection that is a established by "modbus_connect()" our main script is written in such a way that that "modbus_read_holding_registers()" isn't ran unless the modbus connection is successfully established if you recieve a False boolean value from "modbus_connect()" and put it into "modbus_read_holding_registers()" the code will crash.

**address -** this is a property of the message you want to recieve from the sensor

**count -** this is a property of the address for the logicbus temp sensors count should be equal to 2

**slave_id -**  this is a property of the modbus setup no two sensors can have the same slave_id

# MMC_MQTT.py
This file handle the initial connection of the raspberrypi to the AWS server and then handles the publishing of the data to the server

We import just one module.

      from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
      
Here's the documentation for the function:

https://s3.amazonaws.com/aws-iot-device-sdk-python-docs/sphinx/html/index.html

This is a package supported by amazon which has all the tools to complete communication. There are two major functions within this file:
      MQTT_connect()
      MQTT_publish()
MQTT_connect() function 

# Device_List.json

This is a JSON file which stores all of the data for the sensors in the system. It's the cleanest way to keep track of the sensors in the system and add/subtract sensors from the system. An example of the JSON file format is shown below.

![image](https://user-images.githubusercontent.com/99203836/205469225-34f399d4-6931-4ac5-99f5-b075be011f46.png)

In a JSON file you have a key, which for our files are just a name to identify the sensor, this key should be unique from other keys, but aslong as it the key is a string the, name you chose to identify the sensor doesn't effect the code. Each key (sensor name) has a corresponding value in our case the the value is another JSON structure. This embeded JSON structure holds all the sensor communication attributes, so the address, slaveid, count, and the type of sensor (temperature or humidity). Your input for type of sensor will be paired with the slaveid and sent to AWS in the payload in order to help identify the sensor.

# Device_Data.py

This file is called in the main script to load the data from Data_List.json and do a basic check on the json data to check that the format of the JSON (input types) are correct. The only function from this script that is called in the main file is:
      
      data_load(path = str(os.getcwd())+'/Device_List.json')

If you clone this repository as shown in the beginning of document the code will run with the default value presented in the function. If you do not clone, place the JSON path into the function. If you do not use a JSON file or change the structure of the JSON file shown above you don't need to call this function.

# MQTT Logicbus Final V0.2.py

This is the main file and the only file a user needs to start when they want to collect data. The afforementioned files are imported as needed. There are just a couple parameters the user need to be aware of when running this script. 

The only value a user should be changing is "sample_rate".

<img width="599" alt="image" src="https://user-images.githubusercontent.com/99203836/206254024-a7c3e740-1b3b-4ce7-a139-5a8c53f8c26f.png">

sample_rate defines the amount of time we pause between sampling a specific sensor in seconds. 

The code is setup such that it will load in the sensors from the aforementioned JSON file, it will then determine the number of sensors that we are going to be scanning for.

pause_time is then determined by dividing the sample_rate by the number of sensor.

If you set sample_rate = 60 (1 minute) and you have 2 sensors listed in Device_List.json the pause time will be 30 seconds meaning you will sample sensor 1 then pause for 30 seconds, sample sensor 2 then pause for 30 seconds, you will then return to sensor 1 and continue this cycle until the code is manually stopped.



