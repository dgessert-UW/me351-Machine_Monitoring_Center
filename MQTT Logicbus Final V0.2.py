import MMC_Modbus
import MMC_MQTT
from datetime import datetime
import time
import Device_Data   
     
sample_rate=60 # The amount of time between a specific sensor being sampled (value in second)
               # If you set sample_rate = 60 the first sensor will be sampled, it will loop through the other sensors
               # and the next response from the first sensor will be 60 seconds later.

existing_devices =Device_Data.data_load()
print(existing_devices)
pause_time = sample_rate / len(existing_devices) 

Offline_Data_Collection = []

MQTT_client = MMC_MQTT.MQTT_connect()

modbus_connection = MMC_Modbus.modbus_connect()

MQTT_Failures = 0

while True:
    
    if modbus_connection == False:
        modbus_connection = MMC_Modbus.modbus_connect()
        if modbus_connection == False:
            payload =str({'Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'Output':'Unable to Connect to Converter','Unit':'-','Sensor_ID_Code':'NA'})
    
    else:           
        for device_name in existing_devices:
            time.sleep(pause_time)
            try:
                modbus_return = MMC_Modbus.modbus_read_holding_registers(modbus_connection ,existing_devices[device_name]['Address'],
                                                                existing_devices[device_name]['Count'],
                                                                existing_devices[device_name]['SlaveID'])
                
                payload =str({'Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'Output':str(modbus_return),'Unit':'C','Sensor_ID_Code':str(existing_devices[device_name]['Type'])+' '+str(existing_devices[device_name]['SlaveID'])})
            except:
    
                modbus_connection = MMC_Modbus.modbus_connect()
                if modbus_connection == False:
                    payload =str({'Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'Output':'Unable to Connect to Converter','Unit':'-','Sensor_ID_Code':str(existing_devices[device_name]['Type'])+' '+str(existing_devices[device_name]['SlaveID'])})
                else:
                    try:
                        modbus_return = MMC_Modbus.modbus_read_holding_registers(modbus_connection ,existing_devices[device_name]['Address'],
                                                                        existing_devices[device_name]['Count'],
                                                                        existing_devices[device_name]['SlaveID'])
                        
                        payload =str({'Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'Output':str(modbus_return),'Unit':'C','Sensor_ID_Code':str(existing_devices[device_name]['Type'])+' '+str(existing_devices[device_name]['SlaveID'])})
                    except:
                        payload =str({'Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'Output':'Device Unresponsive','Unit':'-','Sensor_ID_Code':str(existing_devices[device_name]['Type'])+' '+str(existing_devices[device_name]['SlaveID'])})
        

            try:
                if len(Offline_Data_Collection) == 0:
                    MMC_MQTT.MQTT_publish(MQTT_client,
                                    'home/sensor_data',
                                    payload )
                else:
                    if MQTT_client == False:
                        MQTT_client = MMC_MQTT.MQTT_connect()
                    for offline_payload in Offline_Data_Collection:
                        MMC_MQTT.MQTT_publish(MQTT_client,
                                    'home/sensor_data',
                                    offline_payload)
                        time.sleep(0.1)
                    Offline_Data_Collection = []   
                    MMC_MQTT.MQTT_publish(MQTT_client,
                                'home/sensor_data',
                                payload)                       
                    
            except:
                Offline_Data_Collection.append(payload)




