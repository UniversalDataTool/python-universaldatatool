import json
from .camelify import camelify_dict, camelify
from .interface import Interface
from .sample import Sample


class Dataset(object):
    def __init__(self, constructor_dict=None, **kwargs):
        self.__dict__["interface"] = None
        self.__dict__["samples"] = None
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

        if constructor_dict is not None:
            self.interface = Interface(
                constructor_dict.get("interface", {}), **interface_kwargs
            )
            if "samples" in constructor_dict:
                self.samples = []
                for sample_obj in constructor_dict["samples"]:
                    if isinstance(sample_obj, Sample):
                        self.samples.append(sample_obj)
                    else:
                        self.samples.append(Sample(sample_obj))
        else:
            self.interface = Interface(**interface_kwargs)

        if self.samples is None:
            if bool(first_sample_kwargs):
                self.samples = [Sample(**first_sample_kwargs)]
            else:
                self.samples = []

    def to_dict(self):
        return_dict = {}
        return_dict["interface"] = self.interface.to_dict()
        return_dict["samples"] = [sample.to_dict() for sample in self.samples]
        return return_dict

    def to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def __getattr__(self, attr):
        camel_attr = camelify(attr)
        if camel_attr in Interface.param_names:
            return self.interface[camel_attr]
        elif len(self.samples) == 0 and camel_attr in Sample.param_names:
            return self.samples[0][camel_attr]
        raise AttributeError(attr)

    def __setattr__(self, attr, v):
        print(self.interface, attr)
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
