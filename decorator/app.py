# encoding: utf-8
from decorator.log import log, log1

# 相当于now = log(now)
@log
def now():
    print '2016-09-28'

# 相当于  now = log('execute')(now)
@log1('execute')
def now1():
    print '2017-09-28'


now()
print now.__name__
now1()
print now1.__name__


