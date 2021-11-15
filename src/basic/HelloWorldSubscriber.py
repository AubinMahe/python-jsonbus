from basic import json_bus
import settings
import text


class HelloWorldSubscriber:
    '''
    Cette classe de démonstration effectue deux abonnements, le premier,
    'hello', manipule un dictionnaire, tandis que le second, 'world',
    utilise un objet de la classe text.Text.
    Les opérations réseau ainsi que les encodages de données sont
    réalisées dans la classe json_bus.JSonBus.
    '''

    def __init__(self):
        self.__hello = {'time': 0.0, 'text':''}
        self.__world = text.Text()
        self.__bus = json_bus.JSonBus('HelloWorldSubscriber', settings.MCAST_GROUP, settings.PORT)
        # On accepte de recevoir un dictionnaire
        self.__bus.subscribe('hello', self._hello)
        # Là, on précise qu'on souhaite recevoir  un objet de type text.Text
        classname = text.Text.__module__ + '.' + text.Text.__qualname__
        self.__bus.subscribe('world', self._world, classname)

    def __display_if_complete(self):
        hello = self.__hello['text']
        world = self.__world.text
        if hello and world:
            ts = (self.__hello['time'] + self.__world.time) // 2
            # On vérifie qu'on a bien un objet avec ses méthodes et pas
            # seulement un ensemble d'attributs issus du réseau.
            self.__world.set_time()
            print("%d: %s%s" % (ts, hello, world))
            self.__hello['text'] = None
            self.__world.text    = None

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
    hws = HelloWorldSubscriber()
    hws.run()
