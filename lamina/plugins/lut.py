# This file is supposed to be the central lookup table for the Stream component
# to find appropriate plugin and assign it to its plugin variable.
# This saves us from updating the stream.py file itself with new import whenever
# a new plugin is added. THIS IS EXPERIMENTAL, will be removed if some better
# compile-time method is found.

# input plugin imports
from lamina.plugins.inputs.mqtt import MQTTInputPlugin
from lamina.plugins.inputs.http import HTTPInputPlugin
# ..

# output plugin imports
from lamina.plugins.outputs.mqtt import MQTTOutputPlugin
# ..


# ==============================================================================
# Plugins lookup table in a form of a python dictionary. All the keys are typed
# in alphabetically enclosed within groups depicting plugin types. It is recom-
# mended to maintain the consistency of this file. I've set the dictionary value
# to be a lambda that returns a new plugin object. This is just for making the
# dictionary calls analogous to a generator / factory function. Working so far.
# ==============================================================================
PLUGIN_LUT = {

    # input plugins
    # --------------------------------------------------------------------------
    "mqtt_in" : ( lambda: MQTTInputPlugin() ),
    "http_in" : ( lambda: HTTPInputPlugin() ),
    # ..

    # output plugins
    # --------------------------------------------------------------------------
    "mqtt_out" : ( lambda: MQTTOutputPlugin() )
    # ..
}