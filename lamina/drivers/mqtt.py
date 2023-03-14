# description of this module in 50 words
# ..


# standard imports
from enum import Enum
from time import sleep

# internal imports
# ..

# module imports
from lamina.utils import stdlog

# thirdparty imports
from paho.mqtt.client import Client as paho_client
from paho.mqtt.client import MQTTMessage as paho_msg


# ..
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


# ..
class Subscription:
    qos = 0
    mid = 0
    topic = ""
    callback = None


# ..
class ERC(Enum):
    SUCCESS = 0
    FAILURE = 1
    WARNING = 2
    EXCEPTION = 3

    NO_CONNECTION = 10


# ,,
# TODO : Rename Agent to Client
class Agent:

    # TODO : add support for userdata and use in cb_on_connect
    # TODO : Add interface for users to own callbacks for all mqtt events
    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self, client_id, clean_session, silent = True):
        self.__NAME  = "MQTT_DVR"
        self.__agent = paho_client(client_id, clean_session)
        self.__is_silent = silent
        self.__id = client_id

        self.__agent.on_connect = self.__cb_on_connect
        self.__agent.on_disconnect = self.__cb_on_disconnect
        self.__agent.on_subscribe = self.__cb_on_subscribe
        self.__agent.on_unsubscribe = self.__cb_on_unsubscribe
        self.__agent.on_publish = self.__cb_on_publish


    # TODO : docs
    # --------------------------------------------------------------------------
    def connect(self, host, port, keep_alive_s):
        self.__agent.connect(host, port, keep_alive_s)
        self.__agent.loop_start()
        sleep(0.5)


    # TODO : docs
    # --------------------------------------------------------------------------
    def disconnect(self, to_apply_force: bool = True):
        self.__agent.disconnect(reasoncode = 0)
        self.__agent.loop_stop(force = to_apply_force)


    # TODO : docs
    # --------------------------------------------------------------------------
    def is_connected(self):
        return self.__agent.is_connected()

    
    # TODO : handle / log failed subscription requests
    # TODO : docs
    # --------------------------------------------------------------------------
    def subscribe(self, req: Subscription):
        self.__agent.subscribe(req.topic, req.qos)
        self.__agent.message_callback_add(req.topic, req.callback)
        sleep(0.25)


    # TODO : docs
    # --------------------------------------------------------------------------
    def unsubscribe(self, req: Subscription):
        self.__agent.unsubscribe(req.topic)
        self.__agent.message_callback_remove(req.topic)
        sleep(0.25)


    # TODO : docs
    # --------------------------------------------------------------------------
    def publish(self, msg: Message) -> int:
        status = ERC.SUCCESS
        
        if self.is_connected():
            rc, mid = self.__agent.publish(msg.topic, msg.payload, msg.qos, msg.retain)
            status = ERC.SUCCESS if rc == 0 else ERC.FAILURE
        else:
            status = ERC.WARNING

        return status.value


    # **************************************************************************
    # PRIVATE METHODS
    # **************************************************************************

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
            stdlog.trace(f"{self.__NAME} : [{self.__id}] published SUCCESS with mid: {mid}")


    # docs
    # --------------------------------------------------------------------------
    def __cb_on_receive(self, client, userdata, msg: Message):
        if not self.__is_silent:
            stdlog.trace(f"{self.__NAME} : {self.__id} received message, topic - {msg.topic}, qos - {msg.qos}, payload - {msg.payload}")