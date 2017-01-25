# encoding: utf-8

from pymongo import MongoClient
from multiprocessing import Process, Queue, Lock, Manager
import sys, os
from redis import Redis
import re
import logging

logging.basicConfig(level=logging.DEBUG, format='[PID:%(process)-5d THD:%(threadName)-5s] %(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S',
  filename='sh1.log',
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

# f = open(path+'/city/test.json')
# LINE = 304
manager = Manager()
WOKERNUM = 6
START = 0
END = 0
SIZE = 100
perLine = LINE/WOKERNUM
q = manager.Queue(WOKERNUM)
lock = manager.Lock()


def readDb():
  logging.info('process started!')
  arr =[]
  while True:
    with lock:
      arr = q.get()

    obj = {}
    # if len(arr) != SIZE:
    #   logging.info(arr)
    logging.info(arr[-1])
    arr = [re.compile('^' + i) for i in arr]
    result = wifi_coll.find({'loc_geohash': {'$in': arr}}, {'_id': 0})
    for v in result:
      # logging.info(v)
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


if __name__ == '__main__':
  position = 0
  l = []
  bStop = False
  for i in range(WOKERNUM):
    p = Process(target=readDb, args=())
    p.start()
    l.append(p)

  s = START * 0
  e = LINE * 9
  while True:
    if bStop:
      logging.info('end')
      break
    else:
      f.seek(s)

    if s + 9 * SIZE >= e:
      bytes = e - s
      bStop = True
    else:
      bytes = 9 * SIZE

    arr = []
    for index, line in enumerate(f):
      # logging.info('line number:%d', index)
      arr.append(line.strip('\n'))
      if len(arr) == SIZE:
        logging.info('line number:%d', index)
        logging.info('len: %d', len(arr))
        q.put(arr)
        del arr[:]
    q.put(arr)


    # lock.acquire()
    # q.put(arr)
    # lock.release()
    # s += bytes

  while q.empty():
    for i in l:
      i.terminate()

  logging.debug('#####')




