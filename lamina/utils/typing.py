# TODO : docs
# ------------------------------------------------------------------------------
def is_bool(value, variable, msg = ""):
    if not isinstance(value, bool):
        raise TypeError(f"{variable} = {value} is of type '{type(value).__name__}', must be a boolean {msg}.")
    else:
        return True


# TODO : docs
# ------------------------------------------------------------------------------
def is_dict(value, variable, msg = ""):
    if not isinstance(value, dict):
        raise TypeError(f"{variable} = {value} is of type '{type(value).__name__}', must be a dictionary {msg}.")
    else:
        return True
    

# TODO : docs
# ------------------------------------------------------------------------------
def is_float(value, variable, msg = ""):
    if not isinstance(value, float):
        raise TypeError(f"{variable} = {value} is of type '{type(value).__name__}', must be a float {msg}.")
    else:
        return True
    

# TODO : docs
# ------------------------------------------------------------------------------
def is_int(value, variable, msg = ""):
    if not isinstance(value, int):
        raise TypeError(f"{variable} = {value} is of type '{type(value).__name__}', must be an int {msg}.")
    else:
        return True
    

# TODO : docs
# ------------------------------------------------------------------------------
def is_list(value, variable, msg = ""):
    if not isinstance(value, list):
        raise TypeError(f"{variable} = {value} is of type '{type(value).__name__}', must be a list {msg}.")
    else:
        return True
    

# TODO : docs
# ------------------------------------------------------------------------------
def is_str(value, variable, msg = ""):
    if not isinstance(value, str):
        raise TypeError(f"{variable} = {value} is of type '{type(value).__name__}', must be a str {msg}.")
    else:
        return True


'''

    Implement error handling: Currently, the publish() method only returns an 
    ERC status code, which doesn't provide enough information about the nature 
    of the error. You could add more specific error codes to the ERC enumeration, 
    such as NO_CONNECTION to indicate that there is no connection to the broker, 
    or TIMEOUT to indicate that the operation timed out. Additionally, you could 
    log the errors with more detail to make it easier to debug them.

    Improve the sleep timings: The sleep() calls in the connect(), subscribe(), 
    and unsubscribe() methods are hardcoded to a fixed delay of 0.25 seconds. 
    This may not be enough time for the client to establish a connection, 
    subscribe to a topic, or unsubscribe from a topic. You could adjust the sleep
    timings based on the response time of the MQTT broker, or use a more 
    sophisticated algorithm to determine the optimal delay time.

    Implement message persistence: By default, the MQTT broker only stores 
    messages in memory, which means that if the broker crashes or loses power, 
    all messages are lost. You could configure the client to use message 
    persistence, which stores messages on disk and ensures that they are not 
    lost in case of a broker failure. This can be done by setting the clean_session
    flag to False and specifying a client_id for the client.

    Implement quality of service (QoS): The publish() method currently doesn't 
    specify a QoS level for the message, which means that the message may be 
    lost if the client disconnects before the broker receives it. You could 
    implement QoS by setting the qos parameter to 1 or 2, which ensures that 
    the message is delivered at least once or exactly once, respectively.

'''