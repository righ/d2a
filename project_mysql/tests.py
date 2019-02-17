import pytest
import sqlalchemy as sa


def info(table):
    result = {}
    for key, col in table.c.items():
        result[key] = {
            'primary_key': col.primary_key,
            'unique': col.unique,
            'type': type(col.type),
            'nullable': col.nullable,
        }
        if col.default:
            default = col.default.arg
            if callable(default):
                # because it can't check function's equality.
                default = default.__name__
            result[key]['default'] = default
    return result


class TestMySQL(object):
    @pytest.fixture
    def books(self):
        from books import modelsa
        return modelsa

    @pytest.fixture
    def sales(self):
        from sales import modelsa
        return modelsa

    def test_CategoryRelation(self, books):
        actual = info(books.CategoryRelation.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
            },
            'category1_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
            },
            'category2_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
            },
            'type': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.VARCHAR,
                'nullable': True,
            },
        }
        assert actual == expected

    def test_Author(self, books):
        actual = info(books.Author.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
            },
            'name': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.VARCHAR,
                'nullable': False,
            },
            'age': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.SMALLINT,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_Category(self, books):
        actual = info(books.Category.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
            },
            'name': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.VARCHAR,
                'nullable': False,
            },
            'created': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.DATETIME,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_Book(self, books):
        actual = info(books.Book.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.mysql.types.CHAR,
                'nullable': False,
                'default': 'uuid4',
            },
            'price': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
                'default': 100,
            },
            'title': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.VARCHAR,
                'nullable': False,
            },
            'description': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.LONGTEXT,
                'nullable': True,
            },
            'author_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': True,
            },
            'content': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.LONGBLOB,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_BookCategory(self, books):
        actual = info(books.BookCategory.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
            },
            'book_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.CHAR,
                'nullable': False,
            },
            'category_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.INTEGER,
                'nullable': False,
            },
        }
        assert actual == expected

    def test_Sales(self, sales):
        actual = info(sales.Sales.__table__)
        expected = {
            'id': {
                'primary_key': True,
                'unique': True,
                'type': sa.dialects.mysql.types.BIGINT,
                'nullable': False,
            },
            'book_id': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.CHAR,
                'nullable': False,
            },
            'sold': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.DATETIME,
                'nullable': False,
            },
            'reservation': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.BIGINT,
                'nullable': True,
            },
            'source': {
                'primary_key': False,
                'unique': False,
                'type': sa.dialects.mysql.types.CHAR,
                'nullable': True,
            },

        }
        assert actual == expected
