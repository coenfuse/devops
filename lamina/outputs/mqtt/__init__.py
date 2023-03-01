# standard dependencies
# ..

# custom import order
# ..

# thirdparty dependencies
# ..

# forward references for dependents
from lamina.outputs.mqtt.service import MQTT_Output_Service
# ..


# pkg const metadata
# ------------------------------------------------------------------------------
NAME = "MQTTSRV_OUT"
INFO = "MQTT publishing service with error handling, encoding and buffering"
AUTH = "github.com/coenfuse"
VERS = ""
# ..

# pkg var metadata
# ------------------------------------------------------------------------------
__VER_MAJOR = 0
__VER_MINOR = 1
__VER_PATCH = 0
__VER_BUILD = 1

__IS_BETA_RELEASE = False
__BETA_BUILD = 0

if __IS_BETA_RELEASE:
    VERS = f"{__VER_MAJOR}.{__VER_MINOR}b-{__BETA_BUILD} (Build {__VER_BUILD})"
else:
    VERS = f"{__VER_MAJOR}.{__VER_MINOR}.{__VER_PATCH} (Build {__VER_BUILD})"