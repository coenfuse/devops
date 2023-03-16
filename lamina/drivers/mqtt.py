# description of this module in 50 words
# ..


# standard imports
from enum import Enum
from time import sleep

# internal imports
# ..

# module imports
from lamina.utils import stdlog                          # will be removed later
from lamina.utils import typing

# thirdparty imports
from paho.mqtt.client import Client as paho_client
from paho.mqtt.client import MQTTMessage as paho_msg



# docs
# ------------------------------------------------------------------------------
class Message:
    qos = 0
    mid = 0
    topic = ""
    retain = ""
    payload = ""

    def __init__(self, msg: paho_msg = None):
        if msg is not None:
            self.mid     = int(msg.mid)
            self.qos     = int(msg.qos)
            self.topic   = str(msg.topic)
            self.retain  = bool(msg.retain)
            self.payload = msg.payload.decode("utf-8")


# docs
# ------------------------------------------------------------------------------
class Subscription:
    qos = 0
    mid = 0
    topic = ""
    callback = None


# docs
# ------------------------------------------------------------------------------
class ERC(Enum):
    SUCCESS = 0
    FAILURE = 1
    WARNING = 2
    EXCEPTION = 3

    NO_CONNECTION = 10


# ==============================================================================
# TODO : docs
# ==============================================================================
class MQTTClient:

    # TODO : add support for userdata and use in cb_on_connect
    # TODO : Add interface for users to own callbacks for all mqtt events
    # TODO : Not handling exceptions here since it doesn't make sense to intialzie
    # the object with invalid values and since ctor can't return values, exceptions
    # are the only logicaly way I see.
    # --------------------------------------------------------------------------
    def __init__(self, 
            client_id: str, 
            clean_session: bool, 
            silent: bool = True
        ):
        self.__NAME  = "DRIVER_MQTT"

        if typing.is_str(client_id, "client_id", "and must be a non-zero length string"):
            self.__id = client_id

        if typing.is_bool(clean_session, "clean_session"):
            self.__agent = paho_client(client_id, clean_session)

        if typing.is_bool(silent, "silent"):
            self.__is_silent = silent

        self.__agent.on_connect = self.__cb_on_connect
        self.__agent.on_disconnect = self.__cb_on_disconnect
        self.__agent.on_subscribe = self.__cb_on_subscribe
        self.__agent.on_unsubscribe = self.__cb_on_unsubscribe
        self.__agent.on_publish = self.__cb_on_publish


    # TODO : docs
    # --------------------------------------------------------------------------
    def connect(self, host: str, port: int, keep_alive_s: int) -> int:
        status = ERC.SUCCESS
        
        if self.is_connected():
            status = ERC(self.disconnect(to_apply_force = True))

        if status == ERC.SUCCESS:
            try:
                typing.is_str(host, f"mqtt.{self.__id}.host", "and must be a non-zero length string")
                typing.is_int(port, f"mqtt.{self.__id}.port", "and must be a non-zero positive integer")
                typing.is_int(keep_alive_s, f"mqtt.{self.__id}.keep_alive_s", "and must be a non-zero positive integer")
            
            except Exception as e:
                stdlog.error(f"{self.__NAME} : [{self.__id}] exception -> {e}")
                status = ERC.EXCEPTION

        if status == ERC.SUCCESS:
            if self.__agent.connect(host, port, keep_alive_s) != 0:
                status = ERC.FAILURE

        if status == ERC.SUCCESS:
            self.__agent.loop_start()
            sleep(0.5)

        return status.value


    # TODO : docs
    # --------------------------------------------------------------------------
    def disconnect(self, to_apply_force: bool = True) -> int:
        if self.__agent.disconnect(reasoncode = 0) == 0:
            self.__agent.loop_stop(force = to_apply_force)          # blocking
            return ERC.SUCCESS
        return ERC.FAILURE


    # TODO : docs
    # --------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return self.__agent.is_connected()

    
    # TODO : handle / log failed subscription requests
    # TODO : docs
    # --------------------------------------------------------------------------
    def subscribe(self, req: Subscription) -> int:
        status = ERC.SUCCESS if self.is_connected() else ERC.NO_CONNECTION

        if status == ERC.SUCCESS:
            rc, mid = self.__agent.subscribe(req.topic, req.qos)
            stdlog.trace(f"{self.__NAME} : [{self.__id}] subscribe request sent with mid: {mid} for topic: {req.topic}, qos: {req.qos}")
            status = ERC.FAILURE if rc != 0 else ERC.SUCCESS

        if status == ERC.SUCCESS:
            self.__agent.message_callback_add(req.topic, req.callback)
        
        return status.value


    # TODO : docs
    # --------------------------------------------------------------------------
    def unsubscribe(self, req: Subscription) -> int:
        status = ERC.SUCCESS if self.is_connected() else ERC.NO_CONNECTION

        if status == ERC.SUCCESS:
            rc, mid = self.__agent.unsubscribe(req.topic)
            stdlog.trace(f"{self.__NAME} : [{self.__id}] unsubscribe request sent with mid: {mid} for topic: {req.topic}")
            status = ERC.FAILURE if rc != 0 else ERC.SUCCESS

        if status == ERC.SUCCESS:
            self.__agent.message_callback_remove(req.topic)

        return status.value


    # TODO : docs
    # --------------------------------------------------------------------------
    def publish(self, msg: Message) -> int:
        if self.is_connected():
            rc, mid = self.__agent.publish(msg.topic, msg.payload, msg.qos, msg.retain)
            stdlog.trace(f"{self.__NAME} : [{self.__id}] attempting publish on topic: {msg.topic} with qos: {msg.qos} and mid: {mid}")
            return ERC.FAILURE if rc != 0 else ERC.WARNING
        else:
            return ERC.NO_CONNECTION


    # **************************************************************************
    # PRIVATE METHODS
    # **************************************************************************

    # TODO : Implement reconnection logic: In case the MQTT client loses its 
    # connection to the broker, it's important to have a way to automatically 
    # reconnect. You could implement a reconnect oop with an exponential backoff
    # algorithm that gradually increases the delay between each attempt. This 
    # will reduce the load on the broker and increase the chances of a successful
    # reconnection.

    # docs
    # --------------------------------------------------------------------------
    def __cb_on_connect(self, client_obj, userdata, flags, rc):
        if not self.__is_silent:
            stdlog.debug(f"{self.__NAME} : [{self.__id}] connected to broker with rc: {rc}")


    # docs
    # --------------------------------------------------------------------------
    def __cb_on_disconnect(self, client, userdata, rc):
        if not self.__is_silent:
            msg = f"{self.__NAME} : [{self.__id}] disconnected from broker with rc: {rc}"
            stdlog.debug(msg) if rc == 0 else stdlog.error(msg)


    # docs
    # --------------------------------------------------------------------------
    def __cb_on_subscribe(self, client, userdata, mid, granted_qos):
        if not self.__is_silent:
            stdlog.debug(f"{self.__NAME} : [{self.__id}] subscribe SUCCESS with mid: {mid} and granted qos: {granted_qos[0]}")


    # docs
    # --------------------------------------------------------------------------
    def __cb_on_unsubscribe(self, client, userdata, mid):
        if not self.__is_silent:
            stdlog.debug(f"{self.__NAME} : [{self.__id}] unsubscribe SUCCESS with mid: {mid}")


    # docs
    # --------------------------------------------------------------------------
    def __cb_on_publish(self, client, userdata, mid):
        if not self.__is_silent:
            stdlog.trace(f"{self.__NAME} : [{self.__id}] publish SUCCESS with mid: {mid}")


    # docs
    # --------------------------------------------------------------------------
    def __cb_on_receive(self, client, userdata, msg: Message):
        if not self.__is_silent:
            stdlog.trace(f"{self.__NAME} : {self.__id} received message, topic - {msg.topic}, qos - {msg.qos}, payload - {msg.payload}")