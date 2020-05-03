from ..dataset import Dataset
import zmq


def edit_online(constructor_dict, **kwargs):

    if isinstance(constructor_dict, Dataset):
        dataset = constructor_dict
    else:
        dataset = Dataset(constructor_dict, **kwargs)

    # dataset.
