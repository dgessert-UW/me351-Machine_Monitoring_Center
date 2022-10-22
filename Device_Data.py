import json
import os
def device_input_check(existing_devices):
    faults = 0 
    parameter_requirements = {"Address":int(),"SlaveID":int(),"Count":int(),"Type":str()}
    error_messages = []
    for device in existing_devices:
        for parameter in parameter_requirements:
            if parameter not in existing_devices[device]:
                faults += 1
                error_messages.append("You need to include the "+ parameter+" for "+device)
            else:
                if type(existing_devices[device][parameter]) != type(parameter_requirements[parameter]):
                    try:
                        if type(parameter_requirements[parameter]) == type(int()):
                            existing_devices[device][parameter] = int(existing_devices[device][parameter])
                        elif type(parameter_requirements[parameter]) == type(str()):
                            existing_devices[device][parameter] = str(existing_devices[device][parameter])
                        elif type(parameter_requirements[parameter]) == type(float()):
                            existing_devices[device][parameter] = float(existing_devices[device][parameter])
                    except:
                        faults += 1
                        error_messages.append("You need to represent the "+ parameter+" for "+device+" as the following type "+str(type(parameter_requirements[parameter])))
    if len(error_messages) > 0:
        raise ValueError('Fix the following issues in your json files format:'+
        ' '+ str(error_messages))
    else:
        return existing_devices

def data_load(path = str(os.getcwd())+'\Device_List.json'):
    
    json_file_path = path
    with open(json_file_path, 'r') as j: 
        existing_devices = json.loads(j.read())
        j.close()
    data = device_input_check(existing_devices)
    return data

