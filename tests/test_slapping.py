import pytest
from PyTeXEditor import hello


def test_empty_slap():
    assert hello.a("asd") == "asd"

