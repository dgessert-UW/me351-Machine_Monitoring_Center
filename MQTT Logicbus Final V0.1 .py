import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
import smtplib
import datetime
import time
from datetime import datetime


def email_module(temp, temp_unit):
    try:
        with smtplib.SMTP("smtp.gmail.com",587) as smtp:
            smtp.ehlo()
            smtp.starttls()

            smtp.login('machinemonitoringcenter@gmail.com','hlvekejgxyslqiet')
                #gmail for this project: machinemonitoringcenter@gmail.com
                #gmail password: MMC#2022
            subject = 'Temperature Error'
            if temp_unit == '°C':
                temp_unit = 'Celcius'
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            body = 'The temperature was recorded at '+str(round(float(temp),2))+'  '+str(temp_unit)+' at '+str(current_time)
            msg = f'Subject: {subject}\n\n{body}'
            print(msg)
            
            smtp.sendmail('machinemonitoringcenter@gmail.com',['dylangessert@gmail.com','dgessert@wisc.edu'], msg)
            #'minlab@office365.wisc.edu'   #minlab mailing list
    except:
        try:
            #Safe Message, Possible there's a charecter in the message that caused it to fail
            with smtplib.SMTP("smtp.gmail.com",587) as smtp:
                smtp.ehlo()
                smtp.starttls()

                smtp.login('machinemonitoringcenter@gmail.com','hlvekejgxyslqiet')
                    #gmail for this project: machinemonitoringcenter@gmail.com
                    #gmail password: MMC#2022
                subject = 'Temperature Error'
                body = 'There was an out of range temp recorded I can not tell you the exact number'
                msg = f'Subject: {subject}\n\n{body}'
                print(msg)
                
                smtp.sendmail('machinemonitoringcenter@gmail.com',['dylangessert@gmail.com','dgessert@wisc.edu'], msg)
                #'minlab@office365.wisc.edu'   #minlab mailing list
        except:
            print('emailing error')
            pass
def modbus_connect():
    try:
        client = ModbusClient(method= 'rtu',port='/dev/ttyUSB0',stopbits = 1,
                              bytesize =8, parity = 'E', baudrate =19200)

        client.connect()
        return client
    except:
        print('F')
        return False

def MQTT_connect():
    try:
        from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
        myMQTTClient = AWSIoTMQTTClient("MMCID")
        myMQTTClient.configureEndpoint("a3r5ud4y7va9gp-ats.iot.us-east-1.amazonaws.com", 8883)
        
        #Directory of the AWS assigned credential files
        myMQTTClient.configureCredentials("/home/pi/AWSIoT/root-CA.crt","/home/pi/AWSIoT/lab-raspberrypi-temperature.private.key","/home/pi/AWSIoT/lab-raspberrypi-temperature.cert.pem")

        myMQTTClient.configureOfflinePublishQueueing(-1)
        myMQTTClient.configureDrainingFrequency(2)
        myMQTTClient.configureConnectDisconnectTimeout(30)
        myMQTTClient.configureMQTTOperationTimeout(5)

        myMQTTClient.connect()
        
        return myMQTTClient
    except:
        return False

def modbus_read_holding_registers(client,address, count, slave_id):
    read=client.read_holding_registers(address = address,count =count, unit = slave_id)#address = 100 ,count =2,unit=sensor) 
    print(read)
    data = read.registers
    print(data)
    print(type( data[0]))
    a = data[0]
    b = data[1]
    temperature = str(struct.unpack('>f', bytes.fromhex(f"{a:0>4x}" + f"{b:0>4x}"))[0])
    return temperature
    
def MQTT_publish(myMQTTClient,topic,payload):
    myMQTTClient.publish(topic=topic,
                            QoS=0,
                            payload= payload)

          
        
        
def testing(sample_rate=60):
    MQTT_Failures = 0
    Offline_Data_Collection = {}
    existing_devices = {'Temp Sensor 1':{'Address':100,'SlaveID':1,'Count':2,'Type':'Temperature'},
                        'Temp Sensor 2':{'Address':100,'SlaveID':2,'Count':2,'Type':'Temperature'},
                        'Temp Sensor 3':{'Address':100,'SlaveID':3,'Count':2,'Type':'Temperature'}}
    pause_time = sample_rate / len(existing_devices)
    MQTT_client = MQTT_connect()

    modbus_connection = modbus_connect()
    while True:
        if modbus_connection == False:
            #time.sleep(sample_rate)
            modbus_connection = modbus_connect()
            payload =str({'Temperature':'Unable to Establish Modbus Connection','Unit':'-','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        
        else:           
            for device_name in existing_devices:
                #time.sleep(pause_time)

                try:
                    modbus_return = modbus_read_holding_registers(modbus_connection ,existing_devices[device_name]['Address'],
                                                                  existing_devices[device_name]['Count'],
                                                                  existing_devices[device_name]['SlaveID'])
                    
                    payload =str({'Temperature':str(modbus_return),'Unit':'C','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
                except:        
                    payload =str({'Temperature':'Device Unresponsive','Unit':'-','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
                
                print(payload)
                try:
                    if MQTT_Failures == 0:
                        MQTT_publish(MQTT_client,
                                     'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                     payload )
                    else:
                        for device_name in Offline_Data_collection:
                            print('138')
                            MQTT_publish(MQTT_client,
                                     'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                     Offline_Data_collection[device_name])
                            print('142')
                        MQTT_Failures = 0
                        Offline_Data_collection = {}
                except:
                    Offline_Data_collection[device_name]+=payload
            
#'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']) 


testing()
