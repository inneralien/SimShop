#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class HMS(object):
    def __init__(self, total_seconds):
        if(total_seconds < 0):
            self.negative = True
        else:
            self.negative = False
        self.total_seconds = abs(total_seconds)

    def __toHMS(self):
        """
        Converts total seconds to hours, minutes and seconds and returns a
        tuple of (h, m, s)
        """
        seconds = self.total_seconds%60.
        hours   = self.total_seconds/3600.
        temp_minutes = hours*60.
        minutes = temp_minutes%60.
        return (hours, minutes, seconds)

    def __str__(self):
        if(self.negative):
            return "-%.2dh %.2dm %.2ds" % self.__toHMS()
        else:
#            return "%.2d:%.2d:%.2d" % self.__toHMS()
            return "%.2dh %.2dm %.2ds" % self.__toHMS()

    def __add__(self, other):
        if(type(other) == type(0)):
            c = self.total_seconds + other
        else:
            c = self.total_seconds + other.total_seconds
        return HMS(c)

    def __sub__(self, other):
        if(self.total_seconds < other.total_seconds):
            c = other.total_seconds - self.total_seconds
        else:
            c = self.total_seconds - other.total_seconds
        return HMS(-c)


if __name__ == '__main__':
    print "3600 seconds : %s" % HMS(3600)
    print "  60 seconds : %s" % HMS(60)
    print "   1 seconds : %s" % HMS(1)
    print "  90 seconds : %s" % HMS(90)
    print "3690 seconds : %s" % HMS(3690)

    print HMS(3600) + 25
