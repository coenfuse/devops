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