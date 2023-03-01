# decodes a raw string (commented) containing serialized json into lamina's
# internal processing format. Practically a dict now with no metadata.

# this module also provides functionality for serializing internal format into
# raw json string

# standard imports
import json as std_json

# internal imports
# ..

# module imports
from lamina.core.utils.error import ERC
from lamina.core.utils import stdlog

# thirdparty imports
import json5



# The current encoding and decoding implementations are very naive. And may even
# look redundant considering native support for json and external json5 support.
# But these parsers are kept separate to perform error handling, logging and
# additional boilerplate or functionality. Will be revised later.

def decode(msg: str) -> dict:
    try:
        return json5.loads(msg)
    except Exception as e:
        stdlog.warn(f"JSON_DEC : decode FAILURE because - {e}, for msg {msg}")
        return {}

def encode(data: dict) -> str:
    try:
        return json5.dumps(data)
    except Exception as e:
        stdlog.warn(f"JSON_ENC : encode FAILURE because - {e}, for data - {data}")
        return ""