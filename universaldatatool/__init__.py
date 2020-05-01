from .version import __version__
from .dataset import Dataset
from .sample import Sample
from .interface import Interface
from .nb.open import open, get_udt_notebook_instance

DataSet = Dataset

__all__ = ["Dataset", "DataSet", "__version__", "Sample", "Interface"]
