# standard dependencies
# ..

# custom import order
# ..

# thirdparty dependencies
# ..

# forward references for dependents
from lamina.plugins.outputs.mqtt.plugin import MQTT_Output_Plugin
# ..


# pkg const metadata
# ------------------------------------------------------------------------------
NAME = "MQTT_OUTPLUG"
INFO = "MQTT publishing plugin with error handling, encoding and rate control"
AUTH = "github.com/coenfuse"
VERS = ""
# ..

# pkg var metadata
# ------------------------------------------------------------------------------
__VER_MAJOR = 0
__VER_MINOR = 1
__VER_PATCH = 0
VERS = f"{__VER_MAJOR}.{__VER_MINOR}.{__VER_PATCH}"