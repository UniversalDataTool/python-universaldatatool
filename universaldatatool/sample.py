from universaldatatool.camelify import camelify_dict


class Sample:

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
