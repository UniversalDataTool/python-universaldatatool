from .open import open
from .open import get_udt_notebook_instance
from .edit_online import edit_online
from .edit_local import edit_local

display = open
edit = open
show = open

from .ProxiedFileSession import ProxiedFileSession
from .CollaborativeSession import CollaborativeSession
from .WebLocalFileProxyServer import WebLocalFileProxyServer
from .ZMQLocalFileProxyServer import ZMQLocalFileProxyServer
from .EmitterLocalFileProxyServer import EmitterLocalFileProxyServer
