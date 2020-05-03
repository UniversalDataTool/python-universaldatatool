import universaldatatool as udt
from universaldatatool.nb.Session import Session


class TestDatasetLoading(object):
    def test_create_collaborative_session(self):
        session = Session()
        session.create_collaborative_session(
            udt.Dataset(
                type="image_classification",
                samples=[
                    {
                        "imageUrl": "https://s3.amazonaws.com/asset.workaround.online/example-jobs/sticky-notes/image1.jpg"
                    }
                ],
            )
        )

        assert len(session.collab_session_id) > 3
        assert session.version == 0

    def test_proxied_dataset(self):
        ds = udt.Dataset(
            type="image_classification",
            image_path="/home/seve/downloads/birds/izJiyLE.png",
        )
        session = Session()
        session.localfileproxy_client_id = "test_localfileproxy_client_id"
        proxied_dict = ds.to_dict(proxy_files=True, session=session)
        assert proxied_dict["samples"][0]["imageUrl"].startswith("http")
        assert "test_localfileproxy" in proxied_dict["samples"][0]["imageUrl"]

    def test_create_session(self):
        session = Session()
        session.start(
            udt.Dataset(
                type="image_classification",
                image_path="/home/seve/downloads/birds/izJiyLE.png",
            )
        )
