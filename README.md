# RTEMS Kernel Pretty-printer integration

The layout of the `rtems` directory under `gdb/python` (in `rtems-tools`) would roughly be like how the `rtems` repository is organised over here. I am yet to work out some of the specifics (I will get to that part)

This is the current idea I have, along with the structure of RTEMS pretty-printers which we can host. 

**1. Base Pretty-Printer Class**

Create a base class that defines common methods and attributes for all pretty-printers. This class will act as an interface or template for specific structure pretty-printers. This can be defined in `base_printer.py` within `rtems`. 
```py
class BasePrettyPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        raise NotImplementedError("Subclasses should implement this!")

    def display_hint(self):
        return None
```

(I am yet to figure out the specifics of utilising the advantages of Inheritance in Python and use it to extend a single, commonly used API (such as `_Objects_Information`) across multiple classes. For now I've made it just so that the `to_string()` is defined by force). 

**2. Derived Pretty-Printer Classes for Specific Structures**

Each specific structure can have its own class that inherits from BasePrettyPrinter. These classes will implement the to_string method to provide the custom string representation for the specific structure.

Example:
```py

class ChainControlPrinter(BasePrettyPrinter):
    """Pretty print a Chain_Control."""

    def __init__(self, val):
        self.val = val

def to_string(self):
        head_node = self.val['Head']['Node']
        head_fill = self.val['Head']['fill']
        tail_node = self.val['Tail']['Node']
        tail_fill = self.val['Tail']['fill']

        empty_status = "empty" if self.is_empty() else "not empty"

        chain_nodes = self.walk_chain(head_node)
        
        return (f"Chain_Control(\n"
                f"    Head(\n"
                f"        Node(\n"
                ...
```

**3. Printer Registration Mechanism**

(This is one of the steps whose specifics I am to finalise on. There might be better approaches than the one I have taken here. I did not refer to the `libstdcxx` approach when writing these functions, so my next step would be to look at their approach to registering so many printers at once and see if I can borrow anything from there).

Create a function to register all the pretty-printers. This function will be called from the pprinter.py file. It can use a dictionary or a list to map structure names to their corresponding pretty-printer classes.

```py
def lookup_printer(val):
    type_name = str(val.type)
    if type_name in pretty_printers:
        return pretty_printers[type_name](val)
    return None

def register_rtems_printers(objfile):
    gdb.pretty_printers.append(lookup_printer)

pretty_printers = {
    'Chain_Control': ChainControlPrinter,
    'Watchdog_Control': WatchdogControlPrinter,
    # More structure-printer mappings to be added here
}
```

**4. Directory Structure**

Organize the pretty-printers in a directory structure that mirrors the nature of the solution:
```
rtems/
├── __init__.py
├── pprinter.py
├── stdcxx.py
├── base_printer.py
├── printers/
│   ├── __init__.py
│   ├── chain_control.py
│   ├── watchdog_control.py
│   └── # more printer modules...
```
- `base_printer.py`: Contains the `BasePrettyPrinter` class
- `printers`: Contains individual modules for each structure's pretty-printer 

**5. Inheritance and Reusability**

(This is also one of the steps whose specifics I am to figure out. If I am able to nicely get one example of, say, `_Objects_Information`'s methods being used elsewhere, I think this will be feeling more complete. Without that, the inheritance part looks unnecessary). 

For structures with common elements, create intermediate classes that encapsulate shared logic. For example:

```py
class ControlBlockPrinter(BasePrettyPrinter):
    def get_common_info(self):
        return f"start={self.val['start']}, end={self.val['end']}"

class ChainControlPrinter(ControlBlockPrinter):
    def to_string(self):
        common_info = self.get_common_info()
        return f"ChainControl({common_info}, other_field={self.val['other_field']})"
```

**6. Dynamic Import of Pretty-Printers**

To make the solution more flexible, we can dynamically load pretty-printers from the `printers/` directory. This way, adding a new pretty-printer involves simply dropping a new Python file in the `printers/` directory.

```py
import os
import importlib

def load_printers():
    for file in os.listdir(os.path.join(os.path.dirname(__file__), 'printers')):
        if file.endswith(".py") and file != "__init__.py":
            file = file.replace(".py", "")
            module_name = f"rtems.printers.{file}"
            importlib.import_module(module_name)

load_printers()
```

**7. Actual usage** 

In the `pprinter.py` script, all we would need to do is simply import and register the RTEMS pretty-printers. 

```py
from . import stdcxx
from .base_printer import register_rtems_printers

register_rtems_printers(None)
```

**8. For users to add their own printers** 

a. Create a new Python file in the `printers/` directory 
b. Define a class that inherits from the `BasePrettyPrinter` class 
c. Implement the `to_string` method (along with any others they would like) 
d. Add the structure name and the class name to the `pretty_printers` dictionary 


**Some notes**: 

1. I am still figuring out the specifics when it comes to importing between these various files/packages
2. There might be a more efficient way to register these various pretty-printers. I plan on taking a look at the `libstdcxx` approach to see if there's any elements I can borrow from that