import pytest


class Test_get_camelcase(object):
    def _callFUT(self, s, capitalize):
        from utils import get_camelcase
        return get_camelcase(s, capitalize)

    @pytest.mark.parametrize(
        'snakecase, capitalize, expected',
        [
            ('spam_ham_egg', False, 'spamHamEgg'),
            ('foo_bar', True, 'FooBar'),
        ]
    )
    def test_get_camelcase(self, snakecase, capitalize, expected):
        actual = self._callFUT(snakecase, capitalize)
        assert actual == expected
