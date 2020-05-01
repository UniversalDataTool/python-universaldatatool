from .camelify import camelify_dict, camelify


class Sample(object):

    param_names = [
        "audioUrl",
        "pdfUrl",
        "imageUrl",
        "videoUrl",
        "url",
        "markdown",
        "document",
        "fields",
        "surveyjs",
        "annotation",
        "videoFrameAt",
        "videoFrame",
    ]
    data = {}

    def __init__(self, constructor_dict={}, **kwargs):
        self.data = constructor_dict.copy()
        self.data.update(camelify_dict(kwargs))

    def to_dict(self):
        return self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, v):
        self.data[key] = v

    def __getattr__(self, attr):
        if camelify(attr) in self.data:
            return self.data[camelify(attr)]
        raise AttributeError(attr)

    def __setattr__(self, attr, v):
        camel_attr = camelify(attr)
        if camel_attr in self.param_names:
            self.data[camel_attr] = v
        super(Sample, self).__setattr__(attr, v)
