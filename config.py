try:
    import tokens
    environ = tokens.environ
except ImportError:
    import os
    environ = os.environ
