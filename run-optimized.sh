#!/bin/bash

#OPTIMIZE=
OPTIMIZE=-OO

cd src
PIDS=()

echo Launching HelloPublisher
python $OPTIMIZE -m optimized.HelloPublisher --master &
PIDS+=($!)

echo Launching WorldPublisher
python $OPTIMIZE -m optimized.WorldPublisher &
PIDS+=($!)

echo Launching HelloWorldSubscriber
python $OPTIMIZE -m optimized.HelloWorldSubscriber &
PIDS+=($!)

if [ -z "$OPTIMIZE" ] ; then
   # Pendant 4 secondes, les publications de HelloPublisher et WorldPublisher
   # seront filtrées car il n'existe pas de consommateur. 
   sleep 4
fi

echo Launching TimePublisher
python $OPTIMIZE -m optimized.TimePublisher &
PIDS+=($!)
# A présent plus aucun filtrage n'est appliqué car toutes les publications
# ont un consommateur

trap ctrl_c INT

function ctrl_c() {
   for PID in "${PIDS[@]}"; do
      kill $PID
   done
   pgrep -a python | grep optimized
   exit 0
}

while true; do
   sleep 1
done
