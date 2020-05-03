from .camelify import camelify_dict, camelify


class Interface(object):

    param_names = [
        "type",
        "labels",
        "description",
        "language",
        "phraseBank",
        "transcriptionType",
        "surveyjs",
        "region",
        "regionTypesAllowed",
        "regionDescription",
        "multipleRegionLabels",
        "multipleRegions",
        "minimumRegionSize",
        "overlappingRegions",
        "multiple",
        "regionMinAcceptableDifference",
        "overlapAllowed",
    ]
    params = {}

    def __init__(self, constructor_dict={}, **kwargs):
        self.params = constructor_dict.copy()
        self.params.update(camelify_dict(kwargs))

    def to_dict(self, **kwargs):
        return self.params

    def __getitem__(self, key):
        return self.params[key]

    def __setitem__(self, key, v):
        self.params[key] = v

    def __getattr__(self, attr):
        if camelify(attr) in self.params:
            return self.params[camelify(attr)]
        if attr == "annotation":
            return None
        raise AttributeError(attr)

    def __setattr__(self, attr, v):
        camel_attr = camelify(attr)
        if camel_attr in self.param_names:
            self.params[camel_attr] = v
            return
        super(Interface, self).__setattr__(attr, v)
