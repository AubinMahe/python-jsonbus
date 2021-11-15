import time

from basic import json_bus
import settings


if __name__ == '__main__':
    bus   = json_bus.JSonBus('time-publisher', settings.MCAST_GROUP, settings.PORT)
    value = {'time': time.time()}
    while(True):
        t = time.time()
        if t - value['time'] > 0.9999:
            value['time'] = t
            bus.publish('time', value)
        time.sleep(0.020)
