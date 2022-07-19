import sys

import pytest
from pytest import MonkeyPatch

import common_nb_preprocessors._constant_builder
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


@pytest.mark.parametrize("without_lib", ["pandas", "bs4", "html5lib"])
def test_import_error(without_lib: str, monkeypatch: MonkeyPatch):
    monkeypatch.setitem(sys.modules, without_lib, None)

    # reload as otherwise monkey-patching was not sufficient
    # when running all tests
    import importlib

    with pytest.raises(ImportError, match="requires"):
        importlib.reload(common_nb_preprocessors._constant_builder)


def test_multiple_matching_tables(monkeypatch: MonkeyPatch):
    def return_two_elem_list(*args, **kwargs):
        return [1, 2]

    import pandas

    monkeypatch.setattr(pandas, "read_html", return_two_elem_list)
    with pytest.raises(ValueError, match="unique table"):
        common_nb_preprocessors._constant_builder._read_unique_myst_nb_table(
            "IamNotOnTheMySTPageAndWillNotFindAMatch"
        )
