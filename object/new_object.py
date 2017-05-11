# encoding: utf-8

import sys

class Point(object):
  def __init__(self, x, y):
    self.x = x
    self.y = y

  @classmethod
  def make_object(cls, x, y):
    return cls(x, y)


if __name__ == '__main__':
  p1 = Point(2, 4)
  p2 = Point.make_object(4, 6)
  print sys.modules[__name__]
  g = globals()
  print 'ok'

