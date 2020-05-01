# Universal Data Tool Python Module

> This is currently a work in progress specification for the python module

pip module for data labeling based leveraging the Universal Data Tool

```bash
pip install universaldatatool
```

## Basic Usage

```python
import universaldatatool as udt

file = udt.File()

```

## Submodules

* udt.nb: jupyter notebook widget

## Methods

* udt.load_json(file_path): Load UDT File from json
* udt.load_csv(file_path): Load UDT File from csv
* udt.File(file_path = None, interface = None) : Create UDT File
* udt.File.save(file_path = None) : Save file (extension should be ".udt.json", ".udt.csv")
* udt.Interface(type=None, labels=None): Create UDT interface
* udt.Sample(image_url=None, document=None, ...) : Create UDT Sample
* udt.nb.display(udt_file): Display Universal Data Tool widget
