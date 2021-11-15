import                       time

from cmdline          import cmdline_parser
from json_bus.factory import IJSonBus


if __name__ == '__main__':
    args  = cmdline_parser()
    bus   = IJSonBus.create(args.impl, 'time-publisher', args.mcast_group, args.port)
    value = {'time': time.time()}
    while(True):
        t = time.time()
        if t - value['time'] > 0.9999:
            value['time'] = t
            bus.publish('time', value)
        time.sleep(0.020)
