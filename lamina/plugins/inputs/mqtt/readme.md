# MQTT Input Plugin
- Version - 1.0
- Release Date - 16 April 2023
- Author - [github.com/coenfuse](www.github.com/coenfuse)

This MQTT Input plugin is a component of the LAMINA data collection application that allows you to collect data from a local or remote MQTT broker. With this plugin, you can subscribe to multiple topics on the broker and receive messages that are then tagged with a specified string. This tagging feature is particularly useful in routing data between different components of your data collection pipeline. The plugin supports multiple subscriptions, and you can specify the quality of service (QoS) for each subscription. Additionally, you can configure the plugin to automatically reconnect to the broker if the connection is lost.


## How to use?

To use the MQTT input plugin in Lamina, follow these steps:
1. Open the root lamina.toml configuration file for your Lamina instance.
2. In the inputs section, add a new input plugin with a unique name using the following naming convention: ```inputs.mqtt.<name>```. For example, ```inputs.mqtt.banana```
3. Fill the input plugin with required plugin parameters as mentioned in this sample [config.toml](config.toml).
4. Save the lamina.toml configuration file and restart your Lamina instance.
5. The MQTT input plugin should now be able connect to the MQTT broker and begin receiving messages based on the configured subscriptions. Messages will be forwarded to any outputs that are configured to receive messages from the plugins.


## Configuration

The following is the full configuration of this plugin in TOML format with complete documentation of each config parameter.
```
# MQTT Input plugin that can connect to a remote or local MQTT broker.
# Does not perform security checks requires authentication parameters yet.
# Can subscribe to several topics on the broker and collects messages on
# those topics which can then be tagged with a specified string. This client
# also reconnect to the broker if it loses connection with broker unnaturally
[inputs.mqtt.<name>]

    # the hostname or IP address of the remote broker
    host.ip = "localhost"

    # the network port of the server host to connect to. Defaults to 1883
    host.port = 1883

    # If True, the broker will remove all information about this client when
    # it disconnects. If False, the client is a persistent client and 
    # subscription information and queued messages will be retained when the 
    # client disconnects. Note that a client will never discard its own 
    # outgoing messages on disconnect.
    session.clean = true

    # Maximum period in seconds between communications with the broker. 
    # If no other messages are being exchanged, this controls the rate at 
    # which the client will send ping messages to the broker
    session.timeout_s = 10

    # If True, the client will retry to connect to the broker in case the
    # connection is lost unnaturally.
    session.reconnect_on_fail = false

    # When connection is lost, the client will initially wait initially for
    # specified timoout and double this time every attempt. The wait is 
    # capped at max_delay + 60. Once the client is fully connected the wait 
    # timer is reset to specified timeout.
    session.reconnect_timeout_s = 0
        
    # Specify the logging verbosity for this client, the logs will be
    # prefixed with string INPUT - [mqtt.<name>].
    # This logger will be using the Lamina's root logger and will dump its
    # output to same Stream / File as mentioned in the root logger. The level
    # mentioned here will be used for both File and Stream logging of data.
    # The logging levels are same as the root logger's
    # 0 - TRACE     [MOST DETAILED]
    # 1 - DEBUG
    # 2 - INFO
    # 3 - WARN
    # 4 - ERROR
    # 5 - CRITICAL  [MOST CONCISE]
    log.level = 0

    # Specify the list of subscriptions you want this client to make on the
    # broker and specify the QOS you want for that subscription. Furthermore,
    # you must also assign a tag that you wish the client to attach to the 
    # received message. This tagging is particularly useful in inter/intra 
    # plugin level data routing
    [[inputs.mqtt.<name>.subs]]
        topic = "lamina/topic/input/a"
        qos = 0
        tag = "mqta"

    [[inputs.mqtt.<name>.subs]]
        topic = "lamina/topic/input/b"
        qos = 1
        tag = "mqtb"

    [[inputs.mqtt.<name>.subs]]
        topic = "lamina/topic/input/c"
        qos = 2
        tag = "mqtc"
```

# Change Log
- v1.0 (16th April 2023)
    - Base version of MQTT collector
    - Can subscribe to multiple topics and have separate tags for each topics
    - The client can reconnect on losing connection from the broker
    - Dedicated and customizable logging handler
    - Does not support TLS certificates or username authentication before connection
    - Based on [paho-mqtt](https://pypi.org/project/paho-mqtt/) package for python