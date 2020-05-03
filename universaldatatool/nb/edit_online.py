from ..dataset import Dataset
import zmq
from .Session import Session


def edit_online(constructor_dict, **kwargs):

    if isinstance(constructor_dict, Dataset):
        dataset = constructor_dict
    else:
        dataset = Dataset(constructor_dict, **kwargs)

    dataset.online_session = Session()
    dataset.online_session.start(dataset)

    return "https://universaldatatool.com?s={}".format(
        dataset.online_session.collab_session_id
    )
