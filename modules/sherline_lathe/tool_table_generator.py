from modules.gparse.rs_274_parser import rs274Parser


def generate(gcode: str) -> list:
    """Generates a list of linux cnc compatible tool
    table strings from gcode text"""

    parser = rs274Parser()             # create the parser object
    gcode = parser.parse_gcode(gcode)  # parse the gcode

    # collect the tool commands
    T_cmds = [x for x in gcode if x[1] == 'code' and x[0][0] == 'T']

    # generate a list of the unique tools
    tool_list = []
    [tool_list.append(T[0]) for T in T_cmds if T[0] not in tool_list]

    # generate list of tool table text strings
    tool_table = []
    [tool_table.append(f'{T} P{i} X+0.0 Z+0.0;') for i, T in enumerate(tool_list, start=1)]

    return tool_table
