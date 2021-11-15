#!/bin/bash

OPTIMIZE=$1

cd src

PIDS=()

echo Launching TimePublisher
python $OPTIMIZE -m TimePublisher        --impl basic &
PIDS+=($!)

echo Launching HelloPublisher
python $OPTIMIZE -m HelloPublisher       --impl basic &
PIDS+=($!)

echo Launching WorldPublisher
python $OPTIMIZE -m WorldPublisher       --impl basic &
PIDS+=($!)

echo Launching HelloWorldSubscriber
python $OPTIMIZE -m HelloWorldSubscriber --impl basic &
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
