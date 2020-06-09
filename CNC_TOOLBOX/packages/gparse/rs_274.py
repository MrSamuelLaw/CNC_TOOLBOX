#!/usr/bin/env python3

from math import isnan
from math import nan
from collections import deque


class rs274():
    '''
    A parser that takes rs274 gcode and generates a list
    with nested sublist with the following format
    [text, type, line_number]
    It is important to note the parser only checks the format
    of the commands for validation, i.e. if the comments are in
    brackets or after a semi-colon, and the codes are a single
    letter followed by an arbatrary amount of numbers.
    It DOES NOT check if the commands found are part of the
    rs274 standard, as many machines have their own small twists.
    '''

    def __init__(self):
        """
        sets up round brackets and semi-colon comment flags
        as well as any end of file symbols
        """
        self._comment_flags = {}
        self._add_comment_flag(['(', ')'], [-1, 1])
        self._add_comment_flag([';'], [nan])
        # create sets for fastest membership tests
        self.comment_flag_set = set(self._comment_flags.keys())
        self.eof_symbol = '%'
        self._math_operators = set(['-', '+', '.'])

    def _add_comment_flag(self, flag_list, val_list):
        """
        Takes a list of flags and a list of values
        and sets up comment flags
        args:
            flag_list: ['(',')'] <- example symbols
            val_list:  [-1, 1] <- example values
        Note, the rs274 standard does not take double
        characters for comment flags such as "//" and
        as such double char flags are not supported
        """
        if any([(len(x) > 1) for x in flag_list]):
            raise ValueError(
                'double character comment flags not supported'
            )

        self._comment_flags[flag_list[0]] = {
            'val': val_list[0], 'count': [0]
            # 'count': [0] simulates shared memory
        }
        if len(flag_list) == 2:
            self._comment_flags[flag_list[1]] = {
                'val': val_list[1],
                'count': self._comment_flags[flag_list[0]]['count']
            }

    def get_flag_count(self, flag_char):
        """
        takes a flag_char, index the count in the dict by
        the flag_char's value, and returns the current count
        """
        self._comment_flags[flag_char]['count'][0] += \
            self._comment_flags[flag_char]['val']
        return self._comment_flags[flag_char]['count'][0]

    def check_flag_counts(self, lnum):
        """
        args: lnum
        Checks to make sure all brackets are closed properly.
        If not closed, it will raise an error, and tell you
        what line number it was on
        """

        # used list comprehension as it is the fastest way
        # to check for 0 and nan values
        if any([
            (f['count'][0] != 0) and (not isnan(f['count'][0]))
            for
            f
            in
            self._comment_flags.values()
        ]):
            raise ValueError(f"unmatched brackets on line {lnum}")

    def reset_flag_counts(self):
        """
        prevents count errors if multiple parse_gcode calls
        are made using the same rs274 object
        """
        for flag in self._comment_flags.values():
            flag['count'][0] = 0

    def parse_gcode(self, text):
        """
        Takes text formatted as gcode and
        returns a list with every comment, blank line, and code
        Notes:
            * Branches have been optimized for speed based on
              how often they are called
            * The rule of one function, one task is ignored as
              function calls come with additional overhead
            * Using an iter allows the comment branch to loop it's
              self using the next() function
        """
        self.reset_flag_counts()
        gcode = deque()
        buff = ''
        # start looping over all the lines
        for lnum, line in enumerate(text.splitlines()):

            # BLANK LINE BRANCH
            if not line.strip():
                gcode.append(['', 'blank', lnum])

            # NON BLANK LINE BRANCH
            line_iter = iter(line)
            try:
                while line_iter:
                    item = next(line_iter)

                    # NUMBER BRANCH
                    if item.isnumeric() or item in self._math_operators:
                        buff += item

                    # ALPHA BRANCH
                    elif item.isalpha():
                        if buff and not buff[-1].isalpha():
                            gcode.append([buff, 'code', lnum])
                            buff = item
                        elif not buff:
                            buff += item
                        else:
                            raise ValueError(
                                'two sequentail characters found not in code'
                            )

                    # COMMENT BRANCH
                    elif item in self.comment_flag_set:
                        # flush the buffer
                        if buff:
                            gcode.append([buff, 'code', lnum])
                        buff = item
                        flag_count = self.get_flag_count(item)
                        while flag_count:  # start while loop
                            try:
                                item = next(line_iter)
                                if item in self.comment_flag_set:
                                    flag_count = self.get_flag_count(item)
                            except StopIteration:
                                flag_count = 0
                            else:
                                buff += item
                        # flush the buffer
                        gcode.append([buff, 'comment', lnum])
                        buff = ''
                        # check for mismatched brackets
                        self.check_flag_counts(lnum)

                    # SYMBOLS BRANCH
                    elif item == self.eof_symbol:
                        gcode.append([item, 'code', lnum])

                    # GARBAGE BRANCH
                    elif not item.isspace():
                        raise ValueError(
                            f'unrecognized symbol -> "{item}"'
                        )

            # iteration exception handling
            except StopIteration:
                if buff:
                    gcode.append([buff, 'code', lnum])
                    buff = ''

        return list(gcode)

    def to_text(self, gcode):
        """
        takes a list of parsed gcode generated
        using parse_gcode()
        and converts it back to text
        """
        # make sure it's in order
        gcode.sort(key=lambda x: x[2])
        # group by matches
        line, text = deque(), deque()
        for i, x in enumerate(gcode[1:]):
            # SAME LINE BRANCH
            if x[2] == gcode[i][2]:
                line.append(gcode[i][0])
            # NEW LINE BRANCH
            else:
                line.append(gcode[i][0])
                text.append(' '.join(line))
                line = deque()
        line.append(x[0])
        text.append(' '.join(line))
        return ('\n'.join(text))

    def _sequence(self, gcode):
        """
        takes a list of parsed gcode and ensures
        that each line is seqentially numbered, as sometimes
        when editing, lines get deleted or moved
        """
        gcode.sort(key=lambda x: x[2])
        # make sure lines are sequentially numbered
        gcode[0][2] = 0  # ensure it starts at zero
        for i, x in enumerate(gcode[1:]):
            if x[2] != gcode[i][2]:
                x[2] = (gcode[i][2] + 1)
        return gcode

    def insert_line(self, gcode, text, lnum):
        """
        args:
            gcode: parsed_gcode list
            text: string line of gcode
            lnum: int line at which to insert text line
        """
        # parse text
        text = self.parse_gcode(text)
        gcode = self._sequence(gcode)
        # find index
        index = 0
        for i, x in enumerate(gcode):
            if x[2] == lnum:
                index = i
                break
        # NOT LAST INDEX BRANCH
        if index != gcode[-1][2]:
            # shift everything at that index up
            for x in gcode[index:]:
                x[2] += 1
            # insert at index
            for x in text:
                x[2] = lnum
                gcode.insert(index, x)
        # LAST INDEX BRANCH
        else:
            for x in text:
                x[2] = (lnum + 1)
                gcode.append(x)
        # return gcode
        return gcode
