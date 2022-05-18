from unittest.mock import MagicMock
from posterr.services.base import ServiceBase

class MockClass:
    pass

class TestServiceBase:
    db = MagicMock()
    dao = MagicMock()
    cache = MagicMock()
    service = ServiceBase()

    def test_save(self):
        # arrange
        self.dao.save = MagicMock(return_value="some_id")

        # act
        inserted_id = self.service.save(self.dao, self.db)

        # assert
        assert inserted_id == "some_id"

    def test_get_all(self):
        # arrange
        props = { "prop": "value" }
        self.service.build(props)
        self.dao.get_all = MagicMock(return_value=[{ "prop": "value" }])

        # act
        items = ServiceBase.get_all(self.dao, self.db, self.cache)

        # arrange
        assert self.service.__dict__ == items[0].__dict__

    def test_get_by_id(self):
       # arrange
        props = { "prop": "value" }
        self.service.build(props)
        self.dao.get_by_id = MagicMock(return_value={ "prop": "value" })
        
        # act
        items = ServiceBase.get_by_id("some-id", self.dao, self.db, self.cache)

        # arrange
        assert self.service.__dict__ == items.__dict__
    
    def test_build(self):
        # arrange
        props = { "prop": "value" }

        # act
        service = self.service.build(props)

        # assert
        assert service.__dict__ == props

        


