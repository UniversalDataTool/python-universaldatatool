from ..dataset import Dataset
import zmq
from .CollaborativeSession import CollaborativeSession
from .WebLocalFileProxyServer import WebLocalFileProxyServer
from .ZMQLocalFileProxyServer import ZMQLocalFileProxyServer
from IPython.display import Markdown, display


def edit_online(constructor_dict, **kwargs):

    if isinstance(constructor_dict, Dataset):
        dataset = constructor_dict
    else:
        dataset = Dataset(constructor_dict, **kwargs)

    dataset.collaborative_session = CollaborativeSession()
    dataset.collaborative_session.start(dataset)

    url = "https://universaldatatool.com?s={}".format(
        dataset.collaborative_session.collab_session_id
    )

    display(
        Markdown(
            """## Edit your dataset at [universaldatatool.com?s={sid}](https://universaldatatool.com?s={sid})\nYou can share this link with others to collaborate.\n\nMake sure to call `Dataset.sync()` after you're done editing to load in your
    annotations.""".format(
                sid=dataset.collaborative_session.collab_session_id
            )
        )
    )

    return url
