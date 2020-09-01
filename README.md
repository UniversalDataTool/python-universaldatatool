# Universal Data Tool Python

Python module for data labeling leveraging the Universal Data Tool.

## Features

- Open [Universal Data Tool](https://github.com/UniversalDataTool/universal-data-tool) in Jupyter notebook
- Massage data into and out of the [UDT format](https://github.com/UniversalDataTool/udt-format)

## Usage

```bash
pip install universaldatatool
```

```python
import universaldatatool as udt

ds = udt.Dataset(
    type="image_segmentation",
    image_paths=["/path/to/birds/good_bird.jpg","/path/to/birds/bird2.jpg"],
    labels=["good bird", "bad bird"]
)

# Opens dataset directly in jupyter notebook
ds.open()
```

# API

## Submodules

- udt.nb: jupyter notebook widget

## Methods

- udt.load_json(file_path): Load UDT File from json
- udt.load_csv(file_path): Load UDT File from csv
- udt.Dataset(type=None, image_paths=None, labels=None)
- udt.Interface(type=None, labels=None): Create UDT interface
- udt.Sample(image_url=None, document=None, ...) : Create UDT Sample
- udt.nb.display(udt_file): Display Universal Data Tool widget

## TODOs

- [x] `image_path`, `video_path` etc. support
- [ ] Better Docs
- [ ] Usage Examples
- [ ] Load CSV or JSON from files
- [x] Collaborative synchronization w/ universaldatatool.com
- [x] `edit`/`open` should check that there are no local paths
- [ ] Helpful stringification
- [ ] Make it easy to run tests
- [ ] Image Segmentation kills jupyter notebook scrolling
- [ ] Make JupyterLab Extension [1](https://github.com/jupyterlab/extension-cookiecutter-ts) [2](https://github.com/jupyterlab/extension-examples) [3](https://github.com/wolfv/jupyterlab-dynext)
- [x] Continuous integration testing via Github Actions
- [x] Cypress browser testing

# Development

## Running Cypress Tests

Cypress will automatically open a browser and create jupyter notebooks with different test scenarios. It's really fast for developing and testing. To
use it, you must first run our jupyter docker container, which mounts volumes properly such that universaldatatool can be imported. To do this, run:

```bash
yarn start:jupyter
```

A jupyter notebook is now running in the background.

You can now run the cypress tests in development mode by running...

```bash
yarn cy:run
```

An electron browser will open with automated tests.

## How To Test

Each file in the `universaldatatool/tests` directory can be tested with pytest e.g.

```bash
python -m pytest universaldatatool/tests/example1.py
```

## Releasing
