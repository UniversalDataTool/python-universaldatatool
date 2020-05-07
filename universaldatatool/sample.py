from .camelify import camelify_dict, camelify
import os


def correct_param(name, value):
    if name == "img" and not value.startswith("http"):
        name = "imagePath"
    if name.endswith("Path"):
        name = name[:-4] + "Url"
        value = "file://" + os.path.abspath(value)
    elif name == "audio" or name == "image" or name == "pdf" or name == "video":
        name = name + "Url"
        if not value.startswith("http"):
            value = "file://" + os.path.abspath(value)
    return name, value


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
        "audio",
        "image",
        "img",
        "pdf",
        "video",
        "audioPath",
        "imagePath",
        "pdfPath",
        "videoPath",
    ]
    data = {}

    def __init__(self, constructor_dict={}, **kwargs):
        data = constructor_dict.copy()
        data.update(camelify_dict(kwargs))
        self.data = {}
        for name, value in data.items():
            n, v = correct_param(name, value)
            self.data[n] = v

    def to_dict(self, proxy_files=False, session=None):
        if proxy_files == False:
            return self.data
        else:
            if session is None:
                raise ValueError(
                    "Cannot proxy files with a ProxiedFileSession (session=None in Sample.to_dict)"
                )
            ret_data = self.data.copy()
            # create a proxied version of any local files
            url_keys = ["imageUrl", "pdfUrl", "videoUrl", "audioUrl"]
            for url_key in url_keys:
                if url_key in ret_data and ret_data[url_key].startswith("file://"):
                    proxied_url = session.get_proxied_file_url(ret_data[url_key])
                    ret_data["original" + url_key.capitalize()] = ret_data[url_key]
                    ret_data[url_key] = proxied_url
            return ret_data

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
            return
        super(Sample, self).__setattr__(attr, v)
