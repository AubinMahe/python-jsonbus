from optimized import json_bus
import settings


class WorldPublisher:

    def __init__(self):
        self._bus = json_bus.JSonBus('WorldPublisher', settings.MCAST_GROUP, settings.PORT)
        self._bus.subscribe('time', self.publish)
        # Ici, contrairement à HelloPublisher, on va publier un
        # dictionnaire et non un objet
        self._world = {'text': 'World!'}

    def publish(self, topic: str, value: dict):
        assert topic == 'time'
        self._world['time'] = value['time']
        self._bus.publish('world', self._world)

    def run(self):
        self._bus.join()

if __name__ == '__main__':
    wp = WorldPublisher()
    wp.run()
