# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import sys

class Score():
    """
    A dictionary version of Score to aid in recursive traversal
    """
    def __init__(self, name, parent=None):
        self.level = 0
        self.lasts = []
        self.data = {   'name'              : name,
                        'parent'            : parent,
                        'kids'              : [],
                        'score'             : 0,
                        'string_len'        : 0,    # Use for printing columns
                        'error_count'       : 0,
                        'warning_count'     : 0,
                        'incomplete_count'  : 0,
                        'not_run_count'     : 0,
                        'invalid_count'     : 0,
                        'pass'              : True,
                        'files'             : [],
                        'total_nodes'       : 0,
                        'status'            : 'PASS', # PASS,FAIL,INCOMPLETE,INVALID
                        'error_message'     : None,
                    }
        self.data['string_len'] = len(name) + 4
        self.tree_str = ""

    def __getitem__(self, key):
        if(key in self.data):
            return self.data[key]
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if(key in self.data):
            self.data[key] = value
        else:
            raise KeyError

    def incError(self, file=None):
        if(file is not None):
            self['files'].append(file)
        self['pass'] = False
        self['status'] = 'FAIL'
        self['error_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incError()

    def incInvalid(self, file=None):
        self['pass'] = False
        self['status'] = 'INVALID'
        self['invalid_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incInvalid()

    def incIncomplete(self, error_message=None):
#        print self.data['error_message']
        if(error_message is not None):
            self.data['error_message'] = error_message
        self['pass'] = False
        self['status'] = 'INCOMPLETE'
        self['incomplete_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incIncomplete()

    def incNotRun(self, error_message=None):
#        print self.data['error_message']
        if(error_message is not None):
            self.data['error_message'] = error_message
        self['pass'] = False
        self['status'] = 'NOT RUN'
        self['not_run_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incNotRun()

    def incWarning(self, file=None):
        if(file is not None):
            self['files'].append(file)
        self['warning_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incWarning()

    def increment(self):
        self['score'] += 1
        if(self['parent'] is not None):
            self['parent'].increment()

    def add(self, name):
#        print "NAME:", name
        score = Score(name, self)
        self.data['kids'].append(score)
        self['total_nodes'] += 1
        if(self['parent'] is not None):
            self['parent']['total_nodes'] += 1
        return score

    def longestString(self, data=None, max_level=None):
        if(data is None):
            data = self.data
        string_length = len(data['name'])
        # Recurse through the children
        if((max_level is None) or (self.level < max_level)):
            for i in range(len(data['kids'])):
                self.level += 1
                ret = self.longestString(data['kids'][i], max_level=max_level)
                if(ret > string_length):
                    string_length = ret
                self.level -= 1
        return string_length


    def printTree(self, data=None, last=False, max_level=None, pad=0):
        if(data is None):
            data = self.data

        pad_length = len(data['name'])

        if(self.level not in self.lasts):
            self.lasts.append(self.level)

        # Lay out the tree pipes if necessary
        for i in range(1, self.level):
            if(i in self.lasts):
                self.tree_str += "|   "# % (lasts[i], i))
            else:
                self.tree_str += "    "# % (lasts[i], i))
            pad_length += 4

        # If the item is the tail of the branch it gets a ` instead of a |
        if(self.level != 0):
            if(last):
                self.tree_str += '`'
            else:
                self.tree_str += '|'
            pad_length += 1

        # All levels but the top get --
        if(self.level != 0):
            self.tree_str += '-- %s ' % (data['name'])
            pad_length += 4
        else:
            self.tree_str += '%s ' % (data['name'])
            pad_length += 1

        pad_length = pad - pad_length + 10
        if(data['status'] == 'PASS'):
            padding = ' ' + ' ' * pad_length
        else:
            padding = '<' + '-' * pad_length

        if(len(data['kids']) == 0):
            pass_msg = '%s [%s]' % (padding, colorize(data['status']))
        else:
            pass_msg = ''

        self.tree_str += "%s\n" % pass_msg

        # Remove branches that have ended
        if(self.level in self.lasts):
            if(last):
                self.lasts.remove(self.level)

        # Recurse through the children
        if((max_level is None) or (self.level < max_level)):
            for i in range(len(data['kids'])):
                last = (i == len(data['kids']) - 1)
                self.level += 1
                self.printTree(data['kids'][i], last, max_level=max_level, pad=pad)
                self.level -= 1

        return self.tree_str

    def printTally(self):
        str = ""
#        sys.stdout.write("\n")
#        str += "\n"
        variants_failed = 0.
        tests_failed = 0.
        tasks_failed = 0.
        for v in self['kids']:
            if(not v['pass']):
                variants_failed += 1
            for t in v['kids']:
                if(not t['pass']):
                    tests_failed += 1
                for task in t['kids']:
                    if(not task['pass']):
                        tasks_failed += 1

        total_scores = 0.
        total_failures = 0.
        total_passed = 0.
        for v in self['kids']:
            # if(no kids and didn't pass): increment failures count
            if(len(v['kids']) == 0):
                total_scores += 1
                if(not v['pass']):
                    total_failures += 1
                else:
                    total_passed += 1
            for t in v['kids']:
                if(len(t['kids']) == 0):
                    total_scores += 1
                    if(not t['pass']):
                        total_failures += 1
                    else:
                        total_passed += 1
                for task in t['kids']:
                    if(len(task['kids']) == 0):
                        total_scores += 1
                        if(not task['pass']):
                            total_failures += 1
                        else:
                            total_passed += 1


        tests_passed = self.test_count - tests_failed
        tasks_passed = self.task_count - tasks_failed
        if(self.test_count != 0):
            tests_percent_passed = float(tests_passed)/float(self.test_count)*100.
        else:
            tests_percent_passed = 0
        tests_percent_failed = 100. - tests_percent_passed

        if(self.task_count != 0):
            tasks_percent_passed = float(tasks_passed)/float(self.task_count)*100.
        else:
            tasks_percent_passed = 0
        tasks_percent_failed = 100. - tasks_percent_passed

#                print "Total Scores  : %d" % total_scores
        str+= "Passed      %d/%d (%.1f%%)\n" % (total_passed, total_scores, (total_passed/total_scores)*100.)
        str+= "Failed      %d/%d (%.1f%%)\n" % (total_failures, total_scores, (total_failures/total_scores)*100.)
        str+= "Invalid     %d\n" % (self['invalid_count'])
        str+= "Incomplete  %d\n" % (self['incomplete_count'])
        str+= "Not Run     %d\n" % (self['not_run_count'])
        str+= "Errors      %d\n" % (self['error_count'])
        str+= "Warnings    %d\n" % (self['warning_count'])

        return str

#TODO - Need to add colored output for Windows as well
if(sys.platform == 'win32'):
    colors = {  'FAIL'   : "",
                'PASS'   : "",
                'INCOMPLETE': "",
                'INVALID': "",
                'end'    : "",
            }
else:
    colors = {  'FAIL'   : "\033[91m",
                'PASS'   : "\033[92m",
                'INCOMPLETE': "\033[95m",
                'INVALID': "\033[95m",
                'NOT RUN': "\033[95m",
                'end'    : "\033[0m",
            }

def colorize(text, type=None):
    str = ""
    if(type is None):
        str += colors[text] + text + colors['end']
    else:
        str += colors[type] + text + colors['end']
    return str


if __name__ == '__main__':
    print colorize('FAIL')
    print colorize('PASS')
    print colorize('INCOMPLETE')
    print colorize('INVALID')
