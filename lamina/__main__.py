# description about this module in 50 words
# ..


# standard imports
import signal
import sys

# internal imports
from lamina.app import Lamina
import lamina.metadata as meta

# module imports
from lamina.utils import stdlog
from lamina.utils.error import ERC

# thirdparty imports
# ..



# signal handlers
def sigint_handler(app_ref: Lamina):
    stdlog.debug(f"received interrupt SIGINT [{signal.SIGINT}]")
    app_ref.stop()

# ------------------------------------------------------------------------------
# BYTES, BANANA and ACTION
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    status = ERC.SUCCESS
    app = Lamina()

    def sgn_handler(signum, frame):
        if signum == signal.SIGINT: sigint_handler(app)
        # ..

    signal.signal(signal.SIGINT, sgn_handler)

    try:
        print("\n")
        status = app.start()

    except Exception as e:
        stdlog.critical(f"runtime exception occured: {e}")
        status = ERC.EXCEPTION
    
    finally:
        print(f"\n{meta.NAME} exited with code {status.value} [{status.name}]")
        sys.exit(status.value)