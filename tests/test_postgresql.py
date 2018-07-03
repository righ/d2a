import pytest
import sqlalchemy as sa


def info(table):
    i = {
        key: {
            'primary_key': col.primary_key,
            'unique': col.unique,
            'type': type(col.type),
            'nullable': col.nullable,
        }
        for key, col in table.c.items()
    }
    return i


@pytest.mark.django_db
class TestPostgreSQL(object):
    @pytest.fixture
    def models_sqla(self):
        from postgresql_app import models_sqla as _models_sqla
        return _models_sqla

    def test_CategoryRelation(self, models_sqla):
        actual = info(models_sqla.CategoryRelation.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': False,
            },
            'category1_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': False,
            },
            'category2_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': False,
            },
            'type': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.VARCHAR,
                'nullable': True,
            },
        }
        assert actual == expected

    def test_Author(self, models_sqla):
        actual = info(models_sqla.Author.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': False,
            },
            'name': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.VARCHAR,
                'nullable': False,
            },
            'age': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.SMALLINT,
                'nullable': False,
            },

        }
        assert actual == expected

    def test_Category(self, models_sqla):
        actual = info(models_sqla.Category.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': False,
            },
            'name': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.VARCHAR,
                'nullable': False,
            },
            'created': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.DateTime,
                'nullable': False,
            },

        }
        assert actual == expected

    def test_Book(self, models_sqla):
        actual = info(models_sqla.Book.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.postgresql.UUID,
                'nullable': False,
            },
            'price': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.JSON,
                'nullable': False,
            },
            'title': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.VARCHAR,
                'nullable': False,
            },
            'description': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.Text,
                'nullable': True,
            },
            'author_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': True,
            },
            'content': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.BYTEA,
                'nullable': False,
            },
            'tags': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.ARRAY,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_BookCategory(self, models_sqla):
        actual = info(models_sqla.BookCategory.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': False,
            },
            'book_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.UUID,
                'nullable': False,
            },
            'category_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.INTEGER,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_Sales(self, models_sqla):
        actual = info(models_sqla.Sales.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.sql.sqltypes.BIGINT,
                'nullable': False,
            },
            'book_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.UUID,
                'nullable': False,
            },
            'sold': {
                'primary_key': False,
                'unique': False,
                'type': sa.sql.sqltypes.DateTime,
                'nullable': False,
            },
            'reservation': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INTERVAL,
                'nullable': True,
            },
            'source': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.postgresql.INET,
                'nullable': True,
            },

        }
        assert actual == expected