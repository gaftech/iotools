'''
Created on 8 avr. 2013

@author: gabriel
'''
import logging
from optparse import OptionParser, make_option
from iotools import __version__
from collections import namedtuple
import sys

class BaseCommand(object):

    arg_list = ()

    @classmethod
    def run_from_argv(cls):
        
        arg_list = cls.make_arg_list()
        arg_list_str = " ".join(("<%s>" % a) for a in arg_list)
        usage = "%%prog [options] %s" % (arg_list_str,)
        
        parser = cls.make_parser()
        options, arg_values = parser.parse_args()
        
#         arg_cls = namedtuple("Args", arg_list)
#         args = arg_cls(*arg_values)
        
        instance = cls(args=arg_values, options=options)
        instance.run()
    
    @classmethod
    def make_parser(cls, **kwargs):
        defaults = {
            "option_list": cls.make_options(),
        }
        defaults.update(kwargs)
        parser = OptionParser(**defaults)
        return parser
    
    @classmethod
    def make_options(cls, *extras):
        options = list(extras) 
        options.extend([
            make_option("--version", "-v", action="store_true", default=False,
                        help="show version and exit"),
        ])
        return options
    
    @classmethod
    def make_arg_list(cls):
        return []
    
    def __init__(self, args, options):
        self._args = args
        self._options = options
        
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        
    @property
    def args(self):
        return self._args
    
    @property
    def options(self):
        return self._options
    
    def run(self):
        
        if self.options.version:
            self.stdout.write("%s\r\n" % (__version__,))
        
        self.configure()
        self.handle()
        
    def configure(self):
        pass
    
    def handle(self):
        raise NotImplementedError
    
    
    
    

    
    