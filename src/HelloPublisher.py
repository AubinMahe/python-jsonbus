from cmdline          import cmdline_parser
from json_bus.factory import IJSonBus
from text             import Text


class HelloPublisher:

    def __init__(self, args: object):
        self.__bus = IJSonBus.create(args.impl, 'HelloPublisher', args.mcast_group, args.port)
        self.__bus.subscribe('time', self.publish)
        # ici contrairement à WorldPublisher, on va publier un
        # objet et non un dictionnaire
        self.__hello = Text('Hello, ')
        self.__bus.join()

    def publish(self, topic: str, value: dict):
        assert topic == 'time'
        self.__hello.set_time(value['time'])
        self.__bus.publish('hello', self.__hello)

if __name__ == '__main__':
    HelloPublisher(cmdline_parser())
