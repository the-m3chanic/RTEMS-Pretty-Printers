import os 
import importlib 
from . import stdcxx

class BasePrettyPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        raise NotImplementedError("Subclasses should implement this!")

    def display_hint(self):
        return None

def load_printers():
    for file in os.listdir(os.path.join(os.path.dirname(__file__), 'rtems-printers')):
        if file.endswith(".py") and file != "__init__.py":
            file = file.replace(".py", "")
            module_name = f"rtems-printers.{file}"
            importlib.import_module(module_name)

def build_pretty_printer():
    pp = gdb.printing.RegexpCollectionPrettyPrinter("rtems_printers")
    pp.add_printer('Chain_Node', '^Chain_Node$', ChainNodePrinter)
    pp.add_printer('Chain_Control', '^Chain_Control$', ChainControlPrinter)
    pp.add_printer('_POSIX_Threads_Objects', '^_POSIX_Threads_Objects$', POSIXThreadsObjectsPrinter)
    return pp

load_printers()
# gdb.printing.register_pretty_printer(gdb.current_progspace(), build_pretty_printer())
