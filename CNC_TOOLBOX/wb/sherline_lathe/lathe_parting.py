#!/usr/bin/env python

from math import pi, floor


def d(msg, ovr=0):
    if False:
        print(msg)
    elif ovr:
        print(msg)


class lathe_parting():

    unit_dict = {"in": "G20", "mm": "G21"}
    units = None
    offset_list = ["G54", "G55", "G56", "G57", "G58", "G59"]
    _offset = None
    _work_plane = "G18"  # G18 is the xz plane which is a constant on a lathe
    _eof_list = ["M2", "M30"]  # End Of File
    _pass_depth = None
    _feed = None

    def part(self, unit, surface_speed, diameter, feedrate):
        self._set_units(unit)
        self._set_surface_speed(surface_speed),
        self._set_diameter(diameter)
        self._set_initial_feedrate(feedrate)

        # rpm = surface_speed/circumference
        rpm = self._surfspeed/(pi*self._dia)
        start_point = -0.05  # inches
        rad = self._dia*0.5
        ring = 1/30  # each slice is 1/30" thick slice is keyword
        ratio = self._surfspeed/self._feed
        whole_slice = floor(rad/ring)

        gcode = "(Parting Script)\n"
        gcode += "G18 G20 G55 G97\n"  # Safetly line
        gcode += "(MSG, please load parting tool)\nM0\n"
        gcode += "(MSG, please set rpm to {0:.1f})\nM0\n".format(rpm)
        gcode += "G94\n"  # Set feed mode to in/min
        gcode += "G00 X0.05\n"  # Back off 1/20"

        for i in range(1, whole_slice):
            feed = (rpm*2*pi*(rad - (i*ring)))/ratio
            if feed > 0.0022:
                gcode += "G01 X{0:.4f} F{1:.4f}\n".format((-i*ring), feed)
            else:
                gcode += "G01 X{0:.4f} F0.0022\n".format((-i*ring))

        gcode += "G01 X{0:.4f} F0.0022\n".format(-(rad+.04))  # overcut
        gcode += "G01 X0.05 F30.0\n"  # retract
        # append the end of file lines
        gcode += self._eof_list[0] + ' (delete if not at end of of script)'
        gcode += '\n% (delete if not at end of script)\n'
        return gcode
        d(gcode)

    def _set_surface_speed(self, surface_speed):
        self._surfspeed = surface_speed

    def _set_units(self, units):
        if units.lower() not in self.unit_dict.keys():
            d("unit options are in or mm")
        else:
            self._units = units.lower()
            d("units set to {}".format(self._units))

    def _set_initial_feedrate(self, feed):
        if self._units == 'mm':
            self._feed = feed/25.4
        elif self._units == 'in':
            self._feed = feed
        else:
            return "units not set"

    def _set_diameter(self, diameter):
        if self._units == 'mm':
            self._dia = diameter/25.4
        elif self._units == 'in':
            self._dia = diameter
        else:
            return "units not set"
