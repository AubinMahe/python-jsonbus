from builtins import staticmethod
import               os
import               pathlib 
import               sys

from logger   import log_prefix_static, log_prefix


class IJSonBus:
    '''
    Cette classe couvre deux rôles : Interface et factory,
    par sa méthode statique create().
    
    Elle seule est connue des clients, les implémentations dans les
    sous-packages adoptent des comportements différents bien qu'offrant
    la même interface.
    '''

    @staticmethod
    def create(impl: str, role: str, group: str, port: int, ttl: int) -> object:
        impl        = 'json_bus.' + impl + '.json_bus.JSonBus'
        dot         = impl.rfind('.')
        module_path = impl[0:dot]
        class_name  = impl[dot+1:]
        module      = __import__(module_path, fromlist=[None])
        clss        = getattr(module, class_name)            
        instance    = clss(role, group, port, ttl)
        if __debug__:
            print("%s|new %s" % (log_prefix_static(IJSonBus, role), instance.__class__))
        return instance

    def subscribe(self, topic: str, consumer, clazz: type = None):
        raise NotImplementedError("Abstract method")

    def publish(self, topic: str, value)->int:
        raise NotImplementedError("Abstract method")

    def join(self):
        raise NotImplementedError("Abstract method")

    def stop(self):
        raise NotImplementedError("Abstract method")

    def _open_observer(self):
        if '--observer' in sys.argv:
            mdl         = self.__class__.__module__
            pckg        = mdl[0:mdl.rfind('.')]
            target_dir  = pathlib.Path(os.path.abspath(__file__)).parent.parent.parent
            target_file = os.path.join(target_dir, pckg + '.log')
            log         = open(target_file, "wt")
            if __debug__:
                print("Observer opened: '%s'" % target_file)
        else:
            log = None
        return log

    def _observe( self, log: object, role: str, publisher: object, length: int, topic: str, value: object ):
        if log:
            log.write(
                "%s|'%s'-->'%s', %d bytes from %s\n" % (log_prefix(self, role), topic, value, length, publisher))
            log.flush()
        elif __debug__:
            print(
                "%s|'%s'-->'%s', %d bytes from %s\n" % (log_prefix(self, role), topic, value, length, publisher))

    def _close_observer(self, log: object):
        if log:
            log.close()
