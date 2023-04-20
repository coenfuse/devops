# MQTT Output Plugin
- Version - 1.0
- Release Date - 17 April 2023
- Author - [github.com/coenfuse](www.github.com/coenfuse)

This MQTT Output plugin is a component of the LAMINA data collection application that allows you to publish data to a local or remote MQTT broker. With the help of this plugin, you can publish your collected data to multiple MQTT topics simultaneously on the broker. Each topic can be assigned a list of permitted tags, since each data packet in Lamina is tagged (check input plugins), using which we can control / filter what messages will be published on what topic. This permitted tags allows this output plugin to perform inter-topic publish routing. Additionally, you can configure the plugin to automatically reconnect to the broker if the connection is lost.


## How to use?

To use the MQTT Output plugin in Lamina, follow these steps:
1. Open the root lamina.toml configuration file for your Lamina instance.
2. In the outputs section, add a new output plugin with a unique name using the following naming convention: ```outputs.mqtt.<name>```. For example, ```outputs.mqtt.hakuna```
3. Fill the output plugin with required plugin parameters as mentioned in this sample [config.toml](docs/config.toml).
4. Go the 'stream' config block at the end of lamina.toml and make sure to add the name of this newly created input plugin. For example,
```
    [stream]
        input = [mqtt.hakuna, ...]
        output = [...]
```
5. Save the lamina.toml configuration file and restart your Lamina instance.
6. The MQTT output plugin should now be able connect to the MQTT broker and will begin publishing configured messages based on the configured publish topics.


## Configuration

The following is the full configuration of this plugin in TOML format with complete documentation of each config parameter.
```
[outputs.mqtt.sample]

    # the hostname or IP address of the remote broker
    host.ip = "localhost"

    # the network port of the server host to connect to, defaults to 1883
    host.port = 1883

    # If True, the broker will remove all information about this client when it
    # disconnects. If false, the client is then a persistent client and queued
    # messges will be retained when the client disconnects. Note that a client
    # will never discard its outgoing messages on disconnect
    session.clean = true

    # Maximum period in seconds between communications with the broker. If no
    # other messages are being exchanged, this controls the rate at which the 
    # client will send ping messages to the broker
    session.timeout_s = 10

    # If True, the client will retry to connect to the broker in case the
    # connection is lost unnaturally
    session.reconnect_on_fail = false

    # When connection is lost, the client will initially wait for specified
    # timeout and double this every attempt. The wait capped at timeout + 60.
    # Once the client is fully connected the wait timer is reset to specified
    # timeout
    session.reconnect_timeout_s = 10
    
    # Specify the logging verbosity for this client, the logs will be prefixed
    # with string OUTPUT - [mqtt.<name>]
    # This logger will be using the Lamina's root logger and will dump its output
    # to same Stream / File as mentioned in the root logger. The level mentioned
    # here will be used for both File and Stream logging of data.
    # The available logging levels are same as for the root logger's
    # 0 - TRACE     [MOST DETAILED]
    # 1 - DEBUG
    # 2 - INFO
    # 3 - WARN
    # 4 - ERROR
    # 5 - CRITICAL  [MOST CONCISE]
    log.level = 1

    # Specify the list of topics you want this client to publish messages to and
    # specify QOS and retention status for that publish. Furthermore, you must
    # also assign a list of unique permitted tags for publish. Any outbound data
    # packet that contains the specified permeable tag will get published to that
    # topic only. This permission list is helpful for intra-topic routing.
    # An empty tags list defines no publish filtering, any outbound message with
    # any tag will be published on that topic.
    [[outputs.mqtt.sample.pubs]]
        topic = "lamina/send/a"
        qos = 0
        retain = true
        tags = ["lma", "lmb", "lmc"]

    [[outputs.mqtt.sample.pubs]]
        topic = "lamina/send/b"
        qos = 0
        retain = false
        tags = ["rma", "rha"]

    [[outputs.mqtt.sample.pubs]]
        topic = "lamina/send/all"
        qos = 0
        retain = false
        tags = []
```

## Release Notes
- v1.0 (17th April 2023)
    - Base version of MQTT publisher.
    - Can publish to multiple topics and support inter-topic routing with tags.
    - The client can reconnect on losing connection from the broker.
    - Dedicated and customizable logging handler.
    - Based on [paho-mqtt](https://pypi.org/project/paho-mqtt/) package for python.