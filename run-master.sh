#!/bin/bash

. functions.sh

launch TimePublisher        master  --observer --master
launch HelloPublisher       master
launch WorldPublisher       master

if [ -z "$OPTIMIZE" ] ; then
# Pendant 4 secondes, les publications de HelloPublisher et WorldPublisher
# seront filtrées car il n'existe pas de consommateur. 
   sleep 4
fi

launch HelloWorldSubscriber master
# A présent plus aucun filtrage n'est appliqué car toutes les publications
# ont un consommateur

wait_ctrl_C_then_kill
