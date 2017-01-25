#! /usr/bin/python
# encoding : utf-8

class A(object):
  def go(self):
    print "go A go!"

  def stop(self):
    print "stop A stop"

  def pause(self):
    print "pause A pause"


class B(A):
  def go(self):
    super(B, self).go()
    print "go B go"

class C(A):
  def go(self):
    super(C, self).go()
    print "go C go"

  def stop(self):
    super(C, self).stop()
    print "stop C stop"

# class D(B, C):
class D(B, A):
  def go(self):
    super(D, self).go()
    print "go D go"

  def stop(self):
    super(D, self).stop()
    print "stop D stop"

  def pasue(self):
    super(D, self).pause()
    print "pasue D pause"


class E(B, C):
  pass


a = A()
b = B()
c = C()
d = D()
e = E()

# a.go()
# b.go()
# c.go()
d.go()
# e.go()
#
# a.stop()
# b.stop()
# c.stop()
# d.stop()
e.stop()
#
# a.pause()
# b.pause()
# c.pause()
d.pause()
# e.pause()






