# CNC_TOOLBOX
 A workbench based gcode editor/cnc toolbox that can be adapted to individual machines
 CNC_TOOLBOX is built on the powerful PySide2 platform and is compatible with and has been 
 tested on windows10 and linux mint 19.1

# Workbench
 There are several reasons that a workbench based design was adopted.
  - The workbench concept allows machine programmers to create tools specific to their workflow using Python.
  - The workbenches are loaded at runtime, and deleted upon changing to different workbench, keeping memory freed and 
    the application running fast, even on lighter weight machines.
  - The workbench design pattern allows for a layer of abstraction allowing workbenches to be tested in isolation from the 
    rest of the program

# Branches
 Master - The current working version of the project. Just run setup.py using python3 and it will run correctly on Linux and  Windows
 Dev - The leading edge of the project where new features are developed and tested. Should work at any given time using setup.py.  
