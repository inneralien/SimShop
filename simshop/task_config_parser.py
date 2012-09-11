from ConfigParser import SafeConfigParser
import re


class TaskConfigParser(SafeConfigParser):
    """Recursive parsing of simulation test configuration files"""
    def __init__(self, defaults=None):
        SafeConfigParser.__init__(self, defaults=defaults)
        self.section_re = re.compile('\[(.*)\]')

    def read(self, config):
        SafeConfigParser.read(self, config)
        for sec in self.sections():
            tasks = self.get(sec,'tasks').split()
            expanded_tasks = " ".join(self.expand_tasks(tasks))
            self.set(sec,'tasks', expanded_tasks)

    def expand_tasks(self, tasks, level=0):
        """Takes a list of tasks and expands any [section] items"""
        if(level > 25):
            raise TooManyTaskLevelsError(level)
        ret_tasks = []
        for task in tasks:
            m = self.section_re.match(task)
            if(m):
                section = m.group(1)
                ret_tasks.extend(self.expand_tasks(self.get(section,'tasks').split(), level=level+1))
            else:
                ret_tasks.append(task)
        return ret_tasks

class TooManyTaskLevelsError(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

if __name__ == '__main__':
    c = TaskConfigParser()
    c.read('v.cfg')
    for sec in c.sections():
        print "%s" %sec
        print "    %s: %r" % (sec, c.get(sec, 'tasks'))
        print "    %s: %r" % (sec, c.get(sec, 'tasks').split())
