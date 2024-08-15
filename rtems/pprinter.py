import stdcxx 
import gdb.printing 
import rtems_pprinters as rtems_library

def register_rtems_printers():
    gdb.printing.register_pretty_printer(
        gdb.current_objfile(), 
        rtems_library.build_pretty_printer()
        )

register_rtems_printers()