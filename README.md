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
 - Master: Contains all the files associated with the project so far, some for linux, some for windows, the ui files for the QtDesigner 
   app, along with other misc files
 - CNC_TOOLBOX_Dist_Linux: The Linux version of the project with unnecessary files removed, including the ui files and the sync files
 - CNC_TOOLBOX_DIST_Windows: The windows version of the project with unnecessary files removed, and an .exe file that allows for the 
   program to  be used with an "open with" program on windows systems

