# encoding: utf-8

# !/usr/bin/env python

# sys.stdin.readline( )会将标准输入全部获取，包括末尾的'\n'，因此用len计算长度时是把换行符'\n'算进去了的，
# 但是raw_input( )获取输入时返回的结果是不包含末尾的换行符'\n'的

import sys
import json

# line1 = sys.stdin.readline()
# line2 = raw_input()
#
# print len(line1), len(line2)


if __name__ == '__main__':
  f=open('/home/mi/repo/python_demo/input/districtID_all', 'r')
  s_code = ['110000', '120000', '310000', '500000', '710000', '810000', '820000']
  s_name = ['北京市','天津市','上海市','重庆市','台湾省','香港特别行政区','澳门特别行政区']
  cities = []
  districts = {}

  for line in f.readlines():
    arr = line.split()
    code = arr[0]
    name = arr[1].decode('utf-8').strip()
    if code in s_code or code[4:6] == "00":
      districts[code] = []
    else:
      c = code[0:2]+'0000'
      if c in s_code:
        districts[c].append(code)
      else:
        c = code[0:4]+'00'
        districts[c].append(code)

  print districts
  f.close()
  fw=open('/home/mi/repo/python_demo/input/districts.json', 'w')
  fw.write(json.dumps(districts))
  fw.close()



