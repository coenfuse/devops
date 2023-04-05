# description of this module in 50 words
# ..


# standard imports
from enum import Enum
from threading import Thread
from time import sleep

# internal imports
# ..

# module imports
from lamina.utils import stdlog
from lamina.utils import typing

# thirdparty imports
from paho.mqtt.client import Client as paho_client
from paho.mqtt.client import MQTTMessage as paho_msg



# A simple, custom MQTT Message structure that is intended to be used by plugins
# that are going to use this client. This structure provides an easier interface
# for organizing MQTT data packets as opposed to paho.MQTTMessage that contains
# internal components in binary format. This structure also allows a simple ctor
# to convert paho.MQTTMessage into custom type 
# ------------------------------------------------------------------------------
class Message:
    qos = 0
    mid = 0
    topic = ""
    retain = ""
    payload = ""

    def __init__(self, msg: paho_msg = None, decode_type = "utf-8"):
        if msg is not None:
            self.mid     = int(msg.mid)
            self.qos     = int(msg.qos)
            self.topic   = str(msg.topic)
            self.retain  = bool(msg.retain)
            self.payload = msg.payload.decode(decode_type)


# A simple subscription object that is used by MQTTClient's dependents. This
# structure allows us to bundle subscription details along with handler callback
# and pass it around. This is especially helpful while intializing a plugin that
# uses this client and wishes to add subscriptions with custom handlers at time
# of configuration. The tag can be set as a unique ID for any message that is 
# received on this subscription 
# ------------------------------------------------------------------------------
class Subscription:
    qos = 0
    mid = 0
    tag = ""
    topic = ""
    callback = None


# ==============================================================================
# A simple MQTT Client that wraps over the paho client to support MQTT communic-
# ation facility, the class provides basic methods for connecting and disconnecting 
# from a broker, checking connection status, and subscribing to topics. The class
# also defines an internal enumerated list for handling error codes and exception
# handling. This client handles and supports connection with one broker only.
# ==============================================================================
class MQTTClient:

    # Internal enumerated list that facilitates in code-readability and easy
    # organization of error codes. This enum is NOT intended to be used outside
    # of this client. Any dependent component MUST process absolute values of
    # these enumeration units
    # --------------------------------------------------------------------------
    class ERC(Enum):
        SUCCESS = 0
        FAILURE = 1
        WARNING = 2
        EXCEPTION = 3
        NO_CONNECTION = 10


    # TODO : add support for userdata and use in cb_on_connect
    # TODO : Add interface for users to own callbacks for all mqtt events
    # 
    # Basic MQTTClient constructor, pass in the client-id (must be unique for a
    # broker) and whether you want a clean session with the broker. Pass an 
    # optional silent parameters that controls whether this client logs its 
    # runtime information or not. 
    # Not handling exceptions here since ctor can't return values, exceptions
    # are the only logicaly way I see to actually raise errors init errors
    # --------------------------------------------------------------------------
    def __init__(self, 
            client_id: str, 
            clean_session: bool,
            silent: bool = True
        ):
        self.__NAME  = "DRIVER - MQTT"

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

        self.__can_reconn_on_fail = False


    # The method attempts to connect to a MQTT broker with the given host, port,
    # and keep-alive time. It first checks if there is an existing connection, 
    # disconnects if there is, and then validates the input parameters. If all 
    # validations pass, it attempts to establish a connection and starts a loop 
    # to receive incoming messages. It returns the connection status as an 
    # integer value.
    # --------------------------------------------------------------------------
    def connect(self, 
            host: str, 
            port: int, 
            keep_alive_s: int, 
            reconnect_on_fail: bool = False, 
            reconnect_timeout_s: int = 10) -> int:
        status = self.ERC.SUCCESS
        
        if self.is_connected():
            status = self.ERC(self.disconnect(to_apply_force = True))

        if status == self.ERC.SUCCESS:
            try:
                typing.is_str(host, f"mqtt.{self.__id}.host", "and must be a non-zero length string")
                typing.is_int(port, f"mqtt.{self.__id}.port", "and must be a non-zero positive integer")
                typing.is_int(keep_alive_s, f"mqtt.{self.__id}.keep_alive_s", "and must be a non-zero positive integer")
                typing.is_bool(reconnect_on_fail, f"mqtt.{self.__id}.reconnect_on_fail", "and must be a boolean")
                typing.is_int(reconnect_timeout_s, f"mqtt.{self.__id}.reconnect_timeout_s", "and must be a positive integer")

            except Exception as e:
                stdlog.error(f"{self.__NAME} : [{self.__id}] exception -> {e}")
                status = self.ERC.EXCEPTION

        if status == self.ERC.SUCCESS:
            try:
                if self.__agent.connect(host, port, keep_alive_s) != 0:
                    status = self.ERC.FAILURE
            except Exception as e:
                stdlog.error(f"{self.__NAME} : [{self.__id}] exception -> {e}, check your network bruh!")
                status = self.ERC.NO_CONNECTION

        if status == self.ERC.SUCCESS:
            self.__agent.loop_start()
            sleep(0.5)

        if reconnect_on_fail:
            self.__agent.reconnect_delay_set(
                min_delay = reconnect_timeout_s,
                max_delay = reconnect_on_fail + 60)
            
            self.__can_reconn_on_fail = reconnect_on_fail

        return status.value


    # This method disconnects from the MQTT broker by stopping the network loop 
    # and disconnecting the client. The optional parameter to_apply_force determines
    # whether to forcefully stop the network loop or not. 
    # If the disconnect operation is successful, it returns ERC.SUCCESS, 
    # otherwise it returns self.ERC.FAILURE.
    # --------------------------------------------------------------------------
    def disconnect(self, to_apply_force: bool = True) -> int:
        if self.__agent.disconnect(reasoncode = 0) == 0:
            self.__agent.loop_stop(force = to_apply_force)          # blocking
            return self.ERC.SUCCESS
        return self.ERC.FAILURE.value


    # returns boolean signaling whether the client is connected with broker or not
    # --------------------------------------------------------------------------
    def is_connected(self) -> bool:
        return self.__agent.is_connected()

    
    # TODO : handle / log failed subscription requests
    # This method subscribes to a given MQTT topic with a specified Quality of 
    # Service (QoS) level and a callback function to be called when a message is
    # received on that topic. It checks if the client is connected to the MQTT 
    # broker, sends a subscription request, and adds a callback function to handle
    # the messages received. The method returns a status code indicating whether
    # the subscription was successful or not.
    # --------------------------------------------------------------------------
    def subscribe(self, req: Subscription) -> int:
        status = self.ERC.SUCCESS if self.is_connected() else self.ERC.NO_CONNECTION

        if status == self.ERC.SUCCESS:
            try:
                rc, mid = self.__agent.subscribe(req.topic, req.qos)
                stdlog.trace(f"{self.__NAME} : [{self.__id}] subscribe request sent with mid: {mid} for topic: {req.topic}, qos: {req.qos}")
                status = self.ERC.FAILURE if rc != 0 else self.ERC.SUCCESS
            except Exception as e:
                stdlog.error(f"{self.__NAME} : [{self.__id}] exception - {e}, while trying to subscribe to topic: '{req.topic}' & qos: '{req.qos}'")
                status = self.ERC.EXCEPTION

        if status == self.ERC.SUCCESS:
            self.__agent.message_callback_add(req.topic, req.callback)
        
        return status.value


    # This method handles unsubscribe requests from a client to a broker. It 
    # first checks if the client is connected or not, and if connected, sends an
    # unsubscribe request to the broker for the given topic. If the request is
    # successful, it removes the message callback associated with the topic.
    # The method returns a status code indicating whether the subscription was 
    # successful or not.
    # --------------------------------------------------------------------------
    def unsubscribe(self, req: Subscription) -> int:
        status = self.ERC.SUCCESS if self.is_connected() else self.ERC.NO_CONNECTION

        if status == self.ERC.SUCCESS:
            rc, mid = self.__agent.unsubscribe(req.topic)
            stdlog.trace(f"{self.__NAME} : [{self.__id}] unsubscribe request sent with mid: {mid} for topic: {req.topic}")
            status = self.ERC.FAILURE if rc != 0 else self.ERC.SUCCESS

        if status == self.ERC.SUCCESS:
            self.__agent.message_callback_remove(req.topic)

        return status.value


    # The publish method attempts to publish a message on a specified topic with
    # given quality of service and retain flag. If connected to the broker, it 
    # returns a warning if the message is not published, otherwise a failure. 
    # If not connected, it returns a no connection error.
    # --------------------------------------------------------------------------
    def publish(self, msg: Message) -> int:
        if self.is_connected():
            rc, mid = self.__agent.publish(msg.topic, msg.payload, msg.qos, msg.retain)
            stdlog.trace(f"{self.__NAME} : [{self.__id}] attempting publish on topic: {msg.topic} with qos: {msg.qos} and mid: {mid}")
            return self.ERC.WARNING.value if rc != 0 else self.ERC.SUCCESS.value
        else:
            return self.ERC.NO_CONNECTION.value


    # **************************************************************************
    # PRIVATE METHODS
    # **************************************************************************

    # the following callback function is invoked whenever the agent is successfully
    # establishes a connection with the broker.
    # - client_ref : reference to client object (need to type cast/hint before use)
    # - userdata   : client userdata that was init during client setup
    # - flags      : client connection flags that were init during connect request
    # - rc         : connection reason code (SUCCESS - 0) 
    # --------------------------------------------------------------------------
    def __cb_on_connect(self, client_ref, userdata, flags, rc):
        if not self.__is_silent:
            stdlog.debug(f"{self.__NAME} : [{self.__id}] connected to broker with rc: {rc}")


    # FIXME : this callback is called twice during unexpected disconnection
    #  
    # this callback function is invoked whenever the MQTTClient loses connection
    # or is manually disconnected. The RC is used to decide what type of connect
    # abortion is.
    # - client_ref : reference to client object (need to type cast/hint before use)
    # - userdata   : client userdata that was init during client setup
    # - rc         : disconnection reason code (SUCCESS - 0)
    # --------------------------------------------------------------------------
    def __cb_on_disconnect(self, client_ref, userdata, rc):
        if not self.__is_silent:
            msg = f"{self.__NAME} : [{self.__id}] disconnected from broker with rc: {rc}"
            if rc == 0:
                stdlog.debug(msg)
            else:
                stdlog.warn(msg)
                if self.__can_reconn_on_fail:
                    stdlog.debug(f"{self.__NAME} : [{self.__id}] reconnecting ...")


    # this callback function is invoked whenever the MQTTClient successfully
    # subscribes to a topic on the broker. This callback just logs SUBACK prompt.
    # --------------------------------------------------------------------------
    def __cb_on_subscribe(self, client, userdata, mid, granted_qos):
        if not self.__is_silent:
            stdlog.debug(f"{self.__NAME} : [{self.__id}] subscribe SUCCESS with mid: {mid} and granted qos: {granted_qos[0]}")


    # this callback function is invoked whenever the MQTTClient successfully
    # unsubscribes from a topic on the broker. Basically a UNSUBACK prompt.
    # --------------------------------------------------------------------------
    def __cb_on_unsubscribe(self, client, userdata, mid):
        if not self.__is_silent:
            stdlog.debug(f"{self.__NAME} : [{self.__id}] unsubscribe SUCCESS with mid: {mid}")


    # this callback function is invoked whenever the client successfully publishes
    # a message to a particular topic on the broker. Only logs the publish 'mid'
    # that can be used for cross-verification
    # --------------------------------------------------------------------------
    def __cb_on_publish(self, client, userdata, mid):
        if not self.__is_silent:
            stdlog.trace(f"{self.__NAME} : [{self.__id}] publish SUCCESS with mid: {mid}")


    # docs
    # --------------------------------------------------------------------------
    # def __cb_on_receive(self, client, userdata, msg: Message):
    #    if not self.__is_silent:
    #        stdlog.trace(f"{self.__NAME} : {self.__id} received message, topic - {msg.topic}, qos - {msg.qos}, payload - {msg.payload}")