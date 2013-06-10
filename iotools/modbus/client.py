# -*- coding: utf-8 -*- 
"""
Created on 15 mai 2013

@author: gabriel
"""
from iotools.exceptions import NoDeviceResponse

class BaseModbusClient(object):
    
    pdu_addressing = False
    
    def __init__(self,
                 host,
                 unit=1,
                 port=502,
                 method="tcp",
                 stopbits=1,
                 bytesize=8,
                 parity='E',
                 baudrate=115200,
                 timeout=1,):
        self.host = host
        self.unit = unit
        self.port = port
        self.method = method
        self.stopbits = stopbits
        self.bytesize = bytesize
        self.parity = parity
        self.baudrate = baudrate
        self.timeout = timeout
#         self.pdu_addressing = pdu_addressing

#     def translate_address(self, user_input_address):
#         if self.pdu_addressing:
#             return user_input_address - 1
#         return user_input_address
    
class PyModbusClient(BaseModbusClient):
    
    def __init__(self, *args, **kwargs):
        
        super(PyModbusClient, self).__init__(*args, **kwargs)

        if self.method == "tcp":
            from pymodbus.client.sync import ModbusTcpClient
            self.client = ModbusTcpClient(self.host, self.port)
        else:
            from pymodbus.client.sync import ModbusSerialClient
            argnames = ("stopbits", "bytesize", "parity", "baudrate", "timeout")
            kwargs = dict((k, getattr(self, k)) for k in argnames)
            kwargs.update({
                "port": self.host,
            })
            self.client = ModbusSerialClient(self.method, **kwargs)
    
    def read_coils(self, address, count):
        resp = self.client.read_coils(address, count, unit=self.unit)
        if resp is None:
            raise NoDeviceResponse()
        return resp.bits[:count]
    
    def write_coil(self, address, value):
        resp = self.client.write_coil(address, int(value), unit=self.unit)
        if resp is None:
            raise NoDeviceResponse()
        return resp.value
    
class ModbusTkClient(BaseModbusClient):
    
    def __init__(self, *args, **kwargs):
        super(ModbusTkClient, self).__init__(*args, **kwargs)
        
        from modbus_tk import defines
        self.defines = defines
        
        if self.method == "rtu":
            import serial
            from modbus_tk.modbus_rtu import RtuMaster
            kwargs = {
                "port": self.host,
            }
            argnames = ("baudrate", "bytesize", "parity", "stopbits")
            kwargs.update(dict((k,getattr(self,k)) for k in argnames))
            s = serial.Serial(**kwargs)
            client = RtuMaster(s)
            client.set_timeout(self.timeout)
            client.set_verbose(True)
            self.client = client
        else:
            raise NotImplementedError(u"Modbus method not implemented by modbus-tk client: %s" % self.method)
        
    def read_coils(self, address, count):
        resp = self.client.execute(self.unit, self.defines.READ_COILS, address, count)
        return resp
    
    def read_discrete_inputs(self, address, count):
        return self.client.execute(self.unit, self.defines.READ_DISCRETE_INPUTS, address, count)
    
    def write_coil(self, address, value):
        resp = self.client.execute(self.unit, self.defines.WRITE_SINGLE_COIL, address, output_value=int(value))
        return resp