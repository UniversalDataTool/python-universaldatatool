from .version import __version__
from .dataset import Dataset
from .sample import Sample
from .interface import Interface

DataSet = Dataset

__all__ = ["Dataset", "DataSet", "__version__", "Sample", "Interface"]
