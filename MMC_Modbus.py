from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import struct
def modbus_connect(parity = 'E',bytesize =8,baudrate =19200,stopbits = 1,port='/dev/ttyUSB0',method= 'rtu'):
    try:
        client = ModbusClient(method= method,port=port,stopbits = stopbits,
                              bytesize =bytesize, parity = parity, baudrate =baudrate)

        client.connect()
        return client
    except:
        print('F')
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