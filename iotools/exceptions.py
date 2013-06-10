'''
Created on 8 avr. 2013

@author: gabriel
'''

class IOToolsException(Exception):
    pass

class CommandError(IOToolsException):
    pass

class CliArgumentError(CommandError):
    pass

class DeviceError(IOToolsException):
    pass
    
class DeviceResponseError(DeviceError):
    pass

class NoDeviceResponse(DeviceResponseError):
    pass