from builtins          import staticmethod
import                        io
import                        json
import                        socket
import                        struct
import                        sys
import                        threading

from typing_extensions import final

from json_bus.factory  import IJSonBus
from logger            import log_prefix


class JSonBus(IJSonBus):

    TOPICS_TOPIC: final = 'jsonbus.topics'

    def __init__(self, role: str, group: str, port: int):
        self.__role          = role
        self.__cont          = True
        self.__subscriptions = {}
        self.__is_master     = '--master' in sys.argv
        self.__remote_topics = set()
        self.__thread        = threading.Thread(name = role, target = self.__run)
        self.__mcast_group   = (group, port)
        self.__sock          = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mreq = struct.pack('4sL', socket.inet_aton(group), socket.INADDR_ANY)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.bind(('', port))
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        self.__sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.__thread.start()
        self.subscribe(JSonBus.TOPICS_TOPIC, self.__update_remote_topics)

    def subscribe(self, topic: str, consumer, clazz: type = None):
        self.__subscriptions[topic] = (consumer, (clazz.__module__ + '.' + clazz.__qualname__) if clazz else None)
        self.__remote_topics.add(topic)
        self.publish(JSonBus.TOPICS_TOPIC, self.__remote_topics)
    
    def __update_remote_topics(self, topic: str, topics: list):
        assert topic == JSonBus.TOPICS_TOPIC
        self.__remote_topics.update(topics)
        # In case of late joining, new participants has smaller sets of
        # topics, we have to resent the merged list.
        if self.__is_master and (self.__remote_topics - set(topics) != set()):
            self.publish(JSonBus.TOPICS_TOPIC, self.__remote_topics)

    def publish(self, topic: str, value)->int:
        '''
        Sérialise et émet sur le groupe UDP-Multicast un message
        associant le topic et sa valeur. 
        @param topic: le sujet de la publication
        @param value: soit un objet utilisateur, soit un dictionnaire
        @return: le nombre d'octets émit sur la socket
        '''
        if topic in self.__remote_topics:
            if isinstance(value, dict):
                pass
            elif isinstance(value, set):
                value = list(value)
            elif isinstance(value, object):
                value = value.__dict__
            serializer = io.StringIO()
            msg = {'topic': topic, 'payload': value}
            json.dump(msg, serializer)
            data = serializer.getvalue().encode()
            sent = self.__sock.sendto(data, self.__mcast_group)
            if __debug__:
                print("%s|topic '%s' published, %d bytes sent." % (log_prefix(self, self.__role), topic, sent))
        else:
            sent = 0
            if __debug__:
                print("%s|No subscriber to '%s' topic." % (log_prefix(self, self.__role), topic))
        return sent

    @staticmethod
    def __create_instance_from_dict(cls: str, value: dict) -> object:
        dot         = cls.rfind('.')
        module_path = cls[0:dot]
        class_name  = cls[dot+1:]
        module      = __import__(module_path, fromlist=[None])
        clss        = getattr(module, class_name)            
        instance    = clss()
        for k in value.keys():
            instance.__setattr__(k, value[k])
        return instance

    def __run(self):
        while(self.__cont):
            (data,_) = self.__sock.recvfrom(64*1024)
            deserializer = io.BytesIO(data)
            msg = json.load(deserializer)
            topic = msg['topic']
            if __debug__:
                print("%s|topic '%s' received." % (log_prefix(self, self.__role), topic))
            if topic in self.__subscriptions:
                value = msg['payload']
                (consumer, classname) = self.__subscriptions[topic]
                if classname:
                    value = JSonBus.__create_instance_from_dict(classname, value)
                consumer(topic, value)

    def join(self):
        self.__thread.join()

    def stop(self):
        self.__cont = False
        self.__sock.close()
