import json
from .camelify import camelify_dict, camelify
from .interface import Interface
from .sample import Sample
import universaldatatool as udt


class Dataset(object):
    def __init__(self, constructor_dict=None, **kwargs):
        self.__dict__["interface"] = None
        self.__dict__["samples"] = None
        self.__dict__["online_session"] = None

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
        return_dict = {}
        return_dict["interface"] = self.interface.to_dict(**kwargs)
        return_dict["samples"] = [sample.to_dict(**kwargs) for sample in self.samples]
        return return_dict

    def to_json_string(self, **kwargs):
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_legacy_json_string(self, **kwargs):
        legacy_dict = {}
        legacy_dict["interface"] = self.interface.to_dict(**kwargs)
        if "labels" in legacy_dict["interface"]:
            legacy_dict["interface"]["availableLabels"] = legacy_dict["interface"][
                "labels"
            ]
        legacy_dict["taskData"] = [s.to_dict(**kwargs) for s in self.samples]
        legacy_dict["taskOutput"] = [
            s.to_dict(**kwargs).get("annotation", None) for s in self.samples
        ]
        return json.dumps(legacy_dict, sort_keys=True)

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

    def edit_online(self):
        return udt.nb.edit_online(self)

    def sync(self):
        self.online_session.sync_changes()
