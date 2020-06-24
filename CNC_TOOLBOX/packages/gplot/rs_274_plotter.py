#!/usr/bin/env python3


class rs274Plotter():
    # psuedo code
    # remove all comments and blank lines from gcode
    # create a generator to yield the next move cmd or
    #   coordinate
    # have a function that recieves the yield value
    #   that calls one function if move or another if coordinate
    # plot the coordinates depending on if linear or circular move pattern

    def __init__(self):
        self.move_set = set(['G00', 'G01', 'G02', 'G03'])
        self.axis_set = set(['A', 'B', 'C', 'U', 'V', 'W', 'X', 'Y', 'Z', ])
        self.arc_set = set(['I', 'J', 'K', 'R'])

    def load_gcode(self, parsed_gcode):
        """gathers x, y, and z points from gcode
        parsed using gparse.rs_274.rs274"""

        self.gcode = [x for x in parsed_gcode if x[1] == 'code']
        for x in self.gcode:  # make sure all cmds are uppercase
            x[0] = x[0].upper()

    def generator(self, parsed_gcode):
        pass
