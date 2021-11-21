#!/bin/bash

. functions.sh

launch TimePublisher        basic
launch HelloPublisher       basic
launch WorldPublisher       basic
launch HelloWorldSubscriber basic   --observer
wait_ctrl_C_then_kill
