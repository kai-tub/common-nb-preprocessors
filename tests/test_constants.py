from unittest.mock import patch

import pytest

from common_nb_preprocessors.myst_nb import MystNBCellConf, MystNBCellTags


# FUTURE: Figure out how to cache the pandas parsing
def test_mystnb_cell_tags_constant():
    MystNBCellTags._validate()


def test_mystnb_cell_conf_constant():
    MystNBCellConf._validate()


def test_unsynced_mystnb_cell_tags_constant(monkeypatch):
    def a(_):
        yield

    # TODO: understand why this is the case!
    monkeypatch.setattr(MystNBCellTags.__class__, "__iter__", a)
    with pytest.raises(RuntimeError):
        MystNBCellTags._validate()


def test_unsynced_mystnb_cell_conf_constant(monkeypatch):
    def a(_):
        yield

    # TODO: understand why this is the case!
    monkeypatch.setattr(MystNBCellConf.__class__, "__iter__", a)
    with pytest.raises(RuntimeError):
        MystNBCellConf._validate()


# TODO: Check if import error is raised
# TODO: Use pdm to only install local deps and check
# that the correct packages are installed!
