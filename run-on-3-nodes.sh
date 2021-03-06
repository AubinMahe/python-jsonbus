#!/bin/bash

OPTIMIZE=$1

#scp -r src/* aubin@eve:/home/apps/jsonbus     >/dev/null
#scp -r src/* muriel@muriel:/home/apps/jsonbus >/dev/null

cd src

PIDS=()

#echo Launching TimePublisher on eve
#ssh aubin@eve "cd /home/apps/jsonbus && python $OPTIMIZE -m TimePublisher --impl optimized --master &" &

echo Launching HelloPublisher
python $OPTIMIZE -m HelloPublisher --impl optimized &
PIDS+=($!)

#echo Launching WorldPublisher on muriel
#ssh muriel@muriel "cd /home/apps/jsonbus && python $OPTIMIZE -m WorldPublisher --impl optimized &" &

if [ -z "$OPTIMIZE" ] ; then
# Pendant 4 secondes, les publications de HelloPublisher et WorldPublisher
# seront filtrées car il n'existe pas de consommateur. 
   sleep 4
fi

echo Launching HelloWorldSubscriber
python $OPTIMIZE -m HelloWorldSubscriber --impl optimized &
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
