#!/usr/bin/env bash
BASE="/home/mi/repo"
SRC="python_demo/hadoop"
hadoop jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-*streaming*.jar \
-file ${BASE}/${SRC}/mapper.py    -mapper ${BASE}/${SRC}/mapper.py \
-file ${BASE}/${SRC}/reducer.py   -reducer ${BASE}/${SRC}/reducer.py \
-input /user/mi/test/* -output /user/mi/test/output