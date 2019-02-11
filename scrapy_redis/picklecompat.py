"""A pickle wrapper module with protocol=-1 by default."""
import lxml

try:
    import cPickle as pickle  # PY2
except ImportError:
    import pickle

import json
from .defaults import REDIS_ENCODING


def loads(s):
    # return pickle.loads(s)
    return json.loads(str(s, encoding=REDIS_ENCODING), encoding=REDIS_ENCODING)


class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return str(o, encoding=REDIS_ENCODING)

        if isinstance(o, lxml.etree._ElementUnicodeResult):
            pass

        return json.JSONEncoder.default(self, o)


def dumps(obj):
    # return pickle.dumps(obj, protocol=-1)
    return json.dumps(obj, ensure_ascii=False, cls=MyEncoder, skipkeys=True)
