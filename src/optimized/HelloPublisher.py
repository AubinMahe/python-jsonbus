from optimized import json_bus
import settings
import text


class HelloPublisher:

    def __init__(self):
        self._bus = json_bus.JSonBus('HelloPublisher', settings.MCAST_GROUP, settings.PORT)
        self._bus.subscribe('time', self.publish)
        # ici contrairement à WorldPublisher, on va publier un
        # objet et non un dictionnaire
        self._hello = text.Text('Hello, ')
        
    def publish(self, topic: str, value: dict):
        assert topic == 'time'
        self._hello.set_time(value['time'])
        self._bus.publish('hello', self._hello)

    def run(self):
        self._bus.join()

if __name__ == '__main__':
    hp = HelloPublisher()
    hp.run()
