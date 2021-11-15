from builtins import staticmethod


class IJSonBus:

    @staticmethod
    def create(impl: str, role: str, group: str, port: int) -> object:
        impl        = 'json_bus.' + impl + '.json_bus.JSonBus'
        dot         = impl.rfind('.')
        module_path = impl[0:dot]
        class_name  = impl[dot+1:]
        module      = __import__(module_path, fromlist=[None])
        clss        = getattr(module, class_name)            
        instance    = clss(role, group, port)
        return instance

    def subscribe(self, topic: str, consumer, clazz: type = None):
        raise NotImplementedError("Abstract method")

    def publish(self, topic: str, value)->int:
        raise NotImplementedError("Abstract method")

    def join(self):
        raise NotImplementedError("Abstract method")

    def stop(self):
        raise NotImplementedError("Abstract method")
