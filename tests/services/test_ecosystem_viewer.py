from unittest import mock

import pytest

from animal_generator.models.ecosystem import Ecosystem
from animal_generator.services.ecosystem_viewer import EcosystemViewer, EcosystemViewerException
from pathlib import PosixPath


def test_find_list_ecosystem():
    list_ecosystem = EcosystemViewer.find_list_ecosystem()
    assert isinstance(list_ecosystem, PosixPath)


def test_find_list_ecosystem_fail():
    with mock.patch('pathlib.Path.iterdir', return_value=[]):
        with pytest.raises(EcosystemViewerException):
            EcosystemViewer.find_list_ecosystem()


def test_find_ecosystem_fail():
    with pytest.raises(EcosystemViewerException):
        EcosystemViewer.find_ecosystem("fake_ecosystem")


def test_find_ecosystem():
    ecosystem = EcosystemViewer.find_ecosystem("example_ecosystem")
    assert isinstance(ecosystem, Ecosystem)
