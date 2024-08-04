from unittest import TestCase
from utils import bidict


class TestUtils(TestCase):
    def test_bidict(self):
        b_dict = bidict({"a": 1})

        assert b_dict["a"] == 1
        assert b_dict.by_val(1) == "a"
        assert "a" in b_dict
        assert b_dict.exist_val(1)
