import pytest


@pytest.mark.django_db
class TestMySQL(object):
    @pytest.fixture
    def models_sqla(self):
        from mysql_app import models_sqla as _models_sqla
        return _models_sqla

    def test_CategoryRelation(self, models_sqla):
        actual = models_sqla.CategoryRelation.c.keys()
        expected = ['category1_id', 'category2_id', 'type']
        assert actual == expected