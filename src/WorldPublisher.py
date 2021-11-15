from cmdline          import cmdline_parser
from json_bus.factory import IJSonBus


class WorldPublisher:

    def __init__(self, args: object):
        self.__bus = IJSonBus.create(args.impl, 'WorldPublisher', args.mcast_group, args.port)
        self.__bus.subscribe('time', self.__publish)
        # Ici, contrairement à HelloPublisher, on va publier un
        # dictionnaire et non un objet
        self.__world = {'text': 'World!'}
        self.__bus.join()

    def __publish(self, topic: str, value: dict):
        assert topic == 'time'
        self.__world['time'] = value['time']
        self.__bus.publish('world', self.__world)

if __name__ == '__main__':
    WorldPublisher(cmdline_parser())
