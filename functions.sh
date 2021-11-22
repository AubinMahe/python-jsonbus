#!/bin/bash
# This script has to be sourced

pgrep -a python | grep -E "Publisher|Subscriber"
if [ $? -ne 1 ] ; then
   echo "Des processus python Pub/Sub tournent déjà !"
   exit 1
fi

OPTIMIZE=$1
PIDS=()
cd src

function launch() {
   MAIN=$1
   shift
   echo python $OPTIMIZE -m $MAIN --impl $*
   python $OPTIMIZE -m $MAIN --impl $* &
   PIDS+=($!)
}
   
function ctrl_c() {
   for PID in "${PIDS[@]}"; do
      kill $PID
   done
   pgrep -a python | grep -E "Publisher|Subscriber"
   exit 0
}

function wait_ctrl_C_then_kill() {
   trap ctrl_c INT
   while true; do
      sleep 1
   done
}
