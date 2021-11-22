#!/bin/bash

. functions.sh

launch TimePublisher        delayed --observer --subs-share-delay 10
launch HelloPublisher       delayed            --subs-share-delay 20
launch WorldPublisher       delayed            --subs-share-delay 30

if [ -z "$OPTIMIZE" ] ; then
# Pendant 4 secondes, les publications de HelloPublisher et WorldPublisher
# seront filtrées car il n'existe pas de consommateur. 
   sleep 4
fi

launch HelloWorldSubscriber delayed            --subs-share-delay 40
# A présent plus aucun filtrage n'est appliqué car toutes les publications
# ont un consommateur

wait_ctrl_C_then_kill
