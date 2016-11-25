# encoding: utf-8

# !/usr/bin/env python

# sys.stdin.readline( )会将标准输入全部获取，包括末尾的'\n'，因此用len计算长度时是把换行符'\n'算进去了的，
# 但是raw_input( )获取输入时返回的结果是不包含末尾的换行符'\n'的

import sys

line1 = sys.stdin.readline()
line2 = raw_input()

print len(line1), len(line2)
