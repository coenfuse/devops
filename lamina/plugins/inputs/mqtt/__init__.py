# standard dependencies
# ..

# custom import order
# ..

# thirdparty dependencies
# ..

# forward references for dependents
from lamina.plugins.inputs.mqtt.plugin import MQTTInputPlugin
# ..


# pkg const metadata
# ------------------------------------------------------------------------------
NAME = "MQTT_INPLUG"
INFO = "A component of the LAMINA data collection application that allows you to collect data from a local or remote MQTT broker."
AUTH = "www.github.com/coenfuse"
VERS = ""
# ..

# pkg var metadata
# ------------------------------------------------------------------------------
__VER_MAJOR = 1
__VER_MINOR = 0
__VER_PATCH = 0
VERS = f"{__VER_MAJOR}.{__VER_MINOR}.{__VER_PATCH}"