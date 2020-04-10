#!/usr/bin/env python3


class gscrape():
    '''a gcode scraper that performs common functions
    for gcode editing purposes. gscrape is desiged to
    enable more effecient writing of macros for machine
    programmers who wish to automate code formatting'''

    def __init__(self):
        self._comment_flags = dict()
        self._math_operators = ['-', '+', '.']

    def add_comment_flag(self, name, vals, status=True):
        '''sets the comment structure for the gcode
        to allow it to parse comments correctly

        arg1 <str> - comment char name
        arg2 <[(<char>, <int>)]> symbol, val
        arg3 <bool> status, true by default

        value = -1 if opening brace like "(" or 1 if closing like ")"
        value = -2 if text right is comment as in ";comment"
        '''

        vals.append(status)
        self._comment_flags[name] = vals

    def get_comment_flags(self):
        return self._comment_flags

    def _is_comment_flag(self, item):
        for key in self._comment_flags.keys():
            for subitem in self._comment_flags[key][:-1]:
                if item in subitem:
                    return True
        return False

    def _get_flag_count(self, flag):
        for item in self._comment_flags.values():
            for subitem in item[:-1]:
                if flag in subitem:
                    return subitem[-1]
        return False

    def _sequence(self, gcode):
        gcode.sort(key=lambda x: x[2])
        # make sure lines are sequentially numbered
        gcode[0][2] = 0  # ensure it starts at zero
        for i, x in enumerate(gcode[1:]):
            if x[2] != gcode[i][2]:
                x[2] = (gcode[i][2] + 1)
        return gcode

    def sort_gcode(self, text):
        gcode = []
        buff, last = '', ''
        for lnum, line in enumerate(text.splitlines()):
            if not line.strip():
                gcode.append(['', 'blank', lnum])
            line_iter = iter(line)
            try:
                while line_iter:
                    item = next(line_iter)

                    # NUMBER BRANCH
                    if item.isnumeric() or item in self._math_operators:
                        buff += item
                    # ALPHA BRANCH
                    elif item.isalpha():
                        if last.isalpha():
                            raise DoubleLetter('two sequentail characters found not in code')
                        elif len(buff):
                            gcode.append([buff, 'code', lnum])
                            buff = item
                        else:
                            buff += item
                    # COMMENT BRANCH
                    elif self._is_comment_flag(item):
                        if buff:
                            gcode.append([buff, 'code', lnum])
                        buff = item

                        flag_count = self._get_flag_count(item)  # index flag count
                        while flag_count:  # start while loop
                            try:
                                item = next(line_iter)
                                if self._is_comment_flag(item):
                                    flag_count += self._get_flag_count(item)
                                buff += item
                            except StopIteration as e:
                                flag_count = 0
                                gcode.append([buff, 'comment', lnum])
                                buff = ''
                        gcode.append([buff, 'comment', lnum])
                        buff = ''

            # iteration exception handling
            except StopIteration as s:
                if buff:
                    gcode.append([buff, 'code', lnum])
                    buff = ''

        return gcode

    def to_text(self, gcode):
        # make sure it's in order
        gcode.sort(key=lambda x: x[2])
        # group by matches
        line, text = [], ''
        for i, x in enumerate(gcode[1:]):
            if x[2] == gcode[i][2]:
                line.append(gcode[i][0])
            else:
                line.append(gcode[i][0])
                text += ' '.join(line) + '\n'
                line = []
        line.append(x[0])
        text += ' '.join(line) + '\n'
        return text


    def insert_line(self, gcode, text, lnum):
        # parse text
        text = self.sort_gcode(text)
        gcode = self._sequence(gcode)
        # find index
        index = 0
        for i, x in enumerate(gcode):
            if x[2] == lnum:
                index = i
                break
        # shift everything at that index up
        for x in gcode[index:]:
            x[2] += 1
        # insert at index
        for x in text[::-1]:
            x[2] = lnum
            gcode.insert(index, x)
        # return gcode
        return gcode
