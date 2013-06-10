'''
Created on 8 avr. 2013

@author: gabriel
'''
#from iotools.modbus.client import PyModbusClient as ModbusClient
from iotools.modbus.client import ModbusTkClient as ModbusClient
from iotools.cli.command import BaseCommand
from iotools.exceptions import CommandError
from optparse import make_option
import json

FUNCTION_LIST = (
    "read_coil",
    "read_coils",
    "write_coil",
)

class Command(BaseCommand):
    
    usage = "%prog [options] HOST [value]"
    
    @classmethod
    def make_options(cls):
        options = [
            make_option("--port", "-p", type="int", default=502,
                        help="Modbus server TCP port (TCP port)"),
            make_option("--unit", "-u", type="int", default=1,
                        help="Modbus server unit number (default: %default)"),
            make_option("--function", "-f",
                        choices=FUNCTION_LIST,
                        help="Modbus function [%s]" % ("|".join(FUNCTION_LIST)),),
            make_option("--address", "-a", type="int",
                        help="I/O address"),
            make_option("--count", "-c", type="int", default=1,
                        help="I/O count (default: %default)"),
            make_option("--method", "-m", default="tcp",
                        choices=("tcp", "ascii", "rtu", "binary"),
                        help="Modbus method [tcp|ascii|rtu|binary] (default: %default)"),
            make_option("--baudrate", "-b", type="int", default=115200,
                        help="serial baudrate (default: %default)"),
            make_option("--parity", "-P", default="E",
                        help="Serial parity [Even|Odd|None] (default: %default)"),
            make_option("--pdu", "-0", dest="pdu_addressing", action="store_true", default=False,
                        help="PDU addressing (first ref is 0 instead of 1)")

        ]
        return BaseCommand.make_options(*options)
    
    @property
    def client(self):
        if getattr(self, "_client", None) is None:
            raise RuntimeError("Modbus client not defined yet")
        return self._client
    
    def handle(self):
        
        host = self.args[0]
        parity = self.options.parity[0].upper()
        kwargs = {
            "parity": parity,
        }
        for name in ('method', 'stopbits', 'bytesize', 'baudrate', 'timeout'):
            try:
                kwargs[name] = getattr(self.options, name)
            except AttributeError:
                pass
        client = ModbusClient(host, **kwargs)
        
        funcname = self.options.function
        try:
            value = self.args[1]
        except IndexError:
            value = None
        address = self.options.address
        count = self.options.count
        
        if self.options.pdu_addressing:
            address = address - 1
        
        if funcname == "read_coils":
            res = client.read_coils(address, count)
        elif funcname == "write_coil":
            assert value is not None
            if isinstance(value, basestring) and value.lower() in ("0", "false", "off"):
                value = False
            res = client.write_coil(address, value)
        else:
            raise CommandError("Unknown function: %s" % funcname)
        
        json.dump(res, self.stdout)
        self.stdout.write("\n")
    
def main():
    Command.run_from_argv()
    
if __name__ == "__main__":
    main()