from typing_extensions import final

from cmdline           import cmdline_parser
from json_bus.factory  import IJSonBus
from logger            import log_prefix
from text              import Text


class HelloWorldSubscriber:
    '''
    Cette classe de démonstration effectue deux abonnements, le premier,
    'hello', attend un dictionnaire, tandis que le second, 'world',
    attend un objet de la classe Text.
    Les opérations réseau ainsi que les encodages de données sont
    réalisées dans la classe json_bus.JSonBus.
    '''

    ROLE: final = 'HelloWorldSubscriber'
    
    def __init__(self, args: object):
        self.__hello = {'time': 0.0, 'text':''}
        self.__world = Text()
        self.__bus = IJSonBus.create(args.impl, HelloWorldSubscriber.ROLE, args.mcast_group, args.port)
        # On accepte de recevoir un dictionnaire
        self.__bus.subscribe('hello', self._hello)
        # Là, on précise qu'on souhaite recevoir  un objet de type text.Text
        self.__bus.subscribe('world', self._world, Text)

    def __display_if_complete(self):
        hello = self.__hello['text']
        world = self.__world.text
        if hello and world:
            print("%s|%d-%d: %s%s" %
                  (log_prefix(self, HelloWorldSubscriber.ROLE), self.__hello['time'], self.__world.time, hello, world))
            # On vérifie qu'on a bien un objet avec ses méthodes et pas
            # seulement les attributs de données.
            self.__world.set_time()
            self.__world.text    = None
            self.__hello['text'] = None

    def _hello(self, topic: str, value: dict):
        assert topic == 'hello'
        self.__hello = value
        self.__display_if_complete()

    def _world(self, topic: str, value: object):
        assert topic == 'world'
        self.__world = value
        self.__display_if_complete()

    def run(self):
        self.__bus.join()

if __name__ == '__main__':
    hws = HelloWorldSubscriber(cmdline_parser())
    hws.run()
