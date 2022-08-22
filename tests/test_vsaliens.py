import pytest
from incolume.py.vsaliens import vsaliens


def test_vsaliens():
    o = vsaliens.Point(12, 13)
    assert o == ''
