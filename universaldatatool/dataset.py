import json
from .camelify import camelify_dict, camelify
from .interface import Interface
from .sample import Sample
import universaldatatool as udt


class Dataset(object):
    """
    Represents a UniversalDataTool dataset.
    """

    def __init__(self, constructor_dict=None, **kwargs):
        self.__dict__["interface"] = None
        self.__dict__["samples"] = None
        self.__dict__["collaborative_session"] = None
        self.__dict__["proxied_file_session"] = None

        interface_kwargs = {}
        first_sample_kwargs = {}
        kwargs = camelify_dict(kwargs)
        for k, v in kwargs.items():
            if k in Interface.param_names:
                interface_kwargs[k] = v
            elif k in Sample.param_names:
                first_sample_kwargs[k] = v
            else:
                interface_kwargs[k] = v

        if "interface" in kwargs:
            if isinstance(kwargs["interface"], Interface):
                self.interface = kwargs["interface"]
            else:
                self.interface = Interface(kwargs["interface"])

        if self.interface is None:
            if constructor_dict is not None:
                self.interface = Interface(
                    constructor_dict.get("interface", {}), **interface_kwargs
                )
            else:
                self.interface = Interface(**interface_kwargs)

        user_sample_list = None
        if constructor_dict is not None and "samples" in constructor_dict:
            user_sample_list = constructor_dict["samples"]
        if "samples" in kwargs:
            user_sample_list = kwargs["samples"]

        # plural syntaxes, e.g. image_paths
        for singular_key in Sample.param_names:
            plural_key = singular_key + "s"
            if plural_key in kwargs and isinstance(kwargs[plural_key], list):
                user_sample_list = []
                for val in kwargs[plural_key]:
                    d = {}
                    d[singular_key] = val
                    user_sample_list.append(d)

        if user_sample_list is not None:
            self.samples = []
            for sample_obj in user_sample_list:
                if isinstance(sample_obj, Sample):
                    self.samples.append(sample_obj)
                else:
                    self.samples.append(Sample(sample_obj))

        if self.samples is None:
            if bool(first_sample_kwargs):
                self.samples = [Sample(**first_sample_kwargs)]
            else:
                self.samples = []

    def to_dict(self, **kwargs):
        if self.proxied_file_session is None and kwargs.get("proxy_files", False):
            self.proxy_files()
        return_dict = {}
        return_dict["interface"] = self.interface.to_dict(
            session=self.proxied_file_session, **kwargs
        )
        return_dict["samples"] = [
            sample.to_dict(session=self.proxied_file_session, **kwargs)
            for sample in self.samples
        ]
        return return_dict

    def to_json(self, **kwargs):
        return self.to_dict(**kwargs)

    def to_json_string(self, **kwargs):
        return json.dumps(self.to_dict(**kwargs), sort_keys=True)

    def __getattr__(self, attr):
        camel_attr = camelify(attr)
        if camel_attr in Interface.param_names:
            return self.interface[camel_attr]
        elif len(self.samples) == 0 and camel_attr in Sample.param_names:
            return self.samples[0][camel_attr]
        raise AttributeError(attr)

    def __setattr__(self, attr, v):
        camel_attr = camelify(attr)
        if camel_attr in Interface.param_names:
            self.interface[camel_attr] = v
            return
        elif (
            self.samples is not None
            and len(self.samples) == 0
            and camel_attr in Sample.param_names
        ):
            self.samples[0][camel_attr] = v
            return
        super(Dataset, self).__setattr__(attr, v)

    def show(self):
        udt.nb.open(self)

    def display(self):
        udt.nb.open(self)

    def open(self):
        udt.nb.open(self)

    def edit(self):
        udt.nb.open(self)

    def proxy_files(self, local_web_server=False):
        if self.proxied_file_session is not None:
            self.stop_editing()
        if local_web_server:
            self.proxied_file_session = udt.nb.WebLocalFileProxyServer()
        else:
            self.proxied_file_session = udt.nb.PublicFileProxy()
        self.proxied_file_session.start()

    def edit_online(self):
        return udt.nb.edit_online(self)

    def edit_local(self):
        return udt.nb.edit_local(self)

    def stop_editing(self):
        if self.collaborative_session is not None:
            self.collaborative_session.stop()
            self.collaborative_session = None

        if self.proxied_file_session is not None:
            self.proxied_file_session.stop()
            self.proxied_file_session = None

    def sync(self):
        self.collaborative_session.sync_changes()

    def __str__(self):
        return "<Dataset {} ({} samples)>".format(
            self.interface.type, len(self.samples)
        )

    def __repr__(self):
        return "<Dataset {} ({} samples)>".format(
            self.interface.type, len(self.samples)
        )
