#!/bin/usr/env python

'''
python class that reads in user's nc files from solidworks cam
and edits them to be compatible with linuxCNC
'''


import os.path
from gscrape import gscrape


def d(msg, ovr=0):
    if False:
        print(msg)
    elif ovr:
        print(msg)


class sw_2_linuxCNC_formatter():

    _file_contents = None
    _unit_dict = {"in": "G20", "mm": "G21"}
    _units = None
    _offset_list = ["G54", "G55", "G56", "G57", "G58", "G59"]
    _offset = None
    _work_plane = "G18"  # G18 is the xz plane which is a constant on a lathe
    _eof_list = ["M2", "M30"]  # End Of File
    _spindle_mode = 'G97'  # G97 is const rpm mode

    def __init__(self):
        self.g = gscrape()
        self.g.add_comment_flag('round', [('(', -1), (')', 1)])
        self.g.add_comment_flag('semicolon_left', [(';', 0)])

    def format(self, contents, units, offset):
        self.load_contents(contents)
        self.set_units(units)
        self.set_offset(offset)
        self.delete_B_commands()
        self.insert_safety_line()
        self.fix_spindle_cmds()
        self.fix_T_commands()
        self.fix_eof()
        self.renumber_lines()
        self.insert_warnings()
        return self.get_text()

    def remove_line_numbers(self):
        self.remove_number_lines()
        return self.g.to_text(self._file_contents)

    def ftmin_to_inmin(self):
        pass

    def load_contents(self, contents):
        self._file_contents = self.g.sort_gcode(contents)

    def set_units(self, units):
        if units.lower() not in self._unit_dict.keys():
            d("unit options are in or mm")
            return -1
        else:
            self._units = units.lower()
            d("units set to {}".format(self._units))
            return None

    def set_offset(self, offset="G54"):
        pass
        if offset.upper() not in self._offset_list:
            d("offset is not valid")
            return -1
        else:
            self._offset = offset.upper()
            return None

    def _in_text(self, code, text):
        code = list(code)
        result = []
        for c in code:
            find = ([x for x in text if x[1] == 'code' and c in x[0]])
            if len(find):
                result.append(find)
        return result

    def _insert_line(self, code, lnum):
        # sort code to insert
        code = self.g.sort_gcode(code)
        # renumber code to insert
        for x in code:
            x[2] = lnum
        # renumber file contents
        for x in self._file_contents:
            if x[2] >= lnum:
                x[2] += 1
        # insert code
        for i, x in enumerate(self._file_contents):
            if x[2] < lnum:
                pass
            else:
                self._file_contents[i:i] = code
                break

    def insert_safety_line(self):
        # define the current safety line
        if self._units and self._offset is not None:
            safety_line = self._unit_dict[self._units]+' '
            safety_line += self._offset+' '
            safety_line += self._work_plane+' '
            safety_line += self._spindle_mode+' '
            safety_line = str(safety_line)
            # check for unit variations
            r = self._in_text(self._unit_dict.values(), self._file_contents)
            if len(r):
                safety_line = safety_line.replace(self._unit_dict[self._units], '')
            # check for offset variations
            r = self._in_text(self._offset_list, self._file_contents)
            if len(r):
                safety_line = safety_line.replace(self._offset, '')
            # check for constants in safety line
            r = self._in_text([self._work_plane], self._file_contents)
            if len(r):
                safety_line = safety_line.replace(self._work_plane, '')
            r = self._in_text([self._spindle_mode], self._file_contents)
            if len(r):
                if r[0][0][2] < 10:  # make sure the G97 is before any motor commands
                    safety_line = safety_line.replace(self._spindle_mode, '')
            # insert the appropriate safetly line on line 2
            self._insert_line(safety_line, 1)

    def delete_B_commands(self):
        del_list = []
        for i, x in enumerate(self._file_contents):
            if x[1] == 'code' and 'B' in x[0]:
                del_list.append(i)
        # do the deleting
        for i, d in enumerate(del_list):
            del self._file_contents[d-i]

    def fix_T_commands(self):
        for i, x in enumerate(self._file_contents):
            if 'T' in x[0] and x[1] == 'code':
                tool = list(x[0])
                while tool[1] == '0':
                    del tool[1]
                while '.' in tool:
                    tool.remove('.')
                x[0] = ''.join(tool)
                swap = ['M6', 'code', x[2]]  # gcode for tool swap
                oset = ['G43', 'code', x[2]]  # gcode to update tool offsets
                if self._file_contents[i+1][0] != 'M6':  # prevents duplicates
                    self._file_contents[i+1:i+1] = [swap, oset]

    def fix_eof(self):
        for i, x in enumerate(self._file_contents):
            if x[1] == 'code' and x[0] in self._eof_list:
                self._file_contents = self._file_contents[0:i+1]
                eof = ['%', 'code', x[2] + 1]
                self._file_contents.append(eof)

    def renumber_lines(self):
        self.remove_number_lines()
        # load up each line
        line_dict = {}
        oset = 0
        for x in self._file_contents:
            if x[2] not in line_dict.keys():
                line_dict[x[2]] = [x]
            else:
                line_dict[x[2]].append(x)
        self._file_contents.clear()
        for i, k in enumerate(sorted(line_dict.keys())):
            if line_dict[k][0][0] == '%':
                for x in line_dict[k]:
                    x[2] = i
                self._file_contents.extend(line_dict[k])
                break
            elif line_dict[k][0][1] != 'blank':
                self._file_contents.append(['N{}'.format(i+1+oset), 'code', i])
            else:
                oset -= 1
            for x in line_dict[k]:
                x[2] = i
            self._file_contents.extend(line_dict[k])

    def remove_number_lines(self):
        # find which items need to be deleted
        del_list = []
        for i, x in enumerate(self._file_contents):
            if x[1] == 'code' and 'N' in x[0]:
                del_list.append(i)
        # do the deleting
        for i, d in enumerate(del_list):
            del self._file_contents[d-i]

    def fix_spindle_cmds(self):
        # find the spindle commands
        for i, x in enumerate(self._file_contents):
            if x[1] == 'code' and 'S' in x[0]:
                # if found, insert a msg cmd string
                spd = x[0][1:]
                msg = f'(MSG, please set speed to {spd} RPM)'
                lnum = x[2]
                preline = [x[0] for x in self._file_contents if x[2] == lnum-1]
                if msg not in preline:
                    msg += 'M0'  # add in a forced pause
                    self._insert_line(msg, x[2])

    def insert_warnings(self):
        msg = '(MSG, warning G96 cmds not supported)'
        x = [x[0] for x in self._file_contents if x[1] == 'code']
        y = [x[0] for x in self._file_contents if x[1] == 'comment']
        if 'G96' in x and msg not in y:
            self._insert_line('(MSG, warning G96 cmds not supported)', 0)

    def make_tool_tbl(self):
        tool_tbl = []
        P = 1
        for x in self._file_contents:
            if x[1] == 'code' and 'T' in x[0]:
                tool = list(x[0])
                while tool[1] == '0':
                    del tool[1]
                while '.' in tool:
                    tool.remove('.')
                x[0] = ''.join(tool)
                tool_tbl.append([''.join(tool), P])
                P += 1
        return tool_tbl

    def get_text(self):
        text = gscrape().to_text(self._file_contents)
        return text

    def fpm_to_ipm(self, text):
        self._file_contents = self.g.sort_gcode(text)
        for x in self._file_contents:
            if x[1] == 'code' and 'F' in x[0]:
                feed = float(x[0][1:])  # convert to float
                feed = 12 * feed  # convert fpm to ipm here
                x[0] = 'F{0:.4f}'.format(feed)  # put back to
        # return as text
        return self.g.to_text(self._file_contents)
