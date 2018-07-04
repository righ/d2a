import pytest


class Test_alias(object):
    def _callFUT(self, new_field, existing_field):
        from d2a.fields import alias
        return alias(new_field, existing_field)

    @pytest.fixture()
    def charfield(self):
        from django.db.models import CharField
        return CharField

    @pytest.fixture()
    def newfield(self, charfield):
        class NewField(charfield):
            pass
        return NewField

    def test_new_field_added(self, newfield, charfield):
        self._callFUT(newfield, charfield)
        from d2a.fields import mapping
        assert newfield in mapping
