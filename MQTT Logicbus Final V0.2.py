import MMC_Modbus
import MMC_MQTT
from datetime import datetime
        
        
def testing(sample_rate=60):
    MQTT_Failures = 0
    Offline_Data_Collection = {}
    existing_devices = {'Temp Sensor 1':{'Address':100,'SlaveID':1,'Count':2,'Type':'Temperature'},
                        'Temp Sensor 2':{'Address':100,'SlaveID':2,'Count':2,'Type':'Temperature'},
                        'Temp Sensor 3':{'Address':100,'SlaveID':3,'Count':2,'Type':'Temperature'}}
    pause_time = sample_rate / len(existing_devices)
    MQTT_client = MMC_MQTT.MQTT_connect()

    modbus_connection = MMC_Modbus.modbus_connect()
    while True:
        if modbus_connection == False:
            #time.sleep(sample_rate)
            modbus_connection = MMC_Modbus.modbus_connect()
            payload =str({'Temperature':'Unable to Establish Modbus Connection','Unit':'-','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
        
        else:           
            for device_name in existing_devices:
                #time.sleep(pause_time)

                try:
                    modbus_return = MMC_Modbus.modbus_read_holding_registers(modbus_connection ,existing_devices[device_name]['Address'],
                                                                  existing_devices[device_name]['Count'],
                                                                  existing_devices[device_name]['SlaveID'])
                    
                    payload =str({'Temperature':str(modbus_return),'Unit':'C','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
                except:        
                    payload =str({'Temperature':'Device Unresponsive','Unit':'-','Time':datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
                
                print(payload)
                try:
                    if MQTT_Failures == 0:
                        MMC_MQTT.MQTT_publish(MQTT_client,
                                     'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                     payload )
                    else:
                        for device_name in Offline_Data_collection:
                            print('138')
                            MMC_MQTT.MQTT_publish(MQTT_client,
                                     'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']),
                                     Offline_Data_collection[device_name])
                            print('142')
                        MQTT_Failures = 0
                        Offline_Data_collection = {}
                except:
                    Offline_Data_collection[device_name]+=payload
            
#'home/'+existing_devices[device_name]['Type']+'/'+str(existing_devices[device_name]['SlaveID']) 


testing()
