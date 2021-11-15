#!/bin/bash

OPTIMIZE=
OPTIMIZE=-OO
cd src

PIDS=()
python $OPTIMIZE -m basic.TimePublisher &
PIDS+=($!)
python $OPTIMIZE -m basic.HelloPublisher &
PIDS+=($!)
python $OPTIMIZE -m basic.WorldPublisher &
PIDS+=($!)
python $OPTIMIZE -m basic.HelloWorldSubscriber &
PIDS+=($!)

trap ctrl_c INT

function ctrl_c() {
   for PID in "${PIDS[@]}"; do
      kill $PID
   done
   pgrep -a python | grep basic
   exit 0
}

while true; do
   sleep 1
done
