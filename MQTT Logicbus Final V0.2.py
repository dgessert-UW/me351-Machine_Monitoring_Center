import MMC_Modbus
import MMC_MQTT
from datetime import datetime
import time
import Device_Data

        
     
sample_rate=60
MQTT_Failures = 0
Offline_Data_Collection = {}



existing_devices =Device_Data.data_load()
print(existing_devices)


#{'Temp Sensor 1':{'Address':100,'SlaveID':1,'Count':2,'Type':'Temperature'},
#                    'Temp Sensor 2':{'Address':100,'SlaveID':2,'Count':2,'Type':'Temperature'},
#                    'Temp Sensor 3':{'Address':100,'SlaveID':3,'Count':2,'Type':'Temperature'}}



pause_time = sample_rate / len(existing_devices)


MQTT_client = MMC_MQTT.MQTT_connect()


modbus_connection = MMC_Modbus.modbus_connect()


while True:
    
    if modbus_connection == False:
        modbus_connection = MMC_Modbus.modbus_connect()
        payload =str({'Temperature':'Unable to Establish Modbus Connection','Unit':'-','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
    
    else:           
        for device_name in existing_devices:
            time.sleep(pause_time)
            try:
                modbus_return = MMC_Modbus.modbus_read_holding_registers(modbus_connection ,existing_devices[device_name]['Address'],
                                                                existing_devices[device_name]['Count'],
                                                                existing_devices[device_name]['SlaveID'])
                
                payload =str({'Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'Output':str(modbus_return),'Unit':'C'})
            except:        
                payload =str({'Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'Output':'Device Unresponsive','Unit':'-'})
            

            try:
                if len(Offline_Data_Collection) == 0:
                    MMC_MQTT.MQTT_publish(MQTT_client,
                                    'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                    payload )
                else:
                    if MQTT_client == False:
                        MQTT_client = MMC_MQTT.MQTT_connect()
                    for offline_device_name in Offline_Data_Collection:
                        for offline_payload  in Offline_Data_Collection[offline_device_name]:
                            
                            MMC_MQTT.MQTT_publish(MQTT_client,
                                        'home/'+str(existing_devices[offline_device_name]['Type'])+'/'+str(existing_devices[offline_device_name]['SlaveID']),
                                        offline_payload)
                            time.sleep(0.1)
                        
                    MMC_MQTT.MQTT_publish(MQTT_client,
                                'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                payload)                       
                    Offline_Data_Collection = {}
            except:
                if device_name not in Offline_Data_Collection:
                    Offline_Data_Collection[device_name]=[payload]
                else:
                    Offline_Data_Collection[device_name].append(payload)




