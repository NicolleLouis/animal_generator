from unittest import mock

import pytest

from animal_generator.zoo_viewer import ZooViewer
from pathlib import PosixPath


def test_find_zoo():
    zoo = ZooViewer.find_zoo()
    assert PosixPath == type(zoo)


def test_find_zoo_fail():
    with mock.patch('pathlib.Path.iterdir', return_value=[]):
        with pytest.raises(BaseException):
            ZooViewer.find_zoo()


def test_find_animal_fail():
    with pytest.raises(BaseException):
        ZooViewer.find_animal("fake_animal")


def test_find_animal():
    animal = ZooViewer.find_animal("example_animal")
    assert dict == type(animal)
