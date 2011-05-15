# Copyright 2010-2011, RTLCores. All rights reserved.
# http://rtlcores.com
# See LICENSE.txt

import sys
from builders.HMS import HMS

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
                        'run_time'          : HMS(0),
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
        if(error_message is not None):
            self.data['error_message'] = error_message
        self['pass'] = False
        self['status'] = 'INCOMPLETE'
        self['incomplete_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incIncomplete()

    def incNotRun(self, error_message=None):
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

    def add(self, name):
        score = Score(name, self)
        self.data['kids'].append(score)
        self['total_nodes'] += 1
        if(self['parent'] is not None):
            self['parent']['total_nodes'] += 1
        return score


if __name__ == '__main__':
    import pickle
    s = Score("Top Score")
    pkl_file = open('out.pkl', 'rb')
    data = pickle.load(pkl_file)
    pkl_file.close()

    longest = s.longestString(data)
    tree = s.printTree(data, pad=longest+4)
    tally = s.printTally(data)
    sys.stdout.write(tree)
    sys.stdout.write("\n")
    sys.stdout.write(tally)

