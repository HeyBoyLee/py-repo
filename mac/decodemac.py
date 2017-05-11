# encoding: utf-8

from pymongo import MongoClient
from multiprocessing import Process, Queue, Lock, Manager
import sys, os
from redis import Redis
import re
import logging
import json

logging.basicConfig(level=logging.DEBUG, format='[PID:%(process)-5d THD:%(threadName)-5s] %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S',
  filename='mac.log',
  filemode='w')

def cur_file_dir():
  path = sys.path[0]
  if os.path.isdir(path):
    return path
  elif os.path.isfile(path):
    return os.path.dirname(path)

path = cur_file_dir()
f = open(path+'/mac_addr.txt')
of = open(path+'/output.json', 'w')
code = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
        'W', 'X', 'Y', 'Z']
len = 62
arr = []
d ={}
if __name__ == '__main__':
  for index, line in enumerate(f):

    mac = line.split('\t')[0]
    # print index
    if index < len:
      d[mac] = code[index]
    else:
      d[mac] = code[index/len-1]+code[index%len]
    arr.append(d)


of.write(json.dumps(d))
f.close()
of.close()

# print arr
