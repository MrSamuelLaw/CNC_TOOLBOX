#!/bin/usr/env python

'''
python class that reads in user's nc files from solidworks cam
and edits them to be compatible with linuxCNC

positive return values indicate an operation was performed successfully
negative values indicate an operation failed

all return values are unique to help in identifing problems
'''


import os.path


'''
Patch Requests
    - fix error when attempting to change offset of safety line
        where the old safetly line stays in
'''


def d(msg, ovr=0):
    if False:
        print(msg)
    elif ovr:
        print(msg)


class sw_2_linuxCNC_formatter():

    _file_contents = None
    unit_dict = {"in": "G20", "mm": "G21"}
    _units = None
    offset_list = ["G54", "G55", "G56", "G57", "G58", "G59"]
    _offset = None
    _work_plane = "G18"  # G18 is the xz plane which is a constant on a lathe
    _eof_list = ["M2", "M30"]  # End Of File
    _spindle_mode = 'G97'  # G97 is const rpm mode

    def __init__(self):
        pass

    def format(self, contents, units, offset):
        self._load_contents(contents)
        self._set_units(units)
        self._set_offset(offset)
        self._delete_B_commands()
        self._insert_safety_line()
        self._fix_spindle_cmds()
        self._fix_T_commands()
        self._fix_eof()
        self._renumber_lines()
        return self._file_contents

    def remove_line_numbers(self):
        self._remove_number_lines()
        return self._file_contents

    def _load_file(self, path):
        if (os.path.exists(path)):
            if (os.path.splitext(path)[-1].lower() != ".nc"):
                d("file is not a .nc file")
                return -2
            else:
                inFile = open(path, 'r')
                self._file_contents = inFile.read()
                d("file read into memory")
                inFile.close()
                return 1
        else:
            d("path to file is corrupt or invalid")
            return -1

    def _load_contents(self, contents):
        self._file_contents = contents

    def _set_units(self, units):
        if units.lower() not in self.unit_dict.keys():
            d("unit options are in or mm")
            return -3
        else:
            self._units = units.lower()
            d("units set to {}".format(self._units))
            return 2

    def _set_offset(self, offset="G54"):
        pass
        if offset.upper() not in self.offset_list:
            d("offset is not valid")
            return -4
        else:
            self._offset = offset.upper()
            return 3

    def _insert_safety_line(self):
        # define the current safety line
        if(self._units and self._offset is not None):
            safety_line = ("{0} {1} {2} {3}".format(self.unit_dict[self._units],
                                                    self._offset,
                                                    self._work_plane,
                                                    self._spindle_mode))
            # check for unit variations
            for code in self.unit_dict.values():
                line = safety_line.replace(self.unit_dict[self._units], code)
                if line in self._file_contents:
                    self._file_contents = self._file_contents.replace(
                                               line, safety_line)
                    break
            # check for offset variations
            for code in self.offset_list:
                line = safety_line.replace(self._offset, code)
                if line in self._file_contents:
                    self._file_contents = self._file_contents.replace(
                                               line, safety_line)
            # no alternate versions of the safety line exist, insert
            # safety line on the second line
            if safety_line not in self._file_contents:
                contents = self._file_contents.splitlines()
                contents.insert(1, safety_line)
                self._file_contents = '\n'.join(contents)
                return 8
        else:
            d("units or offsets are not set")
            return -5

    def _delete_B_commands(self):
        self._parse_and_delete('B')
        return 4

    def _fix_T_commands(self):
        g = self._get_search_index
        content = ""
        for line in self._file_contents.splitlines():
            if len(list(g('T', line))) > 0:
                index = list(g('T', line))[0]
                for i in range(index, (len(line)-1)):
                    if line[i+1].isalpha():
                        tool = line[index:i]
                        line = line[::index]
                        break
                    elif i == (len(line)-2):
                        tool = line[index::]
                        line = line[0:index]
                msg = self._format_message('load tool number ' +
                                           tool[1::])
                content += (msg+'\nM0\n')
            content += (line.lstrip()+'\n')
        self._file_contents = content
        return 5

    def _fix_eof(self):
        for command in self._eof_list:
            self._delete_after_keyword(command, self._file_contents)
        self._file_contents += ('\n%')
        return 6

    def _renumber_lines(self):
        self._parse_and_delete('N')
        self._parse_and_delete('%')
        contents = ''
        offset = 0
        for i, line in enumerate(self._file_contents.splitlines(), start=1):
            if len(line):
                contents += 'N{0} '.format(i+offset)+line+'\n'
            else:
                contents += '\n'
                offset += -1
        self._file_contents = contents.rstrip()+'\n%'
        return 7

    def _remove_number_lines(self):
        self._parse_and_delete('N')
        return 9

    def _fix_spindle_cmds(self):
        g = self._get_search_index
        smf = -1  # spindle_mode_flag
        content = ""
        sliding_window = ['', '']
        for line in self._file_contents.splitlines():
            if len(list(g('G97', line))) > 0:
                smf = 1
            elif len(list(g('G96', line))) > 0:
                smf = 2
                # line = line.replace('G96', 'G97')
                warning = 'WARNING, G96 NOT SUPPORTED'
                msg = self._format_message(warning)
                if warning not in content:
                    content = msg+'\nM0\n' + content
            elif len(list(g('G50', line))) > 0:
                smf = 3
            if len(list(g('S', line))) > 0:
                if smf == 1:
                    index = list(g('S', line))[0]
                    for i in range(index, (len(line)-1)):
                        if line[i+1].isalpha():
                            spd = line[index:i]
                            break
                        elif i == (len(line)-2):
                            spd = line[index::]
                    msg = self._format_message('please set rpm to '
                                               + spd[1::] +
                                               ' RPM')
                    # check to ensure that it is not
                    # unneccessaryly duplicating a command
                    if msg and 'M0' not in "".join(sliding_window):
                        content += (msg+'\n'+'M0\n')
                elif smf == 2:
                    index = list(g('S', line))[0]
                    for i in range(index, (len(line)-1)):
                        if line[i+1].isalpha():
                            spd = line[index:i]
                            break
                        elif i == (len(line)-2):
                            spd = line[index::]
                    msg = self._format_message('please set rpm to '
                                               + spd[1::] +
                                               ' RPM')
                    if msg and 'M0' not in "".join(sliding_window):
                        content += (msg+'\n'+'M0\n')
                elif smf == 3:
                    index = list(g('S', line))[0]
                    for i in range(index, (len(line)-1)):
                        if line[i+1].isalpha():
                            spd = line[index:i]
                            break
                        elif i == (len(line)-2):
                            spd = line[index::]
                    line = line.replace('G50', '')
                    line = line.replace(spd, '')
                    content += line
                else:
                    d("WARNING feed set without spindle mode")
            content += (line.lstrip()+'\n')
            sliding_window[0], sliding_window[1] = sliding_window[1], line
        self._file_contents = content

    def _parse_and_delete(self, command_string):
        # set the command string to 'B' to delete all B commands
        # to delete subsets of commands set the command string to 'B90'
        # to only delete B90 commands, not any other B commands

        if command_string in self._file_contents:
            parsed_content = ""
            g = self._get_search_index
            for line in self._file_contents.splitlines():
                word_cnt = 0
                offset = 0
                index = list(g(command_string, line))
                while len(index) > word_cnt:
                    for i in index:
                        i -= offset
                        if i == (len(line)-1):
                            line = line[0:i]
                        else:
                            for j in range(i, (len(line)-1)):
                                if line[j+1].isalpha() or line[j+1] == '(':
                                    if j == i:
                                        word_cnt += 1
                                        break
                                    else:
                                        line = line[0:i]+line[(j+1)::]
                                        offset = (j+1-i)
                                        break
                                elif j == (len(line)-2):
                                    line = line[0:i]
                    index = list(g(command_string, line))
                parsed_content += (line+'\n')
            self._file_contents = parsed_content
        else:  # command string is not in file contents, nothing happens
            d("no {} commands found".format(command_string))

    def _get_search_index(self, command_string, line):

        window_size = len(command_string)
        bracket_count = 0

        for i in range(0, len(line)):
            if bracket_count:
                if line[i] == ')':
                    bracket_count += 1
                else:
                    pass
            elif line[i] == '(':
                bracket_count -= 1
            if not bracket_count:
                j = i + window_size
                if line[i:j] == command_string:
                    yield i

    def _delete_after_keyword(self, keyword, line):
        delete_index = list(self._get_search_index(keyword, line))

        if len(delete_index) > 1:
            d("multiple instances of {} found for\n"
              "delete after keyword command".format(keyword))
            return -4
        if len(delete_index) == 0:
            d("no instances of {} found for\n"
              "delete after keyword command".format(keyword))
            return -5

        delete_index[0] = delete_index[0] + len(keyword)
        self._file_contents = self._file_contents[0:delete_index[0]]
        return 5

    def _format_message(self, text):
        return("(MSG, {})".format(text))
