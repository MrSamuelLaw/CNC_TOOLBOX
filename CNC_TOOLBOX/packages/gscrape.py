#!/usr/bin/env python3

'''a gcode scraper that performs common functions
for gcode editing purposes. gscrape is desiged to
enable more effecient writing of macros for machine
programmers who wish to automate code formatting'''


class gscrape():

    def __init__(self):
        self._comment_flags = dict()

    def add_comment_flag(self, name, vals, status=True):
        '''sets the comment structure for the gcode
        to allow it to parse comments correctly

        arg1 <str> - comment char name
        arg2 <[(<char>, <int>)]> symbol, val
        arg3 <bool> status, true by default

        value = -1 if opening brace like "(" or 1 if closing like ")"
        value = 0 if text right is comment as in ";comment"
        '''

        vals.append(status)
        self._comment_flags[name] = vals

    def get_comment_flags(self):
        return self._comment_flags

    def _get_char_family(self, char):
        '''loops through and finds the family
        the comment char belongs to
        assigns none if the value char belongs
        to a non_enclosed family
        '''
        for key in self._comment_flags.keys():
            if self._comment_flags[key][-1]:  # prevents inactive keys
                for item in self._comment_flags[key][:-1]:
                    if 0 in item:
                        return None
                    elif char in item:
                        return key

    def _find_char(self, text, chars):
        '''finds characters in a given string
        '''
        if text is not None:
            for c in chars:
                if text.find(c) >= 0:
                    return True
        return False

    def _dict_from_char_tups(self):
        chars = dict()
        for item in self._comment_flags.values():
            if item[-1]:
                vals = {i[0]: i[1] for i in item[:-1]}
                chars.update(vals)
        return chars

    def sort_gcode(self, text):
        bools = [i[-1] for i in self._comment_flags.values()]
        if True not in list(bools):
            print('no comment flags active')
        else:
            # set up a list chars that indicate comments and families
            char_dict = self._dict_from_char_tups()
            fam_count = {key: 0 for key in self._comment_flags.keys()}
            sorted_script = list()

            # sort text line by line
            for num, line in enumerate(text.splitlines()):
                if len(line) == 0:
                    sorted_script.append(['\n', 'blank', num])
                code = ''
                capture = 0
                filter_flag = 0
                # sort line char by char
                for i, char in enumerate(line):
                    if char in char_dict.keys():
                        fam = self._get_char_family(char)
                        if fam is None:
                            # single char comment catcher
                            comment = line[i:]
                            comment = comment.strip()
                            if len(comment):
                                sorted_script.append([comment, 'comment', num])
                            capture = 2
                            # bracketed comment catcher
                        elif fam is not None:
                            fam_count[fam] += 1
                            if filter_flag == 0:  # entering a comment block
                                index = i
                                capture = -1
                                code = code.strip()
                                if len(code):
                                    sorted_script.append([code, 'code', num])
                                code = ''
                            filter_flag += char_dict[char]  # index the count
                            if filter_flag == 0:  # exiting a comment block
                                comment = line[index:i+1]
                                comment = comment.strip()
                                if len(comment):
                                    sorted_script.append([comment, 'comment', num])
                                capture = 1
                    # append char to code string based on condition
                    if capture == 0:  # not in a comment
                        code += char
                    elif capture == 1:  # just came out of a comment
                        capture = 0
                    elif capture == 2:  # unbracketed comment
                        break

                # capture code if end of line encountered
                if capture == 0:
                    code = code.strip()
                    if len(code):
                        sorted_script.append([code, 'code', num])

                # break on unmatched brackets
                for v in fam_count.values():
                    if v % 2 != 0:
                        msg = 'unmatched brackets line: '
                        return msg+str(num)

            # break every gcode command into it's own cell
            temp = []
            for item in sorted_script:
                if item[1] == 'code':
                    ilist = []
                    # find where the splits should be
                    for i, char in enumerate(item[0]):
                        if char.isalpha():
                            ilist.append(i)
                    ilist.append(len(item[0]))
                    # execute the splits
                    index = ilist[0]
                    for i in ilist[1:]:
                        temp.append([item[0][index:i].strip(), item[1], item[2]])
                        index = i
                elif item[1] == 'comment':
                    temp.append(item)
                elif item[1] == 'blank':
                    temp.append(item)
            sorted_script = temp
        return sorted_script

    def to_text(self, sorted_code):
        # initialize variables
        line_dict = {}
        text = ''
        for x in sorted_code:
            if x[2] not in line_dict.keys():
                line_dict[x[2]] = [x]
            else:
                line_dict[x[2]].append(x)
        for k in sorted(line_dict.keys()):
            line = [x[0] for x in line_dict[k]]
            if line[0] == '\n':
                text += ' '.join(line)
            else:
                text += '\n'+' '.join(line)
        return text
