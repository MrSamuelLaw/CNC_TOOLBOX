# ABOUT
CNC_TOOLBOX is a light weight text editor that allows gcode programmers to
write their own macros for parsing and fixing errors before those errors
make it to the machine.

Currently, CNC_TOOLBOX comes equipped with an RS274 gcode parsing module,
and an automatic tool parser and uploader for LinuxCNC tool tables.

While the number of macros is currently few, the stand out feature of the
CNC_TOOLBOX is how easy it is to add new macros.
1. Simply code up the desired functionality in Python, along with any desired
   unit tests.
2. Declare the data structures that the QML front end should send to the
   Python backend in the form of Pydantic Models. See the filehandling and
   sherline_lathe modules for examples.
3. Code up the class that will act as the bridge between QML and Python, this
   is where your slots will go, and examples are available in both the
   file handling & sherline_lathe modules.
4. Write the most basic javascript to send the gcode and any other necessary
   text to the back backend, which can be placed in the main.qml file.

