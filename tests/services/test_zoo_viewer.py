from unittest import mock

import pytest

from animal_generator.models.animal import Animal
from animal_generator.services.zoo_viewer import ZooViewer, ZooViewerException
from pathlib import PosixPath


def test_find_zoo():
    zoo = ZooViewer.find_zoo()
    assert isinstance(zoo, PosixPath)


def test_find_zoo_fail():
    with mock.patch('pathlib.Path.iterdir', return_value=[]):
        with pytest.raises(ZooViewerException):
            ZooViewer.find_zoo()


def test_find_animal_fail():
    with pytest.raises(ZooViewerException):
        ZooViewer.find_animal("fake_animal")


def test_find_animal():
    animal = ZooViewer.find_animal("example_animal")
    assert isinstance(animal, Animal)
