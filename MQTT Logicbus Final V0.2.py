#import MMC_Modbus
import MMC_MQTT
from datetime import datetime
import time
import Device_Data

        
     
sample_rate=60
MQTT_Failures = 0
Offline_Data_Collection = {}
<<<<<<< HEAD



existing_devices =Device_Data.data_load()
print(existing_devices)


#{'Temp Sensor 1':{'Address':100,'SlaveID':1,'Count':2,'Type':'Temperature'},
#                    'Temp Sensor 2':{'Address':100,'SlaveID':2,'Count':2,'Type':'Temperature'},
#                    'Temp Sensor 3':{'Address':100,'SlaveID':3,'Count':2,'Type':'Temperature'}}
=======
existing_devices = {'Temp Sensor 1':{'Address':100,'SlaveID':1,'Count':2,'Type':'Temperature'},
                    'Temp Sensor 2':{'Address':100,'SlaveID':2,'Count':2,'Type':'Temperature'},
                    'Temp Sensor 3':{'Address':100,'SlaveID':3,'Count':2,'Type':'Temperature'}}

>>>>>>> parent of 18f0d39 (Revert "MQTT Logicbus Final V0.2")
pause_time = sample_rate / len(existing_devices)


MQTT_client = MMC_MQTT.MQTT_connect()


modbus_connection = MMC_Modbus.modbus_connect()


while True:
    time.sleep(pause_time)
    if modbus_connection == False:
        modbus_connection = MMC_Modbus.modbus_connect()
        payload =str({'Temperature':'Unable to Establish Modbus Connection','Unit':'-','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
    
    else:           
        for device_name in existing_devices:
            try:
                modbus_return = MMC_Modbus.modbus_read_holding_registers(modbus_connection ,existing_devices[device_name]['Address'],
                                                                existing_devices[device_name]['Count'],
                                                                existing_devices[device_name]['SlaveID'])
                
                payload =str({'Temperature':str(modbus_return),'Unit':'C','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            except:        
                payload =str({'Temperature':'Device Unresponsive','Unit':'-','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            

            try:
                if MQTT_Failures == 0:
                    MMC_MQTT.MQTT_publish(MQTT_client,
                                    'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                    payload )
                else:
                    for device_name in Offline_Data_Collection:
                        MMC_MQTT.MQTT_publish(MQTT_client,
                                    'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                    Offline_Data_Collection[device_name])

                    MQTT_Failures = 0
                    Offline_Data_Collection = {}
            except:
                Offline_Data_Collection[device_name]+=[payload]
        




