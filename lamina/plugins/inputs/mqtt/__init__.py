# standard dependencies
# ..

# custom import order
# ..

# thirdparty dependencies
# ..

# forward references for dependents
from lamina.plugins.inputs.mqtt.service import MQTT_Input_Plugin
# ..


# pkg const metadata
# ------------------------------------------------------------------------------
NAME = "INPUT  - MQTT : "
INFO = "MQTT subscription service with error handling and buffering"
AUTH = "github.com/coenfuse"
VERS = ""
# ..

# pkg var metadata
# ------------------------------------------------------------------------------
__VER_MAJOR = 0
__VER_MINOR = 1
__VER_PATCH = 0
VERS = f"{__VER_MAJOR}.{__VER_MINOR}.{__VER_PATCH}"