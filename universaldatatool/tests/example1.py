import pytest
import json
from universaldatatool import Dataset
from universaldatatool import Interface
from universaldatatool import Sample

ex_udt_file = {
    "interface": {"type": "image_classification", "labels": ["good", "bad"]},
    "samples": [
        {
            "imageUrl": "https://cdn.pixabay.com/photo/2017/06/12/19/02/cat-2396473__480.jpg"
        }
    ],
}
ex_json_string = json.dumps(ex_udt_file, sort_keys=True)


class TestDatasetLoading(object):
    def test_json_constructor(self):
        ds = Dataset(ex_udt_file)
        assert ds.to_json_string() == ex_json_string

    def test_1(self):
        iface = Interface(type="image_classification")
        assert json.dumps(iface.to_dict(), sort_keys=True) == json.dumps(
            {"type": "image_classification"}, sort_keys=True
        )

    def test_2(self):
        ds = Dataset(
            {"interface": {"type": "image_classification"}},
            labels=["good", "bad"],
            image_url="https://cdn.pixabay.com/photo/2017/06/12/19/02/cat-2396473__480.jpg",
        )
        assert ds.to_json_string() == ex_json_string

    def test_3(self):
        ds = Dataset(
            type="image_classification",
            labels=["good", "bad"],
            image_url="https://cdn.pixabay.com/photo/2017/06/12/19/02/cat-2396473__480.jpg",
        )
        assert ds.to_json_string() == ex_json_string

    def test_4(self):
        ds = Dataset(ex_udt_file)
        assert ds.type == "image_classification"

    def test_5(self):
        iface = Interface(type="image_classification")
        iface.type = "image_segmentation"
        assert iface.type == "image_segmentation"
        assert iface.to_dict()["type"] == "image_segmentation"

    def test_6(self):
        ds = Dataset(type="image_classification")
        ds.type = "image_segmentation"
        assert ds.type == "image_segmentation"
        assert ds.interface.type == "image_segmentation"
        assert ds.to_dict()["interface"]["type"] == "image_segmentation"
