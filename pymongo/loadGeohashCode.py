# encoding: utf-8
# import pymongo
from pymongo import MongoClient
from multiprocessing import Process
import sys, os
from redis import Redis
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s [PID:%(process)-5d THD:%(threadName)-5s]', datefmt='%a, %d %b %Y %H:%M:%S',
  filename='sh.log',
  filemode='w')


conn = MongoClient('127.0.0.1', 27017, connect=False)
wifi_coll = conn['metok_core']['wifi_position']

redis_client = Redis(host='127.0.0.1', port=6379, db=0)


def cur_file_dir():
  path = sys.path[0]
  if os.path.isdir(path):
    return path
  elif os.path.isfile(path):
    return os.path.dirname(path)

path = cur_file_dir()
f = open(path+'/city/sh.json')
LINE = 26291109
WOKERNUM = 6
START = 0
END = 0
SIZE = 100
perLine = LINE/WOKERNUM


def read_file(start, end):
  s = start*9
  e = end*9
  # obj = {}
  f.seek(s)
  bStop = False
  bytes = 9 * SIZE

  while True:
    obj = {}
    if s + 9 * SIZE >= e:
      bytes = e - s
      bStop = True
    else:
      bytes = 9 * SIZE

    arr = f.read(bytes).strip('\n').split('\n')
    # arr = map(lambda i: '/^'+i+'/', arr)
    arrR = [re.compile('^'+i) for i in arr]
    result = wifi_coll.find({'loc_geohash': {'$in': arrR}}, {'_id': 0})
    for v in result:
      if v.get('loc_geohash') in obj:
        o = obj.get(v.get('loc_geohash'))
        if v.get('updateDate') > o.get('updateDate'):
          obj[v.get('loc_geohash')] = {'updateDate': v.get('updateDate'), 'imeiCount': v.get('imeiCount', 0)}
          redis_client.set(v.get('loc_geohash'), v.get('bssid'))
        elif v.get('imeiCount') > o.get('imeiCount'):
          obj[v.get('loc_geohash')] = {'updateDate': v.get('updateDate'), 'imeiCount': v.get('imeiCount', 0)}
          redis_client.set(v.get('loc_geohash'), v.get('bssid'))
      else:
        obj[v.get('loc_geohash')] = {'updateDate': v.get('updateDate'), 'imeiCount': v.get('imeiCount', 0)}
        redis_client.set(v.get('loc_geohash'), v.get('bssid'))

    s += bytes
    logging.info('已读行数:%d', s / 9)
    if bStop:
      logging.info('last one: %s', arr[len(arr)-1])
      return
    else:
      f.seek(s)

  logging.info('process id: %d end!', os.getpid())


if __name__ == '__main__':
  position = 0
  l = []
  for i in range(WOKERNUM):
    if i == WOKERNUM-1:
      START = position + perLine * i
      END = LINE
    else:
      START = position + perLine * i
      END = position + perLine * (i+1)

    logging.debug('start=%d, end=%d', START, END)
    p = Process(target=read_file, args=(START, END,))
    p.start()
    l.append(p)
    # p.join()

  for i in l:
    i.join()
  logging.debug('end')




