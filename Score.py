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
                        'invalid_count'     : 0,
                        'pass'              : True,
                        'files'             : [],
                        'total_nodes'       : 0,
                        'status'            : 'PASS', # PASS,FAIL,INCOMPLETE,INVALID
                    }
        self.data['string_len'] = len(name) + 4

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
#        print 'Incrementing Error: "%s"' % self['name']
        if(file is not None):
            self['file'].append(file)
        self['pass'] = False
        self['status'] = 'FAIL'
        self['error_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incError()

    def incInvalid(self, file=None):
#        print 'Incrementing Invalid: "%s"' % self['name']
        self['pass'] = False
        self['status'] = 'INVALID'
        self['invalid_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incInvalid()

    def incIncomplete(self, file=None):
#        print 'Incrementing Incomplete: "%s"' % self['name']
        if(file is not None):
#            print "Adding file: %s" % file
            self['files'].append(file)
        self['pass'] = False
        self['status'] = 'INCOMPLETE'
        self['incomplete_count'] += 1
        if(self['parent'] is not None):
            self['parent'].incIncomplete()

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
                sys.stdout.write("|   ")# % (lasts[i], i))
            else:
                sys.stdout.write("    ")# % (lasts[i], i))
            pad_length += 4

        # If the item is the tail of the branch it gets a ` instead of a |
        if(self.level != 0):
            if(last):
                sys.stdout.write('`')
            else:
                sys.stdout.write('|')
            pad_length += 1

        # All levels but the top get --
        if(self.level != 0):
            sys.stdout.write('-- %s ' % (data['name']))
            pad_length += 4
#            sys.stdout.write('-- %s: %s\n' % (data['name'], pass_msg))
        else:
            sys.stdout.write('%s ' % (data['name']))
            pad_length += 1
#            sys.stdout.write('%s: %s\n' % (data['name'], pass_msg))

        pad_length = pad - pad_length + 10
        padding = ' ' * pad_length
        # Test failure precedence
        #   Invalid
        #   Incomplete
        #   FAIL based on error_count
        #   PASS
#        if(data['invalid_count'] > 0):
#            pass_msg = '%s- INVALID' % (padding)
#        elif(data['incomplete_count'] > 0):
#            pass_msg = '%s- INCOMPLETE' % (padding)
#        elif(data['error_count'] > 0):
#            pass_msg = '%s- FAIL' % (padding)
#        else:
#            pass_msg = '%s+ PASS' % (padding)

        if(self.level != 0):
            pass_msg = '%s %s' % (padding, data['status'])
        else:
            pass_msg = ''
#        if(data['pass']):
#            pass_msg = '%s+ PASS' % (padding)
#        else:
#            pass_msg = '%s- FAIL' % (padding)

        sys.stdout.write("%s\n" % pass_msg)

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


