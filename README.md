# RTEMS Kernel Pretty-printer integration

The layout of pretty-printers under the `gdb/python/rtems` directory is pretty
much the same as what is suggested here in the GDB docs:
https://sourceware.org/gdb/current/onlinedocs/gdb.html/Writing-a-Pretty_002dPrinter.html 

I have a single file (`pprinter.py`) to import and register the `libstdcxx`
printers.

The `rtems_pprinters.py` acts as the file harbouring all the definitions of
classes for the various structures present in RTEMS. It also has a
`build_pretty_printer()` function, which generates a pretty-printer object with
all the printer classes, and the `register_rtems_printers()` function registers
them with the current objfile for GDB. 

The user (person using `GDB`) has to do nothing except make the change to their
`~/.gdbinit` file and that's it. 

For a developer who wants to add a new printer, all they have to do is define a
new class for it, and add it to the `printers`dictionary (Name of the structure
: Pretty printer class name), and that's all. 

Making these changes and placing them under `gdb/python/rtems`, and loading a
file into GDB, we see: 

```
suslaptop@Apollo:~/quick-start/my-printers$ arm-rtems6-gdb build/arm-rtems6-xilinx_zynq_a9_qemu/iostream.exe
GNU gdb (GDB) 14.2
Copyright (C) 2023 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "--host=x86_64-linux-gnu --target=arm-rtems6".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from build/arm-rtems6-xilinx_zynq_a9_qemu/iostream.exe...
RTEMS GDB Support
(gdb) info pretty-printer
global pretty-printers:
  builtin
    mpx_bound128
  libstdc++-v6
objfile /home/suslaptop/quick-start/my-printers/build/arm-rtems6-xilinx_zynq_a9_qemu/iostream.exe pretty-printers:
  rtems_printers
    Chain_Control
    Chain_Node
    _POSIX_Threads_Objects
(gdb)
```

