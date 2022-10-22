from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

def MQTT_connect():
    try:
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

def MQTT_publish(myMQTTClient,topic,payload):
    myMQTTClient.publish(topic=topic,
                            QoS=0,
                            payload= payload)