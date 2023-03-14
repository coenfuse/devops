# standard dependencies
# ..

# custom import order
# ..

# thirdparty dependencies
# ..

# forward references for dependents
from lamina.plugins.outputs.mqtt.plugin import MQTT_Output_Service
# ..


# pkg const metadata
# ------------------------------------------------------------------------------
NAME = "OUTPUT - MQTT : "
INFO = "MQTT publishing service with error handling, encoding and buffering"
AUTH = "github.com/coenfuse"
VERS = ""
# ..

# pkg var metadata
# ------------------------------------------------------------------------------
__VER_MAJOR = 0
__VER_MINOR = 1
__VER_PATCH = 0
VERS = f"{__VER_MAJOR}.{__VER_MINOR}.{__VER_PATCH}"